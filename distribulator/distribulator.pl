#!/usr/local/bin/perl
######################################################################
# $Id$
#
# Name: distribulator.pl
#
# Description: The Distribulator.
# A detailed description can be found in the ../README file.
#
######################################################################
#
# Force unbuffered output.
#
$|=1;

#
# * Enforce strict conventions.
# * Current working directory Module
# * Command-line Options Module
# * ICMP ping Module
# * Perl documentation Module
# * Unix hostname Module
# * Readline Module
#
use strict;
use Cwd;
use Getopt::Long;
use Net::Ping;
use Pod::Usage;
use Sys::Hostname;
use Term::ReadLine;

######################################################################
# USER CONFIGURABLE SETTINGS
#
# Where distribulator is installed, required for help files.
my($HOME_DIR) =   '/usr/local/novo/distribulator';
# Where the configuration files are located.
my($CONFIG_DIR) = '/usr/local/novo/distribulator/conf';
#
# Binary Locations - These are defined further on in the file.
# ------------------------------------------------------------
my($SCP_BIN, $SSH_BIN);
######################################################################

######################################################################
# NON-USER CONFIGURABLE SETTINGS
#
# Unless you know what you're doing, don't go here!
######################################################################
#
# Constant Variables (Fix Me!)
#
my($FALSE) = 0;
my($TRUE) = 1;
#
# Runtime Arg/Temp Variables
#
my($env_arg, $help_arg, $noping_arg, $shell_arg, $version_arg) = '';
my($command);
my(@command_tokens);
my($exec_str);
my($input);
my($prompt);
my($remote_command);
my($server);
my($temp_str);
my($user);
my($userserver);
my($MYFILE);

#
# State Tracking Variables
#
my($current_server_group) = 'wlx';
my($environment);
my(@external_commands);
my(@server_groups);
my(%groups_userservers_hash);
my(@internal_commands) = ( 'cd', 'copy', 'exit', 'help', 'login', 'remote-shell',
    'run', 'server-group', 'server-list' );

GetOptions("env=s" => \$env_arg,
           "help" => \$help_arg,
           "noping" => \$noping_arg,
           "shell=s" => \$shell_arg,
           "version" => \$version_arg) ||
    pod2usage(-exitstatus => 0, -verbose => 2);
#
# Check for --help
#
if ($help_arg)
{
    pod2usage(-exitstatus => 0, -verbose => 2);
}
#
# Give the user a banner, no matter what.
#
print("+=======================+\n");
print("|The Distribulator v0.45|\n");
print("+=======================+\n");
print("\n");
#
# Check for --version
#
if ($version_arg)
{
    print("(c) Copyright 2002 Adam W. Dace.\n");
    print("The Distribulator may be copied only under the terms of the BSD License,\n");
    print("a copy of which can be found with The Distribulator distribution kit.\n");
    print("\n");
    print("Specify the --help option for further information about The Distribulator.\n");
    print("\n");

    exit(0);
}
#
# Validate our command-line arguments.
#
ValidateArgs();
#
# Load server group configuration from appropriate files.
#
LoadConfig();
#
# Find out where our binaries are located.
#
getBinaryLocations();
#
# Preparing to launch the shell.
#
my($user) = getlogin() || getpwuid($<);
my($hostname) = Sys::Hostname::hostname();
#
# Setup signal handler for SIGQUIT, aka CTRL-D.
# This doesn't appear compatible with ReadLine.
#
$SIG{QUIT} = \&catchSigQuit;
#
# Setup ReadLine for input...
#
my $term = new Term::ReadLine 'Distribulator';
$term->ornaments(0,0,0,0);
#
# Print a little intro.
#
print("Local Install Dir:       $HOME_DIR\n");
print("Local Config Dir:        $CONFIG_DIR\n");
print("Local Host:              $hostname\n");
print("Current Environment:     $environment\n");
print("\n");
print("Shell Commands Loaded:   " .
      scalar (@external_commands) . "\n");
print("Available Server Groups: @server_groups\n");
print("\n");
print("Prompt Description:      <user\@environment[current_server_group]:local_dir>\n");
print("\n");
print("Confused?  Need help?  Try typing \'help\' and see what happens!\n");
print("\n");

#
# The Never Ending Loop...
#
while ($TRUE)
{
    $command = '';
    $prompt = "<$user\@$environment\[$current_server_group\]:" .
        cwd() . "> ";
    $input = $term->readline($prompt);

    @command_tokens = split(' ', $input);
    $command = shift(@command_tokens);

    # If the user just hit ENTER, simply give them another prompt.
    # How can we possibly detect CTRL-D?
    if ($input eq '')
    {
        next;
    }

    # If the command isn't found in the array.
    if ( (!isValidInternalCommand($command)) &&
         (!isValidExternalCommand($command)) )
    {
        print("ERROR: Unknown Command: $command\n");

        next;
    }

    #################### IMPLEMENTED - Internal ####################

    # Copy
    if ($command eq 'copy')
    {
        ParseCopy();

        next;
    }

    # Exit
    if ( ($command eq 'exit') )
    {
        print "Received exit command.  Dying...\n\n";

        exit(0);
    }

    # Group
    if ($command eq 'server-group')
    {
        $temp_str = shift(@command_tokens);

        if ( !$temp_str )
        {
            print("ERROR: No server group given.\n");
        }
        elsif ( $groups_userservers_hash{$temp_str} )
        {
            $current_server_group = $temp_str;
            print("NOTE:  Current server group now is '$current_server_group'.\n");
        }
        else
        {
            print("ERROR: Unknown server group $temp_str.\n");
        }

        next;
    }

    # Help
    if ($command eq 'help')
    {
        $temp_str = shift(@command_tokens);

        # If the next argument is a valid command, show help for it.
        if ( isValidInternalCommand($temp_str) )
        {
            if ( !PrintHelpFile("$temp_str-desc.txt") )
            {
                print("ERROR: Problem displaying $temp_str-desc.txt file.\n");
            }
        }
        else
        {
            if ( !PrintHelpFile('help.txt') )
            {
                print("ERROR: Problem displaying help.txt file.\n");
            }
        }

        next;
    }

    # Login
    if ($command eq 'login')
    {
        $temp_str = shift(@command_tokens);

        if ( $userserver = getMatchingUserServer($temp_str) )
        {
            if ( PingUserServer($userserver) )
            {
                $temp_str = "$SSH_BIN $userserver";

                print "EXEC:  $temp_str\n";

                system($temp_str);
            }
        }
        else
        {
            print("ERROR: No server hostname matching '$temp_str' found.\n");
        }

        next;
    }

    # List
    if ($command eq 'server-list')
    {
        $temp_str = shift(@command_tokens);

        # If there's no target, list the current server group.
        if ( !$temp_str )
        {
            print("Known user-server pairs in group $current_server_group:\n");

            foreach $userserver ( sort @{$groups_userservers_hash{$current_server_group}} )
            {
        print("$userserver\n");                    
            }

        }
        elsif ( $groups_userservers_hash{$temp_str} )
        {
            print("Known user-server pairs in group $temp_str:\n");

            foreach $userserver ( sort @{$groups_userservers_hash{$temp_str}} )
            {
                    print("$userserver\n");                    
            }

        }
        else
        {
            print("ERROR: No server group matching '$temp_str' found.\n");
        }

        next;
    }

    # Run
    if ($command eq 'run')
    {
        ParseRun();

        next;
    }

    #################### IMPLEMENTED - External ####################

    # Unix-style change directory
    if ($command eq 'cd')
    {
        $temp_str = shift(@command_tokens);

        if ( !chdir($temp_str) )
        {
            print("ERROR: Directory $temp_str not found.\n");
        }

        next;
    }

    # This should match any of the listed external commands.
    if ( isValidExternalCommand($command) )
    {
        RunCommandLocal($input);

        next;
    }

    #################### NOT IMPLEMENTED ####################

    if ($command eq 'remote-shell')
    {
        print("ERROR: This command is not yet implemented.\n");
    }
}

#
# Ask the ever-necessary "Are You Sure?" question.
#
sub AreYouSure
{
    if ( $term->readline("Yes / No> ") =~ /^[Yy]/ )
    {
        return $TRUE;
    }
    else
    {
        print "Okay, NOT running the command.\n";

        return $FALSE;
    }
}

#
# Catch SIGQUIT signal, and cleanly exit the program.
#
sub catchSigQuit
{
    print "Caught SIGQUIT signal(probably CTRL-D).  Dying...\n\n";

    exit(0);
}

#
# Attempt to guess where our binaries are located.
#
sub getBinaryLocations
{
    my($uname1_bin) = '/bin/uname';
    my($uname2_bin) = '/usr/bin/uname';
    my($os_name) = '';

    if ( stat($uname1_bin) )
    {
        $os_name = qx/$uname1_bin/;
    }
    elsif ( stat($uname2_bin) )
    {
        $os_name = qx/$uname2_bin/;
    }
    else
    {
        die("Unable to determine platform.  Can't find uname!");
    }

    chomp($os_name);

    #
    # Binary utility locations, setup based on platform.
    #
    # NOTE: Blowfish is chosen because of its low CPU overhead.
    #
    if ($os_name eq 'Linux')
    {
        $SCP_BIN = '/usr/bin/scp -c blowfish';
        $SSH_BIN = '/usr/bin/ssh -c blowfish';
    }
    elsif ($os_name eq 'SunOS')
    {
        $SCP_BIN = '/usr/local/bin/scp -c blowfish';
        $SSH_BIN = '/usr/local/bin/ssh -c blowfish';
    }
}

#
# Take the passed-in string, and do fuzzy matching with
# existing groups.
#
sub getMatchingGroup
{
    my($search_group) = @_;
    my($group, $group_server, $sub_string);

    foreach $group (sort keys(%groups_userservers_hash) )
    {
        if ($search_group eq $group)
        {
            return $group;
        }
    }

    return $FALSE;
}

#
# Take the passed-in string, and do fuzzy matching with
# existing groups.
#
sub getMatchingUserServer
{
    my($partial) = @_;
    my($group, $sub_string);

    foreach $group (sort keys(%groups_userservers_hash) )
    {
        foreach $userserver ( @{$groups_userservers_hash{$group}} )
        {
        $userserver =~ /(\w*)\@([0-9a-zA-z.]*)/;

            if ($partial eq $2)
            {
                return $userserver;
            }

            $sub_string = substr($2, 0, length($partial));

            if ($partial eq $sub_string)
            {
                return $userserver;
            }
        }
    }

    return $FALSE;
}

#
# Find one of the groups this server belongs to.
#
sub getServerGroup
{
    my($find_server) = @_;
    my($group, $group_server);

    foreach $group (sort keys(%groups_userservers_hash) )
    {
        foreach $userserver ( @{$groups_userservers_hash{$group}} )
        {
            $userserver =~ /(\w*)\@([0-9a-zA-z.]*)/;

            if ($find_server eq $2)
            {
                return $group;
            }
        }
    }
}

#
# Lookup which user we need to connect as.
#
sub getServerUser
{
    my($server) = @_;

    my($group) = getServerGroup($server);

    $userserver = pop(@{$groups_userservers_hash{$group}});
    $userserver =~ /(\w*)\@([0-9a-zA-z.]*)/;

    return $1;
}

#
# Load server group configuration from files.
#
sub LoadConfig
{
    my($filename);
    my($line);
    my($MYCONFIGDIR, $MYUSERFILE);

    # First, read in our list of valid Unix pass-through commands.
    open(MYCONFIGDIR, "$CONFIG_DIR/pass-through.conf")
        || die("Failed to open file $CONFIG_DIR/pass-through.config for reading.");

    while(<MYCONFIGDIR>)
    {
        $filename = $_;
        chomp($filename);

        push(@external_commands, $filename);
    }

    close(MYCONFIGDIR);

    # The idea here is to go into the environment directory,
    # and pull in -all- files within that directory.
    opendir(MYCONFIGDIR, "$CONFIG_DIR/$environment")
        || die("Failed to open directory $CONFIG_DIR/$environment for reading.");

    while( $filename = readdir(MYCONFIGDIR) )
    {
        # Filter out . and .. -- we don't want those.
        if ( !($filename =~ /\./) && !($filename eq 'user') )
        {
            # Load the file in.
            open(MYFILE, "<$CONFIG_DIR/$environment/$filename")
                || die("Failed to open file $CONFIG_DIR/$environment/$filename for reading.");

            while(<MYFILE>)
            {
                $server = $_;
                chomp($server);

                open(MYUSERFILE, "<$CONFIG_DIR/$environment/user/$filename")
                    || die("Failed to open file $CONFIG_DIR/$environment/user/$filename for reading.");

                while(<MYUSERFILE>)
                {
                    $user = $_;
                    chomp($user);
                }

                close(MYUSERFILE);

                $line = "$user\@$server";

                if ( !getMatchingUserServer($server) )
                {
                    push(@{$groups_userservers_hash{'all'}}, $line);
                }

                push(@{$groups_userservers_hash{$filename}}, $line);
            }

            close(MYFILE);

            push(@server_groups, $filename);
        }
    }

    closedir(MYCONFIGDIR);

    push(@server_groups, 'all');
    @server_groups = sort(@server_groups);
}

#
# Simple validation logic.
#
sub isValidExternalCommand
{
    my($validate_me) = @_;
    my($command_str);

    foreach $command_str (@external_commands)
    {
        if ($validate_me eq $command_str)
        {
            return $TRUE;
        }
    }

    return $FALSE;
}

#
# Simple validation logic.
#
sub isValidInternalCommand
{
    my($validate_me) = @_;
    my($command_str);

    foreach $command_str (@internal_commands)
    {
        if ($validate_me eq $command_str)
        {
            return $TRUE;
        }
    }

    return $FALSE;
}

#
# Parse & execute the "copy" command.
#
sub ParseCopy
{
    # Validation TODO:
    # * Need a subroutine that will seperate the file element from the
    # the path element.
    #
    # Copy a local file to the current working server group,
    # with the remote path specified.
    # EXAMPLE: copy /tmp/test.out wlx
    # EXAMPLE: copy /tmp/test.out wlx01st
    if ( $input =~ /^copy (.*) ([0-9a-zA-z.]*)$/ )
    {
        if ( !stat($1) )
        {
             print("ERROR: Local file $1 is not accessible.\n");
        }

        print("ERROR: This syntax of the copy command is currently incomplete.\n");

        return;
    }

    # Copy from a local file to a specified server group or single server,
    # with remote path specified.
    # EXAMPLE: copy /tmp/test.out wlx:/usr/local/tmp/
    # EXAMPLE: copy /tmp/test.out wlx01st:/usr/local/tmp/
    if ( $input =~ /^copy (.*) ([0-9a-zA-z.]*):(.*\/)$/ )
    {
        if ( !stat($1) )
        {
            print("ERROR: Local file $1 is not accessible.\n");

            return;
        }

        # Check groups first, they get priority.
        if ( getMatchingGroup($2) )
        {
            print("Copy local file $1 to server group $2, remote directory $3?\n");

            if ( AreYouSure() )
            {
                foreach $userserver ( sort @{$groups_userservers_hash{$2}} )
                {
                    if ( PingUserServer($userserver) )
                    {
                        print("EXEC:  $SCP_BIN $1 $userserver:$3\n");

                        system("$SCP_BIN $1 $userserver:$3");
                    }
                }
            }
        }
        # If that fails, then check servers.
        elsif ( $userserver = getMatchingUserServer($2) )
        {
            print("Copy local file $1 to userserver $userserver, remote directory $3?\n");

            if ( AreYouSure() )
            {
                if ( PingUserServer($userserver) )
                {
                    print("EXEC:  $SCP_BIN $1 $userserver:$3\n");

                    system("$SCP_BIN $1 $userserver:$3");
                }
            }
        }
        else
        {
            # If no match, then print a sane error.
            print("ERROR: No server hostname or group matching '$temp_str' found.\n");
        }

    return;
    }

    # Copy a local file to the current working server group,
    # with the remote path specified.
    # EXAMPLE: copy /tmp/test.out /usr/local/tmp/
    if ( $input =~ /^copy (.*) (.*\/)$/ )
    {
        if ( !stat($1) )
        {
             print("ERROR: Local file $1 is not accessible.\n");

             return;
        }

        print("Copy local file $1 to server group $current_server_group, remote directory $2?\n");

        if ( AreYouSure() )
        {
            foreach $userserver ( sort @{$groups_userservers_hash{$current_server_group}} )
            {
                if ( PingUserServer($userserver) )
                {
                    print("EXEC:  $SCP_BIN $1 $userserver:$2\n");

                    system("$SCP_BIN $1 $userserver:$2");
                }
            }
        }

        return;
    }

    # Fall-through logic, invalid syntax error.
    print("ERROR: Invalid copy command syntax.\n");
    print("ERROR: Did you end your remote path with a slash?\n");
}

#
# Parse & execute the "run" command.
#
# TODO: run "uptime" on wlx01st,wlx02st,wlx05st
#       run "uptime" on wlx concurrent 5
#       run "uptime" on wlx log
#       run "uptime" on wlx concurrent 5 log
#
sub ParseRun
{
    # Run command on local host
    # EXAMPLE: run "uptime" local
    if ( $input =~ /^run (\".*\") local$/ )
    {
        RunCommandLocal($1);

        return;
    }

    # Run command on current server group.
    # EXAMPLE: run "uptime"
    if ($input =~ /^run (\".*\")$/)
    {
        print("Run $1 on server group $current_server_group?\n");
        
        if ( AreYouSure() )
        {
            foreach $userserver ( sort @{$groups_userservers_hash{$current_server_group}} )
            {
                RunCommandRemote($userserver,$1);
            }
        }

        return;
    }

    # Run command on a specific server or group.
    # EXAMPLE: run "uptime" wlx
    # EXAMPLE: run "uptime" wlx01st
    if ( $input =~ /^run (\".*\") ([a-zA-z0-9.]*)$/ )
    {
        # Check groups first, they get priority.
        if ( getMatchingGroup($2) )
        {
            print("Run $1 on server group $2?\n");

            if ( AreYouSure() )
            {
                foreach $userserver ( sort @{$groups_userservers_hash{$2}} )
                {
                    RunCommandRemote($userserver,$1);
                }
            }
        }
        # If that fails, then check servers.
        elsif ( $userserver = getMatchingUserServer($2) )
        {
            print("Run $1 on userserver $userserver?\n");

            if ( AreYouSure() )
            {
                RunCommandRemote($userserver,$1);
            }
        }
        else
        {
            # If no match, then print a sane error.
            print("ERROR: No server hostname or group matching '$2' found.\n");
        }

        return;
    }

    # Fall-through logic, invalid syntax error.
    print("ERROR: Invalid run command syntax.\n");
}

#
# Ping each server before we attempt to run remote commands on it.
#
sub PingUserServer
{
    my($userserver) = @_;
    my($pinger);

    if ($noping_arg)
    {
        return $TRUE;
    }
    else
    {
        $pinger = Net::Ping->new("tcp", 22);

        $userserver =~ /(\w*)\@([0-9a-zA-z.]*)/;

        if ($pinger->ping($2))
        {
            return $TRUE;
        }
        else
        {
            print("ERROR: Host $2 appears to be down.\n");

            return $FALSE;
        }
    }
}

#
# Print the help file.
#
sub PrintHelpFile
{
    my ($filename) = @_;

    open(MYFILE, "<$HOME_DIR/doc/$filename") ||
        return($FALSE);

    print "\n";

    while(<MYFILE>)
    {
        print($_);
    }

    close(MYFILE);

    print "\n";

    return($TRUE);
}

#
# Run a command locally.
#
sub RunCommandLocal
{
    my($local_command) = @_;
    my(@command_output, $output_line);

    print "EXEC:  $local_command\n";

    @command_output = qx/$local_command 2>&1/;

    foreach $output_line (@command_output)
    {
        chomp($output_line);
        print "$output_line\n";
    }

    if ($? != 0)
    {
        print("ERROR: Local shell returned error state.\n");
    }
}

#
# Run a command remotely.
#
sub RunCommandRemote
{
    my($remote_userserver, $remote_command) = @_;
    my(@command_output, $output_line);
    my($exec_line);

    if ( PingUserServer($remote_userserver) )
    {
        $exec_line = "$SSH_BIN $remote_userserver $remote_command";

        print "EXEC:  $exec_line\n";

        @command_output = qx/$exec_line 2>&1/;

        foreach $output_line (@command_output)
        {
            chomp($output_line);
            print "$output_line\n";
        }

        if ($? != 0)
        {
            print("ERROR: Remote shell returned error state.\n");
        }
    }
}

#
# Validate incoming arguments.  Dump user out if in error.
#
# This really needs some more work...
#
sub ValidateArgs
{
    if ($env_arg)
    {
        # Validate arguments.
        if ( !stat("$CONFIG_DIR/$env_arg") )
        {
            die("Directory for environment $env_arg doesn't exist!");
        }

        $environment = $env_arg;
    }
    else
    {
        die('Invalid arguments given.  See --help for required flags.');
    }
}

__END__
######################################################################
# Start POD Text

=head1 NAME

B<distribulator.pl> - Remote command execution and file transfer utility.

=head1 SYNOPSIS

B<distribulator.pl> --env=I<environment>

=head1 DESCRIPTION

The Distribulator is a distributed remote command execution and file transfer
tool written in Perl. If you have command execution priviledges on more than
10 Unix boxes in one domain this tool might be for you!

=head1 OPTIONS

=over 3

=item *

B<--env>=I<environment>

=over 3

Specifies which environment this session will be limited to.
NOTE: This is a required option.

=back

=item *

B<--noping>

=over 3

Indicates that we do not wish to "Ping" servers before talking
to them via our remote shell.  This is handy when the local version
of Net::Ping is broken, or firewalls are blocking us, etc.

=back

=item *

B<--shell>=[ I<nsh> | I<ssh> ]

=over 3

Specifies whether to use ssh or some other remote shell,
such as BladeLogic's NetShell product.

=back

=item *

B<--version>

=over 3

Displays version information and exits.

=back

=back

=head1 AUTHORS

=over 3

Adam W. Dace <adace@orbitz.com>

=back

=cut

# End POD Text
######################################################################

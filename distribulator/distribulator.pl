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
my($env_arg, $help_arg, $shell_arg, $version_arg) = '';
my(@command_tokens);
my($remote_command);
my($server);
my($temp_str);
my($user);
my($MYFILE);

#
# State Tracking Variables
my($current_server_group) = 'wlx';
my($environment);
my(@server_groups);
my(%users_groups_hash);
my(%servers_groups_hash);
my(@valid_commands) = ( 'copy', 'exit', 'group', 'help', 'run', 'shell' );

GetOptions("env=s" => \$env_arg,
           "help" => \$help_arg,
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
# Check for --version
#
if ($version_arg)
{
    print("\n");
    print("The Distribulator v0.1\n");
    print("\n");
    print("(c) Copyright 2002 Adam W. Dace.\n");
    print("The Distribulator may be copied only under the terms of the BSD License,\n");
    print("a copy of which can be found with The Distribulator distribution kit.\n");
    print("\n");
    print("Specify the --help option for further information about The Distribulator.\n");
    print("\n");

    exit(0);
}
#
# Give the user a banner, no matter what.
#
print("\n");
print("The Distribulator v0.1\n");
print("----------------------\n");
print("\n");
#
# Validate our command-line arguments.
#
ValidateArgs();
#
# Load server group configuration from appropriate files.
#
LoadConfig();
#
# Should I use Text::ParseWords to parse?  On maybe just split?
#
# Auto-detection Magic.
#
my($user) = getlogin() || getpwuid($<);
my($dir) = cwd();
my($hostname) = Sys::Hostname::hostname();
#
# Variable Definitions
#
my($command);
my($input);
my($prompt);
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
print("Available Server Groups: @server_groups\n");
print("\n");
print("Prompt Description:      <user\@environment[current_server_group]:local_dir>\n");
print("\n");
#
# The Never Ending Loop...
#
while ($TRUE)
{
	$command = '';
	$prompt = "<$user\@$environment\[$current_server_group\]:$dir> ";
	$input = $term->readline($prompt);

	@command_tokens = split(' ', $input);
	$command = shift(@command_tokens);

    # If the command isn't found in the array.
    if (!isValidCommand($command))
    {
		print("ERROR: Unknown Command: $command\n");

        next;
    }

    #################### IMPLEMENTED ####################

    # Exit
    if ( ($command eq 'exit') )
	{
		print "Received exit command.  See ya later!\n\n";

		exit(0);
	}

	#
	# Idea -- We should create a hashtable of command name and
	# maximum number of args, would be good for validation.
	#
	# How do we see if the user hit CTRL-D?
	#
	# Group
	if ($command eq 'group')
	{
		$temp_str = shift(@command_tokens);

        if ( !$temp_str )
        {
            print("ERROR: No server group given.\n");
        }
		elsif ( $servers_groups_hash{$temp_str} )
		{
			$current_server_group = $temp_str;
			print("NOTE:  Current server group now is '$current_server_group'.\n");
		}
		else
		{
			print("ERROR: Unknown server group $temp_str.\n");
		}
	}

	# Help
	if ($command eq 'help')
	{
		$temp_str = shift(@command_tokens);

        # If the next argument is a valid command, show help for it.
		if ( isValidCommand($temp_str) )
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
	}

	# Run
	if ($command eq 'run')
	{
        ParseRun();
	}

    #################### NOT IMPLEMENTED ####################

    if ($command eq 'copy' || $command eq 'shell')
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
# Lookup which group this server belongs to.
#
sub getServerGroup
{
    my($find_server) = @_;
    my($group, $group_server);

    foreach $group (sort keys(%servers_groups_hash) )
    {
        foreach $group_server ( @{$servers_groups_hash{$group}} )
        {
            if ($find_server eq $group_server)
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

    return $users_groups_hash{$group};
}

#
# Load server group configuration from files.
#
sub LoadConfig
{
    my($MYDIR);
    my($filename);
	my($line);

    # The idea here is to go into the environment directory,
    # and pull in -all- files within that directory.
    opendir(MYDIR, "$CONFIG_DIR/$environment")
        || die("Failed to open directory $CONFIG_DIR/$environment for reading.");

    while( $filename = readdir(MYDIR) )
    {
        # Filter out . and .. -- we don't want those.
        if ( !($filename =~ /\./) && !($filename eq 'user') )
        {
            # Load the file in.
            open(MYFILE, "<$CONFIG_DIR/$environment/$filename")
                || die("Failed to open file $CONFIG_DIR/$environment/$filename for reading.");

            while(<MYFILE>)
            {
                $line = $_;
                chomp($line);

                push(@{$servers_groups_hash{$filename}}, $line);
            }

            close(MYFILE);

            push(@server_groups, $filename);
        }
    }

    closedir(MYDIR);

    @server_groups = sort(@server_groups);

    # The idea here is to go into the environment/user directory,
    # and pull in -all- files within that directory.
    opendir(MYDIR, "$CONFIG_DIR/$environment/user")
        || die("Failed to open directory $CONFIG_DIR/$environment/user for reading.");

    while( $filename = readdir(MYDIR) )
    {
        # Filter out . and .. -- we don't want those.
        if ( !($filename =~ /\./) )
        {
            # Load the file in.
            open(MYFILE, "<$CONFIG_DIR/$environment/user/$filename")
                || die("Failed to open file $CONFIG_DIR/$environment/user/$filename for reading.");

            while(<MYFILE>)
            {
                $line = $_;
                chomp($line);

                $users_groups_hash{$filename} = $line;
            }

            close(MYFILE);
        }
    }

    closedir(MYDIR);

######################################################################
#    foreach my $group (sort keys(%servers_groups_hash) )
#    {
#        print("Group: $group\n");
#
#        foreach my $server ( @{$servers_groups_hash{$group}} )
#        {
#            print("     Server: $server\n");
#        }
#    }
#
#    print ("----------\n");
#
#    foreach my $group (sort keys(%users_groups_hash) )
#    {
#        print("Group: $group\n");
#        print ("     User: " .
#               $users_groups_hash{$group} .
#               "\n");
#    }
#
######################################################################

}

#
# Simple validation logic.
#
sub isValidCommand
{
    my($validate_me) = @_;
    my($command_str);

    foreach $command_str (@valid_commands)
    {
        if ($validate_me eq $command_str)
        {
            return $TRUE;
        }
    }

    return $FALSE;
}

sub isValidServer
{
    return $TRUE;
}

#
# Parse & execute the "run" command.
#
sub ParseRun
{
    # Run command on server group
    if ( $input =~ /^run (\".*\") on group (.*)/ )
    {
        # Parsing logic.
        print("Run $1 on $2 server group?\n");

        # Validate Me!
        if ( AreYouSure() )
        {
            foreach my $server ( @{$servers_groups_hash{$2}} )
            {
                RunCommandRemote($server,$1);
            }
        }
    }
    # Run command on server host
    if ($input =~ /^run (\".*\") on server (.*)/)
    {
        # Parsing logic.
        print("Run $1 on $2 server?\n");
        
        # Validate Me!
        if ( AreYouSure() )
        {
            RunCommandRemote($server,$1);
        }
    }
    # Run command on current group.
    elsif ($input =~ /^run (\".*\")/)
    {
        print("Run $1 on server group $current_server_group?\n");
        
        if ( AreYouSure() )
        {
            foreach $server ( @{$servers_groups_hash{$current_server_group}} )
            {
                RunCommandRemote($server,$1);
            }
        }
    }
    # Invalid syntax.
    else
    {
        print("ERROR: Invalid run command syntax.\n");
    }
}

#
# Ping each server before we attempt to run remote commands on it.
#
sub PingServer
{
    my($host) = @_;
    my($pinger);

    $pinger = Net::Ping->new("tcp", 22);

    if ($pinger->ping($host))
    {
        return $TRUE;
    }
    else
    {
        print("ERROR: Host $host appears to be down.\n");

        return $FALSE;
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
# Run a command remotely.
#
sub RunCommandRemote
{
    my($remote_server, $remote_command) = @_;
    my(@command_output, $output_line);
    my($exec_line);

    if ( PingServer($remote_server) )
    {
        # Super magic.
        $exec_line = "ssh " .
            getServerUser($remote_server) .
                "\@$remote_server $remote_command";

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

B<distribulator.pl> - The Distribulator.

=head1 SYNOPSIS

B<distribulator.pl> [ I<options> ] I<argument>

=head1 DESCRIPTION

The Distribulator is a distributed remote command execution and file transfer
tool written in Perl. If you have command execution priviledges on more than
10 Unix boxes in one domain this tool might be for you!

=head1 OPTIONS

=over 3

=item *

B<--env>
Specifies which environment this session will be limited to.

=item *

B<--help>
Displays this manual page and exits.

=item *

B<--shell>
Specifies whether to use ssh or some other remote shell,
such as BladeLogic's NetShell product.

=item *

B<--version>
Displays version information and exits.

=back

=head1 AUTHORS

=over 3

Adam W. Dace <adace@orbitz.com>

=back

=cut

# End POD Text
######################################################################
#!/usr/local/bin/perl
######################################################################
# $Id$
#
# Name: distribulator.pl
#
# Description: The Distribulator.  A detail description can be found
# in the README file in the above directory(..).
#
######################################################################
#
# Force unbuffered output.
#
$|=1;

#
# * Enforce strict conventions.
# * Command-line Options Module
# * Perl Documentation Module
#
use strict;
use Cwd;
use Getopt::Long;
use Pod::Usage;
use Sys::Hostname;
use Term::ReadLine;
#
# Constant Variables (Fix Me!)
#
my($CONF_DIR) = '/usr/local/ops/environ';
my($FALSE) = 0;
my($TRUE) = 1;
#
# Runtime Arg/Temp Variables
#
my($config_arg, $env_arg, $help_arg, $shell_arg, $version_arg) = '';
my(@command_tokens);
my($error_state);
my($remote_command);
my($server);
my($temp_str);
my($MYFILE);

#
# State Tracking Variables
my($current_server_group) = 'wlx';
my($environment);
my(@server_groups);
my(%servers_groups_hash);
my(@valid_commands) = ( 'copy', 'exit', 'group', 'help', 'run', 'shell' );

GetOptions("config=s" => \$config_arg,
           "env=s" => \$env_arg,
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
print("\n");
print("Your Client Host:         $hostname\n");
print("Your Current Environment: $environment\n");
print("\n");
print("Prompt Description -- <user\@environment[current_server_group]:local_dir>\n");
print("\n");
#
# The Never Ending Loop...
#
while ($TRUE)
{
	$command = '';
	$error_state = $TRUE;
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
		$error_state = $FALSE;
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
		$error_state = $FALSE;
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
					print("ssh $server $1\n");
				}
			}
            else
            {
                print "Okay, NOT running the command.\n";
            }

			$error_state = $FALSE;
		}
        # Run command on server host
        if ($input =~ /^run (\".*\") on server (.*)/)
        {
            # Parsing logic.
            print("Run $1 on $2 server?\n");

			# Validate Me!
            if ( AreYouSure() )
            {
                print("ssh $2 $1\n");
            }
            else
            {
                print "Okay, NOT running the command.\n";
            }

			$error_state = $FALSE;
        }
		# Run command on current group.
		elsif ($input =~ /^run (\".*\")/)
		{
			print("Run $1 on server group $current_server_group?\n");

			if ( AreYouSure() )
			{
				foreach $server ( @{$servers_groups_hash{$current_server_group}} )
				{
					print("ssh $server $1\n");
				}
			}
			else
			{
				print "Okay, NOT running the command.\n";
			}

			$error_state = $FALSE;
		}
		# Invalid syntax.
		else
		{
			print("ERROR: Invalid syntax.\n");
		}
	}

    #################### NOT IMPLEMENTED ####################

    if ($command eq 'copy' || $command eq 'shell')
    {
		$error_state = $FALSE;
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
		return $FALSE;
	}
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
    opendir(MYDIR, "$CONF_DIR/$environment")
        || die("Failed to open directory $CONF_DIR/$environment for reading.");

    while( $filename = readdir(MYDIR) )
    {
        # Filter out . and .. -- we don't want those.
        if ( !($filename =~ /\./) )
        {
            # Load the file in.
            open(MYFILE, "<$CONF_DIR/$environment/$filename")
                || die("Failed to open file $CONF_DIR/$environment/$filename for reading.");

            print("Loading hostnames for $filename server group...");

            while(<MYFILE>)
            {
                $line = $_;

                chomp($line);
                push(@{$servers_groups_hash{$filename}}, $line);
            }

            close(MYFILE);

	    push(@server_groups, $filename);

            print "Done.\n";
        }
    }

    closedir(MYDIR);

    print("\n");

    # Debug / summary
    print("Known Server Groups: @server_groups\n");

    foreach my $group (sort keys(%servers_groups_hash) )
    {
        print("Group: $group\n");

        foreach my $server ( @{$servers_groups_hash{$group}} )
        {
            print("     Server: $server\n");
        }
    }
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

#
# Ping each server before we attempt to run remote commands on it.
#
sub PingServer
{
#    use Net::Ping;

	return($TRUE);
}

#
# Print the help file.
#
sub PrintHelpFile
{
	my ($filename) = @_;

    open(MYFILE, "<./doc/$filename") ||
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
# Validate incoming arguments.  Dump user out if in error.
#
sub ValidateArgs
{
    if ($env_arg)
    {
        # Validate arguments.
        if ( !stat("$CONF_DIR/$env_arg") )
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

#$group_servers{$current_group} = \@server_array;
#foreach my $id (sort keys(%to_run) ) {
#        print "$id\n";
#        foreach my $machine (@{$to_run{$id}}) {
#          $remote_file =~ s/\/$//g;
#          my $command = "$ssh $id\@$machine \"$remote_command\"";
#          print "Running: $command\n";                             
#          system("$command");
#        }
#}

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

B<--config>
Allows people to manually specify where our configuration lives.

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

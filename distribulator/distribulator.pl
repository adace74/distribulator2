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
#
# Runtime Variables
#
my($config_arg, $env_arg, $help_arg, $shell_arg, $version_arg) = '';
my(@command_tokens);
my($command_tokens_count);
my($current_group) = 'wlx';
my(@current_servers);
my($environment);
my($remote_command);
my($server);
my($MYFILE);

my(%servers_groups_hash);

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
    print "\n";
    print "The Distribulator v0.1\n";
    print "\n";
    print "(c) Copyright 2002 Adam W. Dace.\n";
    print "The Distribulator may be copied only under the terms of the BSD License,\n";
    print "a copy of which can be found with The Distribulator distribution kit.\n";
    print "\n";
    print "Specify the --help option for further information about The Distribulator.\n";
    print "\n";

    exit(0);
}
#
# Give the user a banner, no matter what.
#
print "\n";
print "The Distribulator v0.1\n";
print "----------------------\n";
print "\n";
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
print "\n";
print "You Are On Server               : $hostname\n";
print "You Can Run Distributed Stuff In: $environment\n";
print "\n";
print "Prompt Description -- <user\@environment[current_group]:local_dir>\n";
print "\n";
#
# The Never Ending Loop...
#
while (true)
{
	$command = '';
	$prompt = "<$user\@$environment\[$current_group\]:$dir> ";
	$input = $term->readline($prompt);

	# Argh, how to detect CTRL-D?
	if ( ($input eq 'exit') || ($input eq 'quit') )
	{
		print "Received exit/quit command.  See ya later!\n\n";

		exit(0);
	}

	@command_tokens = split(' ', $input);
	$command_tokens_count = scalar @command_tokens;

	$command = shift(@command_tokens);

	print "Input:          $input\n";
	print "Command Tokens: @command_tokens\n";
	print "Token Count:    $command_tokens_count\n";
	print "Command:        $command\n";
	#
	# Idea -- We should create a hashtable of command name and
	# maximum number of args, would be good for validation.
	#
	# How do we see if the user hit CTRL-D?
	#
	if ($command eq 'group')
	{
		$current_group = shift(@command_tokens);
	}
    elsif ($command eq 'help')
    {
        PrintHelpFile();
    }
	elsif ($command eq 'run')
	{
		$remote_command = join(' ', @command_tokens);

		print "Run $remote_command on server group $current_group?\n";

		if ( $term->readline("Yes / No> ") =~ /^[Yy]/ )
		{
			print "Want to run it!\n";

			foreach $server (@current_servers)
			{
				print "ssh $server $remote_command\n";
			}
		}
		else
		{
			print "Okay, not running the command.\n";
		}

		#RunCommandRemote($remote_command, $current_group);
	}
	else
	{
		print "ERROR: Unknown Command: $command\n";
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

            print "Loading hostnames for $filename server group...";

            while(<MYFILE>)
            {
                $line = $_;

                chomp($line);
                push(@{$servers_groups_hash{$filename}}, $line);
            }

            close(MYFILE);

            print "Done.\n";
        }
    }

    closedir(MYDIR);

    print "\n";

    foreach my $group (sort keys(%servers_groups_hash) )
    {
        print "Group: $group\n";

        foreach my $server ( @{$servers_groups_hash{$group}} )
        {
            print "     Server: $server\n";
        }
    }
}

#
# Ping each server before we attempt to run remote commands on it.
#
sub PingServer
{
#    use Net::Ping;

	return 1;
}

#
# Print the help file.
#
sub PrintHelpFile
{
        print "\n";

        open(MYFILE, "<./doc/help.txt") ||
            die("Cannot find the help file in ./doc!");

        while(<MYFILE>)
        {
            print $_;
        }

        close(MYFILE);

        print "\n";
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
        die ('Invalid arguments given.  See --help for required flags.');
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

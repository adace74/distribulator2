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
# Standard Perl Modules:
# 
# * Enforce strict conventions.
# * Current working directory Module
# * Command-line Options Module
# * ICMP ping Module
# * Perl documentation Module
# * Unix hostname Module
# * GNU::Term::ReadLine Module
#
use strict;
use Cwd;
use Getopt::Long;
use Net::Ping;
use Pod::Usage;
use Sys::Hostname;
use Term::ReadLine;

#
# Custom Perl Modules:
# * Global configuration.
# * Command execution.
# * Command parsing.
# * Server tracking.
#
use Global::Config;
use Global::Run;
use Parse::Commands;
use Parse::Servers;

#
# Arg Temp Storage
#
my($env_arg, $help_arg, $shell_arg, $version_arg) = '';

#
# Generic Temp Storage
#
my($command,@command_tokens);
my($flag,$input,$server,$server_user_temp,$temp_str,$user);

#
# Prompt-related Storage
#
my($prompt_env, $prompt_hostname, $promp_user);

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
# Give the user a banner, no matter what.
#
print("\n");
print("The Distribulator v0.47\n");
print("-----------------------\n");
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
# Load Command & Server Group Configuration.
#
LoadCommands();
LoadServers("$CONFIG_DIR/$prompt_env");
#
# Find out where our binaries are located.
#
getBinaryLocations();
#
# Preparing to launch the shell.
#
my($prompt_user) = getlogin() || getpwuid($<);
my($prompt_hostname) = Sys::Hostname::hostname();
#
# Setup signal handler for SIGINT.
#
$SIG{INT} = \&catchSignal;
#
# Setup ReadLine for input...
#
my($term) = getNewReadLineTerm();

#
# Print a little intro.
#
print("GNU Readline Version:     " . getReadLineVersion() . "\n");
print("Local Install Dir:        $INSTALL_DIR\n");
print("Local Config Dir:         $CONFIG_DIR\n");
print("Local Host:               $prompt_hostname\n");
print("Current Environment:      $prompt_env\n");
print("\n");
print("Internal Commands Loaded: " . scalar (@internal_commands) . "\n");
print("External Commands Loaded: " . scalar (@external_commands) . "\n");
print("Available Server Groups:  @server_groups\n");
print("\n");
print("Prompt Description:       <user\@environment[current_server_group]:local_dir>\n");
print("\n");
print("Confused?  Need help?  Try typing \'help\' and see what happens!\n");
print("\n");

#
# The Never Ending Loop...
#
while ($TRUE)
{
    # Setting up our state.
    $command = '';
    setReadLinePrompt("<$prompt_user\@$prompt_env\[wlx\]:" .
        cwd() . "> ");

    $input = $term->readline( getReadLinePrompt() );

    setUserAborting($FALSE);

    # Parsing magic.
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

    # Command: copy
    if ($command eq 'copy')
    {
        ParseCopy($input);

        next;
    }

    # Command: exit
    if ( ($command eq 'exit') )
    {
        ResetTermAndExit();
    }

    # Command: help
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

    # Command: login
    if ($command eq 'login')
    {
        ParseLogin(@command_tokens);

        next;
    }

    # Command: server-group
    if ($command eq 'server-group')
    {
        ParseServerGroup(@command_tokens);

        next;
    }

    # Command: server-list
    if ($command eq 'server-list')
    {
        ParseServerList(@command_tokens);

        next;
    }

    # Command: run
    if ($command eq 'run')
    {
        ParseRun($input);

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
# Catch signals.
#
sub catchSignal
{
    print("\n");

    # Trying to have ReadLine hit the reset button.
    $term->initialize();
    $term->redisplay();

    # Internal flag to try and stop runaway commands.
    setUserAborting($TRUE);
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

        $prompt_env = $env_arg;
    }
    else
    {
        print("Invalid arguments given.\n");
        die('See --help for required flags.');
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

#
# $Id$
#
######################################################################
#
# Name: Commands.pm
#
# Description:  Perl module containing command-parsing functionality.
#
######################################################################

#
# Package definition
#
package Parse::Commands;

#
# Required Perl Modules
#
# * Enforce strict conventions.
# * Export Subroutines Module
#
use strict;
use Exporter;

#
# Custom Perl Modules
#
# * Global Configuration
#
use Global::Config;
use Global::Run;
use Parse::Servers;

######################################################################
#
# Exporter Setup
#
use vars qw(@ISA @EXPORT @EXPORT_OK);
@ISA = qw(Exporter);

BEGIN
{
    # Initialize subroutines immediately so their contents
    # can be used in the 'use vars' below.
    @EXPORT = qw(@external_commands @internal_commands
                 &isUserAborting &setUserAborting
                 &isValidExternalCommand &isValidInternalCommand
                 &LoadCommands &ParseCopy &ParseLogin &ParseRun
                 &ParseServerGroup &ParseServerList
                 &PrintHelpFile);
    @EXPORT_OK = qw();
}

# User visible variables.
use vars @EXPORT, @EXPORT_OK;
######################################################################

#
# Hard-coded, icky icky.
#
@external_commands = ( 'ls' );
@internal_commands = ( 'cd', 'copy', 'exit', 'help', 'login',
                       'remote-shell', 'run', 'server-group',
                       'server-list' );

# Attempt to do state-tracking for cancelled commands.
my($user_aborting) = $FALSE;

######################################################################
# Initialization & Functionality
######################################################################

sub AreYouSure
{
    my($term) = getReadLineTerm();

    if ( $term->readline("Yes / No> ") =~ /^[Yy]/ )
    {
        $term->set_prompt( getReadLinePrompt() );

        return $TRUE;
    }
    else
    {
        print "Okay, NOT running the command.\n";

        return $FALSE;
    }
}

sub LoadCommands
{
    my($MYFILE, $filename);

    # First, read in our list of valid Unix pass-through commands.
    open(MYFILE, "$CONFIG_DIR/pass-through.conf")
        || die("Failed to open file $CONFIG_DIR/pass-through.config for reading.");

    while(<MYFILE>)
    {
        $filename = $_;
        chomp($filename);

        push(@external_commands, $filename);
    }

    close(MYFILE);
}

#
# Print the help file.
#
sub PrintHelpFile
{
    my ($filename) = @_;

    open(MYFILE, "<$INSTALL_DIR/doc/$filename") ||
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

######################################################################
# Validation.
######################################################################

#
# Set user_aborting variable.
#
sub setUserAborting
{
    # Variable Scope Hack -- Not Sure Why?
    my($TempVar) = shift(@_);

    $user_aborting = $TempVar;
}

#
# Get user_aborting variable.
#
sub isUserAborting
{
    if ($user_aborting)
    {
        return $TRUE;
    }
    else
    {
        return $FALSE;
    }
}

#
# Simple validation logic.
#
sub isValidExternalCommand
{
    my($validate_me) = shift(@_);
    my($command_str);

    foreach $command_str (@external_commands)
    {
        if ($validate_me eq $command_str)
        {
            return($TRUE);
        }
    }

    return($FALSE);
}

#
# Simple validation logic.
#
sub isValidInternalCommand
{
    my($validate_me) = shift(@_);
    my($command_str);

    foreach $command_str (@internal_commands)
    {
        if ($validate_me eq $command_str)
        {
            return($TRUE);
        }
    }

    return($FALSE);
}

######################################################################
# Parsing & exeuction functionality.
######################################################################

#
# Parse & execute the "copy" command.
#
sub ParseCopy
{
    my($input) = shift(@_);

    my($copy_server, $copy_user);

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

             return;
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
                foreach $copy_server ( @{$groups_servers_hash{$2}} )
                {
                    if ( PingServer($copy_server) )
                    {
                        $copy_user = getServerUser($copy_server);

                        RunCommandLocal("$SCP_BIN $1 $copy_user\@$copy_server:$3");
                    }
                }
            }
        }
        # If that fails, then check servers.
        elsif ( $copy_server = getMatchingServer($2) )
        {
            print("Copy local file $1 to server $copy_server, remote directory $3?\n");

            if ( AreYouSure() )
            {
                if ( PingServer($copy_server) )
                {
                    $copy_user = getServerUser($copy_server);

                    RunCommandLocal("$SCP_BIN $1 $copy_user\@$copy_server:$3");
                }
            }
        }
        else
        {
            # If no match, then print a sane error.
            print("ERROR: No server hostname or group matching '$2' found.\n");
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
            foreach $copy_server ( @{$groups_servers_hash{$current_server_group}} )
            {
                if ( PingServer($copy_server) )
                {
                    $copy_user = getServerUser($copy_server);

                    RunCommandLocal("$SCP_BIN $1 $copy_user\@$copy_server:$2");
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
# Parse & execute the "login" command.
#
sub ParseLogin
{
    my(@command_tokens) = @_;
    my($partial) = shift(@command_tokens);
    my($exec_str, $login_server, $found_user);

    print("Attempt to match |$partial|\n");

    if ( $login_server = getMatchingServer($partial) )
    {
        if ( PingServer($login_server) )
        {
            $found_user = getServerUser($login_server);

            $exec_str = "$SSH_BIN -l $found_user $login_server";
            
            RunCommandLocal($exec_str);
        }
    }
    else
    {
        print("ERROR: No server hostname matching '$partial' found.\n");
    }
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
    my($input) = shift(@_);

    my($run_server);

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
            foreach $run_server ( getServerList($current_server_group) )
            {
                if ( !isUserAborting() )
                {
                    RunCommandRemote($run_server,$1);

                    # Sleep 1/4 second.
                    sleep(0.25);
                }
                else
                {
                    print("NOTE:  CTRL-C detected, aborting command.\n");
                    setUserAborting($FALSE);
                    last;
                }
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
                foreach $run_server ( getServerList($2) )
                {
                    if ( !isUserAborting() )
                    {
                        RunCommandRemote($run_server,$1);

                        # Sleep 1/4 second.
                        sleep(0.25);
                    }
                    else
                    {
                        print("NOTE:  CTRL-C detected, aborting command.\n");
                        setUserAborting($FALSE);
                        last;
                    }
                }
            }
        }
        # If that fails, then check servers.
        elsif ( $run_server = getMatchingServer($2) )
        {
            print("Run $1 on server $run_server?\n");

            if ( AreYouSure() )
            {
                RunCommandRemote($run_server,$1);
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
# Parse & execute the "server-group" command.
#
sub ParseServerGroup
{
    my(@command_tokens) = @_;

    my($server_group) = shift(@command_tokens);

    if ( !$server_group )
    {
        print("ERROR: No server group given.\n");
    }
    elsif ( $groups_servers_hash{$server_group} )
    {
        $current_server_group = $server_group;

        print("NOTE:  Current server group now is '$current_server_group'.\n");
    }
    else
    {
        print("ERROR: Unknown server group '$server_group'.\n");
    }
}

#
# Parse & execute the "server-list" command.
#
sub ParseServerList
{
    my($server_group) = shift(@_);
    my($server_user_temp, @server_list);

    # If there's no target, list the current server group.
    if ( !$server_group )
    {
        print("Known servers in group $current_server_group:\n");
        print("---------------------------------\n");

        @server_list = getServerList($current_server_group);

        foreach $server_user_temp ( @server_list )
        {
            print("$server_user_temp\n");
        }
    }
    elsif ( $groups_servers_hash{$server_group} )
    {
        print("Known servers in group $server_group:\n");
        print("---------------------------------\n");

        @server_list = getServerList($server_group);

        foreach $server_user_temp ( @server_list )
        {
            print("$server_user_temp\n");
        }
    }
    else
    {
        print("ERROR: No server group matching '$server_group' found.\n");
    }
}

######################################################################
#
# Let the loading script know we've loaded successfully.
#
return($TRUE);

#
# $Id$
#
######################################################################
#
# Name: Run.pm
#
# Description:  Perl module containing global configuration information
# such as where specific binaries live.
#
######################################################################

#
# Package definition
#
package Global::Run;

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
# * 
#
use Global::Config;
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
    @EXPORT = qw(&RunCommandLocal &RunCommandRemote
                 &PingServer);
    @EXPORT_OK = qw();
}

# User visible variables.
use vars @EXPORT, @EXPORT_OK;
######################################################################

#
# Handy constants
#
my($TRUE) = 1;
my($FALSE) = 0;

#
# State Tracking Variables
#
$current_server_group = 'wlx';
%groups_servers_hash;

#
# Misc. Variables
#
my($flag, $group, $server, $sub_string, $user);
my(@server_user);
my($server_user_temp);

######################################################################
# Various Functionality
######################################################################

#
# Run a command locally.
#
sub RunCommandLocal
{
    my($local_command) = @_;
    my(@command_output, $output_line);

    print "EXEC:  $local_command\n";

    system($local_command);

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
    my($remote_server, $remote_command) = @_;
    my(@command_output, $exec_line, $output_line, $remote_user);

    if ( PingServer($remote_server) )
    {
        $remote_user = getServerUser($remote_server);

        $exec_line = "$SSH_BIN -l $remote_user $remote_server $remote_command";

        print "EXEC:  $exec_line\n";

        system($exec_line);

        if ($? != 0)
        {
            print("ERROR: Remote shell returned error state.\n");
        }
    }
}

#
# Ping each server before we attempt to run remote commands on it.
#
sub PingServer
{
    my($ping_server) = @_;
    my($pinger);

    # Setup Net::Ping to do a TCP-level ping to remote port 22,
    # with a 2 second timeout.
    $pinger = Net::Ping->new("tcp", 2);
	$pinger->{port_num} = 22;

    if ( $pinger->ping($ping_server) )
    {
        $pinger->close();
        
        return $TRUE;
    }
    else
    {
        $pinger->close();
        
        print("ERROR: Host $ping_server appears to be down.\n");
        
        return $FALSE;
    }
}

#
# Let the loading script know we've loaded successfully.
#
return($TRUE);

#
# $Id$
#
######################################################################
#
# Name: Servers.pm
#
# Description:  Perl module containing global configuration information
# such as where specific binaries live.
#
######################################################################

#
# Package definition
#
package Parse::Servers;

#
# Required Perl Modules
#
# * Enforce strict conventions.
# * Export Subroutines Module
#
use strict;
use Exporter;

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
    @EXPORT = qw($current_server_group @server_groups
                 %groups_servers_hash
                 &LoadServers
                 &getMatchingGroup &getMatchingServer
                 &getServerGroup &getServerUser);
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

my($flag, $group, $server, $sub_string, $user);
my(@server_user);
my($server_user_temp);

######################################################################
# Various Startup Subroutines
######################################################################

sub LoadServers
{
    my($env_dir) = @_;

    my($MYDIR, $MYSERVERFILE, $MYUSERFILE);
    my($filename);

    # The idea here is to go into the environment directory,
    # and pull in -all- files within that directory.
    opendir(MYDIR, $env_dir)
        || die("Failed to open directory $env_dir for reading.");

    while( $filename = readdir(MYDIR) )
    {
        # Filter out . and .. -- we don't want those.
        if ( !($filename =~ /\./) && !($filename eq 'user') )
        {
            # Load the file in.
            open(MYSERVERFILE, "<$env_dir/$filename")
                || die("Failed to open file $env_dir/$filename for reading.");

            while(<MYSERVERFILE>)
            {
                $server = $_;
                chomp($server);

                open(MYUSERFILE, "<$env_dir/user/$filename")
                    || die("Failed to open file $env_dir/user/$filename for reading.");

                while(<MYUSERFILE>)
                {
                    $user = $_;
                    chomp($user);
                }

                close(MYUSERFILE);

                @server_user = ( $server, $user );

                if ( !getMatchingServer($server) )
                {
                    push(@{$groups_servers_hash{'all'}}, @server_user);
                }

                push(@{$groups_servers_hash{$filename}}, @server_user);

                @server_user = 0;
            }

            close(MYSERVERFILE);

            push(@server_groups, $filename);
        }
    }

    closedir(MYDIR);

    push(@server_groups, 'all');
    @server_groups = sort(@server_groups);
}

#
# Take the passed-in string, and do exact matching with
# existing groups.
#
sub getMatchingGroup
{
    my($search_group) = @_;
    my($temp_group);

    foreach $temp_group (sort keys(%groups_servers_hash) )
    {
        if ($search_group eq $temp_group)
        {
            return($temp_group);
        }
    }

    return($FALSE);
}

#
# Take the passed-in string, and do fuzzy matching with
# existing groups.
#
sub getMatchingServer
{
    my($partial) = @_;

    if (!$partial)
    {
        return $FALSE;
    }

    $flag = $TRUE;

    #
    # The order here should go hostname, user, hostname, user, etc.
    #
    foreach $group (sort keys(%groups_servers_hash) )
    {
        foreach $server_user_temp ( @{$groups_servers_hash{$group}} )
        {
            # It's a hostname!
            if ($flag)
            {
                if ($partial eq $server_user_temp)
                {
                    return $server_user_temp;
                }

                $sub_string = substr($server_user_temp, 0, length($partial));

                if ($partial eq $sub_string)
                {
                    return $server_user_temp;
                }

                $flag = $FALSE;
            }
            else
            {
                $flag = $TRUE;
            }
        }
    }

    return($FALSE);
}

#
# Find one of the groups this server belongs to.
#
sub getServerGroup
{
    my($find_server) = @_;

    $flag = $TRUE;

    foreach $group (sort keys(%groups_servers_hash) )
    {
        foreach $server_user_temp ( @{$groups_servers_hash{$group}} )
        {
            # It's a hostname!
            if ($flag)
            {
                if ($find_server eq $server_user_temp)
                {
                    return($group);
                }
                else
                {
                    $flag = $FALSE;
                }
            }
            else
            {
                $flag = $TRUE;
            }
        }
    }

    return($FALSE);
}

#
# Lookup which user we need to connect as.
#
sub getServerUser
{
    my($find_server) = @_;
    my($found_it) = $FALSE;

    $flag = $TRUE;

    my($find_group) = getServerGroup($find_server);

    foreach $server_user_temp ( @{$groups_servers_hash{$find_group}} )
    {
        if ($found_it)
        {
            return($server_user_temp);
        }

        # It's a hostname!
        if ($flag)
        {
            if ($find_server eq $server_user_temp)
            {
                # Found the server we want, next item up should be
                # the username we're looking for!
                $found_it = $TRUE;
            }
            else
            {
                $flag = $FALSE;
            }
        }
        else
        {
            $flag = $TRUE;
        }
    }
}

#
# Let the loading script know we've loaded successfully.
#
return($TRUE);

#
# $Id$
#
######################################################################
#
# Name: Config.pm
#
# Description:  Perl module containing global configuration information
# such as where specific binaries live.
#
######################################################################

#
# Package definition
#
package Global::Config;

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
    @EXPORT = qw($SCP_BIN $SSH_BIN $TRUE $FALSE
                 $CONFIG_DIR $INSTALL_DIR
                 @internal_commands
                 &getBinaryLocations
                 &getNewReadLineTerm &getAttemptedCompletion
                 &getReadLinePrompt &setReadLinePrompt
                 &getReadLineTerm &getReadLineVersion
                 &ResetTermAndExit);
    @EXPORT_OK = qw();
}

# User visible variables.
use vars @EXPORT, @EXPORT_OK;
######################################################################

######################################################################
# USER CONFIGURABLE SETTINGS
#
# Where the configuration files are located.
$CONFIG_DIR =  '/promo/distribulator/conf';
# Where distribulator is installed, required for help files.
$INSTALL_DIR = '/promo/distribulator';
######################################################################

#
# Handy constants
#
$TRUE = 1;
$FALSE = 0;

#
# Hard-coded, icky icky.
#
@internal_commands = ( 'cd', 'copy', 'exit', 'help', 'login',
                       'remote-shell', 'run', 'server-group',
                       'server-list' );

#
# Runtime storage variables
#
my($attribs);
my($prompt);
my($term);

######################################################################
# Various Startup Subroutines
######################################################################

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
# Sets up our interface to GNU libreadline, and returns a
# handle to our instance.
#
sub getNewReadLineTerm
{
    #
    # Setup ReadLine for input...
    #
    $term = new Term::ReadLine 'Distribulator';
    $attribs = $term->Attribs;
    #
    # No ornaments(i.e. bold)
    #
    $term->ornaments(0,0,0,0);
    #
    # Attempt to have readline not grab signals.
    #
    $term->clear_signals();
    #
    # The joyous rebinding of CTRL-D for our own devious purposes.
    #
    $term->unbind_key(ord "\cd");
    $term->add_defun('exit', \&ResetTermAndExit, ord "\cd");
    #
    # Minimum size of command to add to history.
    #
    $term->MinLine(4);
    #
    # Command completion magic.
    #
    $attribs->{attempted_completion_function} = \&getAttemptedCompletion;
    $attribs->{completion_word} = \@internal_commands;
    #
    # Load history from ~/.distribulator if possible.
    #
    $term->ReadHistory("$ENV{'HOME'}/.dist_history");

    return $term;
}

#
# Attempted completion check.
#
sub getAttemptedCompletion
{
    my ($text, $line, $start, $end) = @_;

    # If first word then username completion, else filename completion
    if (substr($line, 0, $start) =~ /^\s*$/) {
        return $term->completion_matches($text,
            $attribs->{'list_completion_function'});
    }
    else
    {
        return ();
    }
}

#
# Hopefully will clean up any termcap weirdness.
#
sub ResetTermAndExit
{
    $term->WriteHistory("$ENV{'HOME'}/.dist_history");

    system("reset");

    print "\nReceived exit command.  Wrote history.  Reset terminal.  Dying...\n\n";

    exit(0);
}

######################################################################
# Various Get/Set Function For Dynamic Runtime Settings
######################################################################

#
# Allow other modules to get ahold of our ReadLine prompt.
#
sub getReadLinePrompt
{
    return $prompt;
}

#
# Allow other modules to set the ReadLine prompt.
#
sub setReadLinePrompt
{
    # Variable Scope Hack -- Not Sure Why?
    my($TempVar) = shift(@_);

    # Store it.
    $prompt = $TempVar;
}

#
# Allow other modules to get ahold of our ReadLine session.
#
sub getReadLineTerm
{
    return $term;
}

#
# Queries GNU libreadline for its' version.
#
sub getReadLineVersion
{
    my($version_str);

    $version_str = $attribs->{'library_version'};

    return $version_str;
}

######################################################################
#
# Let the loading script know we've loaded successfully.
#
return($TRUE);

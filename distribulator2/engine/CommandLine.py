######################################################################
#
# $Id$
#
# Name: CommandLine.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

try:
    # Standard modules
    import atexit
    import getpass
    import os
    import os.path
    import readline
    import rlcompleter
    import string
    import sys

    # Custom modules
    import engine.data.ExternalCommand
    import engine.data.InternalCommand

except ImportError:
    print "An error occured while loading Python modules, exiting..."
    sys.exit(1)

######################################################################

class CommandLine:

    def initHistory(self):
        thisCounter = 0
        thisHistory = os.path.join(os.environ['HOME'], ".dist_history")
    
        try:
            thisFile = open(thisHistory, 'r')
            for thisLine in thisFile:
                thisCounter = thisCounter + 1
            thisFile.close()

            # Load readline history.
            readline.read_history_file(thisHistory)
        
        except IOError:
            pass

        # Save readline history on exit.    
        atexit.register(readline.write_history_file, thisHistory)

        # Enable TAB filename-completion, instead of Python's default
        # object completion.
        readline.set_completer()
        readline.parse_and_bind("tab: complete")

        return thisCounter

    def invoke(self, PassedGlobalConfig):

        thisPromptEnv = 'sample'
        thisPromptUser = getpass.getuser()
        thisPromptGroup = 'wlx'

        while (1):
            #
            # Reset critical variables every time around the loop.
            #
            thisFoundIt = False
            thisInput = ''
            thisPrompt = '<' + thisPromptUser + '@' + thisPromptEnv + \
            '[' + thisPromptGroup + ']:' + os.getcwd() + '> '

            try:
                thisInput = raw_input(thisPrompt)

            except EOFError:
                print
                print
                print("Caught CTRL-D keystroke.  Wrote history.  Dying...")
                print
                return

            except KeyboardInterrupt:
                print

            if (thisInput):
                thisTokens = thisInput.split()

                #
                # Step 1 - Handle both "cd" and "exit" from this chunk of code.
                # Should probably be moved into the parser proper,
                #
                if (thisTokens[0] == 'exit'):
                    print
                    print("Received exit command.  Wrote history.  Dying...")
                    print
                    return

                try:
                    if (thisTokens[0] == 'cd'):
                        os.chdir(thisTokens[1])
                        continue

                except OSError, (errno, strerror):
                    print "ERROR: [Errno %s] %s: %s" % (errno, strerror, thisTokens[1])
                    continue
                #
                # Step 2 - Check for Unix "pass through" commands.
                #
                for thisCommand in PassedGlobalConfig.getPassThruList():
                    if (thisTokens[0] == thisCommand):
                        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand()
                        thisExternalCommand.setCommand(thisInput)
                        thisExternalCommand.run()
                        del thisExternalCommand
                        thisFoundIt = True
                        break

                # Icky flow-control hack.
                if (thisFoundIt):
                    continue
                #
                # Step 3 - Create InternalCommand object and fire up
                # the parser.
                #
                thisInternalCommand = engine.data.InternalCommand.InternalCommand()
                thisInternalCommand.setCommand(thisInput)
                thisInternalCommand.parse()
                del thisInternalCommand

######################################################################

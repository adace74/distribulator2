######################################################################
#
# $Id: RunParser.py 23 2005-10-14 21:20:52Z awd $
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved.
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""Parser implementation for the "copy" command."""

# Version tag
__version__= '$Revision: 23 $'[11:-2]

# Standard modules
import string
from pyparsing import Literal, Word, delimitedList, Optional, \
    Dict, Group, alphas, nums, alphanums, ParseException, Forward, \
    oneOf, pythonStyleComment, quotedString, ZeroOrMore, Keyword

# Custom modules
import Parser

######################################################################

class RunParser(Parser.Parser):
    """Parser implementation for the "run" command."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def getParseTree(self, PassedString):
        """This method is responsible for parsing the given string and returning a parse tree to the caller."""

        # Uhh...?
        runStatement   = Forward()

        # Define literals.
        leftBracket    = Literal('[').suppress()
        rightBracket   = Literal(']').suppress()
        quote          = Literal('"').suppress()
        nowKeyword     = Keyword("now", caseless=True)
        onKeyword      = Keyword("on", caseless=True)
        reverseKeyword = Keyword("reverse", caseless=True)
        runKeyword     = Keyword("run", caseless=True)
        singleKeyword  = Keyword("single", caseless=True)
        threadsKeyword = Keyword("threads", caseless=True)
        whereKeyword   = Keyword("where", caseless=True)

        # Basic server group and attribute parsing logic.
        identifier     = Word(alphas, alphanums + '_' ).setName("identifier") 
        commandStr     = identifier
        attribStr      = delimitedList(identifier)
        attribStrList  = Group(attribStr)
        groupStr       = identifier + ZeroOrMore(leftBracket + attribStrList.setResultsName("attribs") + rightBracket)
        groupStrList   = Group(delimitedList(groupStr))

        # Extended server group and attribute parsing logic.
        whereExpression = Forward()
        and_ = Keyword("and", caseless=True)
        or_ = Keyword("or", caseless=True)

        binaryOpStr = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True)
        integerStr = Word(nums)
        rightValue = integerStr | quotedString

        whereCondition = Group(identifier + binaryOpStr + rightValue)
        whereExpression << whereCondition + ZeroOrMore( (and_|or_) + whereExpression )

        # define the grammar
        runStatement << ( runKeyword + 
                          quote + commandStr.setResultsName("command") + quote +
                          Optional(onKeyword + groupStrList.setResultsName("groups")) +
                          Optional(Group(whereKeyword + whereExpression), "").setResultsName("where") +
                          Optional(nowKeyword) + Optional(reverseKeyword) +
                          Optional(singleKeyword) + Optional(threadsKeyword)
                        )

        runStatement.ignore(pythonStyleComment)

        RunParser = runStatement
        myTokens = RunParser.parseString(PassedString)

        print "Output: tokens = ",                 myTokens
        print "Output: tokens.attribs =",          myTokens.attribs
        print "Output: tokens.command =",          myTokens.command
        print "Output: tokens.groups =",           myTokens.groups
        print "Output: tokens.where =",            myTokens.where

        return myTokens
        
######################################################################

######################################################################
#
# $Id: CopyParser.py 23 2005-10-14 21:20:52Z awd $
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

class CopyParser(Parser.Parser):
    """Parser implementation for the "copy" command."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def getParseTree(self, PassedString):
        """This method is responsible for parsing the given string and returning a parse tree to the caller."""

        # Uhh...?
        copyStatement   = Forward()

        # Define literals.
        colon          = Literal(':').suppress()
        leftBracket    = Literal('[').suppress()
        rightBracket   = Literal(']').suppress()
        quote          = Literal('"').suppress()
        copyKeyword    = Keyword("copy", caseless=True)
        nowKeyword     = Keyword("now", caseless=True)
        onKeyword      = Keyword("on", caseless=True)
        reverseKeyword = Keyword("reverse", caseless=True)
        singleKeyword  = Keyword("single", caseless=True)
        threadsKeyword = Keyword("threads", caseless=True)
        whereKeyword   = Keyword("where", caseless=True)

        # Basic server group and attribute parsing logic.
        identifier     = Word(alphas + '/', alphanums + '_' ).setName("identifier") 
        filename       = Word(string.letters + string.punctuation).setName("filename")
        attribStr      = delimitedList(identifier)
        attribStrList  = Group(attribStr)
        groupStr       = identifier + ZeroOrMore(leftBracket + attribStrList.setResultsName("attribs") + rightBracket)
        groupStrList   = Group(delimitedList(groupStr))
        localfileStr   = filename 
        remotefileStr  = filename

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
        copyStatement << ( copyKeyword + 
                           localfileStr.setResultsName("local_filename") +
                           Optional(groupStrList.setResultsName("groups") + colon) +
                           remotefileStr.setResultsName("remote_filename") +
                           Optional(Group(whereKeyword + whereExpression), "").setResultsName("where") +
                           Optional(nowKeyword) + Optional(reverseKeyword) +
                           Optional(singleKeyword) + Optional(threadsKeyword)
                         )

        copyStatement.ignore(pythonStyleComment)

        CopyParser = copyStatement
        myTokens = CopyParser.parseString(PassedString)

        print "Output: tokens = ",                 myTokens
        print "Output: tokens.attribs =",          myTokens.attribs
        print "Output: tokens.local_filename =",   myTokens.local_filename
        print "Output: tokens.groups =",           myTokens.groups
        print "Output: tokens.remote_filename = ", myTokens.remote_filename
        print "Output: tokens.where =",            myTokens.where

        return myTokens

######################################################################

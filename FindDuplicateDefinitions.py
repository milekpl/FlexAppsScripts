# -*- coding: utf-8 -*-
#
#   Example.Find_Duplicate_Definitions
#    - A FlexTools Module
#
#   Scans a FLEx database checking for duplicate definitions in the same sense.
#
#   An error message is added to the FT_Flags (sense-level) field if database
#   changes are enabled. This allows easy filtering in FLEx to correct the errors.
#
# Marcin Miłkowski
# May 2014
#
# Platforms: Python .NET and IronPython
#

from FTModuleClass import *

import re
from types import *

#----------------------------------------------------------------
# Configurables:

TestNumberOfEntries  = -1   # -1 for whole DB; else no. of db entries to scan

TestSuite = [
       (re.compile(r"[?!\.]{1}$"), False, "ERR:no-ending-punc"),
       (re.compile(r"[?!\.]{2,}$"), True, "ERR:too-much-punc")

       ]

#----------------------------------------------------------------
# Documentation that the user sees:

docs = {'moduleName'       : "Find duplicate definitions",
        'moduleVersion'    : 1,
        'moduleModifiesDB' : True,
        'moduleSynopsis'   : "Finds entries with duplicate definitions.",
        'moduleDescription':
u"""

If database modification is permitted, then a warning value will be appended
to the sense-level custom field called FTFlags. This field must already exist
and should be created as a 'Single-line text' field using the 'First Analysis
Writing System.'
""" }


def list_duplicates(seq):
  seen = set()
  seen_add = seen.add
  # adds all elements it doesn't know yet to seen and all other to seen_twice
  seen_twice = set( x for x in seq if x in seen or seen_add(x) )
  # turn the set into a list (as requested)
  return list( seen_twice )

#----------------------------------------------------------------
# The main processing function

def MainFunction(DB, report, modifyAllowed):
    """
    This is the main processing function.

    This example illustrates:
     - Processing over all lexical entries and their senses.
     - Adding a message to a custom field.
     - Report messages that give feedback and information to the user.
     - Report messages that include a hyperlink to the entry (for Warning & Error only).
    
    """
    report.Info("Beginning Definition Check")
    #report.Warning("The sky is falling!")
    #report.Error("Failed to ...")
    
    limit = TestNumberOfEntries

    if limit > 0:
        report.Warning("TEST: Scanning first " + str(limit) + " entries...")
    else:
        report.Info("Scanning " + str(DB.LexiconNumberOfEntries()) + " entries...")

    AddReportToField = modifyAllowed

    flagsField = DB.LexiconGetSenseCustomFieldNamed("FTFlags")
    if AddReportToField and not flagsField:
        report.Error("FT_Flags custom field doesn't exist at Sense level")
        AddReportToField = False
    
    for e in DB.LexiconAllEntries():
        lexeme = DB.LexiconGetLexemeForm(e)
        list = []
        for sense in e.SensesOS:
			list.extend(DB.LexiconGetSenseDefinition(sense).split("; "))			
				
        if list_duplicates(list):
			report.Info("Found duplicate in: " + lexeme + ": " + " ,".join(list_duplicates(list)))
			if AddReportToField:
				#oldtag = DB.LexiconGetFieldText(sense, flagsField)
				DB.LexiconSetFieldText(sense, flagsField, "Duplicate definition found: " + " ,".join(list_duplicates(list)))
				#DB.LexiconAddTagToField(sense, flagsField, message)           
        if limit > 0:
           limit -= 1
        elif limit == 0:
           break


#----------------------------------------------------------------
# The name 'FlexToolsModule' must be defined like this:

FlexToolsModule = FlexToolsModuleClass(runFunction = MainFunction,
                                       docs = docs)

#----------------------------------------------------------------
if __name__ == '__main__':
    FlexToolsModule.Help()

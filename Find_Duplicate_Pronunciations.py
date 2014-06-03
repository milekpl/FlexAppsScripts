# -*- coding: utf-8 -*-
#
#   LingPl.Find_Duplicate_Pronunciations
#    - A FlexTools Module
#
#   Scans a FLEx database checking for duplicate pronunciations in entries.
#
#
# Marcin Miłkowski
# May 2014
#
# Platforms: Python .NET and IronPython
#

from FTModuleClass import *

from SIL.FieldWorks.Common.COMInterfaces import ITsString, ITsStrBldr

#----------------------------------------------------------------
# Configurables:

TestNumberOfEntries  = -1   # -1 for whole DB; else no. of db entries to scan
WritingIPA = "seh-fonipa"
splitString = ", "

#----------------------------------------------------------------
# Documentation that the user sees:

docs = {'moduleName'       : "Find duplicate pronunciations",
        'moduleVersion'    : 1,
        'moduleModifiesDB' : True,
        'moduleSynopsis'   : "Finds entries with duplicate pronunciations.",
        'moduleDescription': "No database modification. You can use the report links to modify the database."
 }


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

    """
    report.Info("Beginning Pronunciation Check")
    #report.Warning("The sky is falling!")
    #report.Error("Failed to ...")

    limit = TestNumberOfEntries

    if limit > 0:
        report.Warning("TEST: Scanning first " + str(limit) + " entries...")
    else:
        report.Info("Scanning " + str(DB.LexiconNumberOfEntries()) + " entries...")

    wsHandle = DB.WSHandle(WritingIPA)

    counter = 0

    for e in DB.LexiconAllEntries():
        lexeme = DB.LexiconGetLexemeForm(e)
        list = []
        for p in e.PronunciationsOS:
           pronText = ITsString(p.Form.get_String(wsHandle)).Text
           if pronText is not None:
                list.extend(pronText.split(splitString))
            #report.Info(pronText)

        if list_duplicates(list):
            report.Info("Found duplicate in: " + lexeme + ": " + " ,".join(list_duplicates(list)),
                    DB.BuildGotoURL(e))
            counter += 1

        if limit > 0:
           limit -= 1
        elif limit == 0:
           break

    report.Info("Number of duplicates found: " + str(counter))

#----------------------------------------------------------------
# The name 'FlexToolsModule' must be defined like this:

FlexToolsModule = FlexToolsModuleClass(runFunction = MainFunction,
                                       docs = docs)

#----------------------------------------------------------------
if __name__ == '__main__':
    FlexToolsModule.Help()

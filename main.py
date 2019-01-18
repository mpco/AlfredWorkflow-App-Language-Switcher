#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os
import sys
import subprocess

LangCodeDict = {'he': "Hebrew",
                'ar': "Arabic",
                'el': "Greek",
                'ja': "Japanese",
                'da': "Danish",
                'sk': "Slovak",
                'pt_PT': "Portuguese",
                'cs': "Czech",
                'ko': "Korean",
                'no': "Norwegian",
                'hu': "Hungarian",
                'tr': "Turkish",
                'pl': "Polish",
                'ru': "Russian",
                'fi': "Finnish",
                'id': "Indonesian",
                'nl': "Dutch",
                'th': "Thai",
                'pt': "Portuguese",
                'de': "German",
                'en': "English",
                'es': "Spanish",
                'it': "Italian",
                'sv': "Swedish",
                'fr': "French",
                'hr': "Croatian",
                'zh': "Chinese",
                "uk": "Ukrainian",
                "ms": "Malaysian",
                "vi": "Vietnamese",
                "ro": "Romanian",
                'es_419': "Latin American Spanish",
                'zh-Hans': "Chinese (Simplified)",
                'zh-Hant': "Chinese (Traditional)",
                'zh_CN': "Chinese (Simplified)",
                'zh_TW': "Chinese (Traditional)"}

appFilePath = os.environ['AppPath'].decode('utf-8')

appName, _ = os.path.splitext(os.path.basename(appFilePath))
appBundleID = subprocess.check_output(['mdls', '-name', 'kMDItemCFBundleIdentifier', '-r', appFilePath])
isSysLanguageCN = (subprocess.check_output(['defaults', 'read', '.GlobalPreferences', 'AppleLanguages'])[7:9] == "zh")

if not isSysLanguageCN:
    strBackDefault = "Unset Default Language"
    strBackDefaultAndOpen = "Unset Default Language & Launch"
    strLaunchApp = "Launch App in This Language"
    strSetDefaultAndOpen = "Set as Default Language & Launch"
else:
    strBackDefault = "删除默认语言设置"
    strBackDefaultAndOpen = "删除默认语言设置，并启动"
    strLaunchApp = "以此语言启动 App"
    strSetDefaultAndOpen = "始终 以此语言启动 App"

languageNameAbbreviationList = [x[:-6] for x in os.listdir(appFilePath + "/Contents/Resources") if x.endswith('.lproj')]

result = {"items": []}

if languageNameAbbreviationList:
    temp = {}
    temp["title"] = strBackDefault
    temp["autocomplete"] = temp["title"]
    temp["arg"] = "defaults delete {} AppleLanguages".format(appBundleID)
    mods_cmd = {}
    mods_cmd["valid"] = True
    mods_cmd["arg"] = "defaults delete {} AppleLanguages && open {}".format(appBundleID, appFilePath)
    mods_cmd["subtitle"] = strBackDefaultAndOpen
    temp["mods"] = {}
    temp["mods"]["cmd"] = mods_cmd

    result['items'].append(temp)

    for item in languageNameAbbreviationList:

        if item == "Base":
            continue

        languageName = LangCodeDict.get(item, item)

        temp = {}
        # temp["type"] = "file:skipcheck"
        # temp["icon"] = {"type": "fileicon", "path": item["formats"][0]}
        temp["title"] = languageName
        temp["autocomplete"] = temp["title"]
        temp["subtitle"] = strLaunchApp
        # temp["arg"] = appFilePath + "/Contents/MacOS/" + appName + " -AppleLanguages '({})' &".format(item)
        temp["arg"] = "\"" + os.path.join(appFilePath, "Contents",
                                          "MacOS", appName) + "\" -AppleLanguages '({})' &".format(item)
        mods_cmd = {}
        mods_cmd["valid"] = True
        mods_cmd["arg"] = "defaults write {} AppleLanguages '(\"{}\")' && open {}".format(
            appBundleID, item, appFilePath)
        mods_cmd["subtitle"] = strSetDefaultAndOpen
        temp["mods"] = {}
        temp["mods"]["cmd"] = mods_cmd

        result['items'].append(temp)
else:
    temp = {}
    temp["title"] = "No Available Language!"
    result['items'].append(temp)

sys.stdout.write(json.dumps(result))

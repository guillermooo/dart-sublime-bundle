# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import sublime

import unittest
import os

from Dart.lib.fs_completion import CompletionsList
from Dart.lib.fs_completion import FileSystemCompletion


items = [
    "addins",
    "ADFS",
    "AppCompat",
    "apppatch",
    "AppReadiness",
    "assembly",
    "Boot",
    "Branding",
    "BrowserChoice",
    "Camera",
    "CbsTemp",
    "CSC",
    "Cursors",
    "debug",
    "DesktopTileResources",
    "diagnostics",
    "DigitalLocker",
    "Downloaded Program Files",
    "en-GB",
    "en-US",
    "FileManager",
    "Firmware",
    "Fonts",
    "Globalization",
    "Help",
    "IME",
    "ImmersiveControlPanel",
    "Inf",
    "InputMethod",
    "L2Schemas",
    "LiveKernelReports",
    "Logs",
    "Media",
    "MediaViewer",
    "Microsoft.NET",
    "Minidump",
    "ModemLogs",
    "Offline Web Pages",
    "Panther",
    "Performance",
    "PLA",
    "PolicyDefinitions",
    "Prefetch",
    "Registration",
    "rescache",
    "Resources",
    "SchCache",
    "schemas",
    "security",
    "ServiceProfiles",
    "servicing",
    "Setup",
    "ShellNew",
    "SKB",
    "SoftwareDistribution",
    "Speech",
    "System",
    "System32",
    "SystemResources",
    "SysWOW64",
    "TAPI",
    "Tasks",
    "Temp",
    "ToastData",
    "tracing",
    "twain_32",
    "vpnplugins",
    "Vss",
    "Web",
    "WinStore",
    "WinSxS",
    "bfsvc.exe",
    "bootstat.dat",
    "DtcInstall.log",
    "explorer.exe",
    "HelpPane.exe",
    "hh.exe",
    "MEMORY.DMP",
    "mib.bin",
    "notepad.exe",
    "PFRO.log",
    "Professional.xml",
    "regedit.exe",
    "setupact.log",
    "setuperr.log",
    "splwow64.exe",
    "Starter.xml",
    "system.ini",
    "twain_32.dll",
    "vmgcoinstall.log",
    "win.ini",
    "WindowsUpdate.log",
    "winhlp32.exe",
    "WMSysPr9.prx",
    "write.exe",
]


class Test_CompletionsList(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def tearDown(self):
        self.view.close()

    def test_is_iterable(self):
        cl = CompletionsList(items)
        collected = []
        times = 0
        for item in cl:
            collected.append(item)
            times += 1
            if times == 2:
                break
        self.assertEqual(collected, ["addins", "ADFS"])

    def test_can_return_prefixed(self):
        cl = CompletionsList(items)
        collected_a = cl.iter_prefixed("set")
        collected_b = cl.iter_prefixed("win")
        self.assertEqual(list(collected_a), ["Setup", "setupact.log", "setuperr.log"])
        self.assertEqual(list(collected_b), ['WinStore', 'WinSxS', 'win.ini', 'WindowsUpdate.log', 'winhlp32.exe'])

    def test_can_be_casesensitive(self):
        cl = CompletionsList(items)
        collected_a = cl.iter_prefixed("set")
        collected_b = cl.iter_prefixed("set", casesensitive=True)
        self.assertNotEqual(list(collected_a), list(collected_b))


class Test_FileSystemCompletion(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def tearDown(self):
        self.view.close()

    @unittest.skipIf(os.name != 'nt', 'because OS is not Windows')
    def test_can_return_items(self):
        fsc = FileSystemCompletion()
        items = fsc.get_completions('C:\\')
        self.assertTrue("Windows/" in items)
        self.assertTrue(len(items) > 1)

    @unittest.skipIf(os.name != 'nt', 'because OS is not Windows')
    def test_can_filter_items(self):
        fsc = FileSystemCompletion()
        items_a = fsc.get_completions('C:\\')
        items_b = fsc.get_completions('C:\\W')
        self.assertNotEqual(items_a, items_b)
        self.assertTrue(set(items_b).issubset(set(items_a)))

import sublime
import sublime_plugin
import re
import os
import time
import traceback
import subprocess

class VerilogAddHeaderCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        file_name = self.view.file_name()
        plugin_settings = sublime.load_settings("SublimePlugin.sublime-settings")
        file_name_without_path = os.path.split(file_name)[1]
        author = plugin_settings.get("Author")
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.view.insert(edit, 0, "\n//" + "=" * 98 + "\n")
        self.view.insert(edit, 0, "\n//Description" + " " * 3 + ": ")
        self.view.insert(edit, 0, "\n//")
        self.view.insert(edit, 0, "\n//Revision" + " " * 6 + ": " + "0")
        self.view.insert(edit, 0, "\n//Last Modified" + " " + ": " + current_time)
        self.view.insert(edit, 0, "\n//Create" + " " * 8 + ": " + current_time)
        self.view.insert(edit, 0, "\n//File" + " " * 10 + ": " + file_name_without_path)
        self.view.insert(edit, 0, "\n//Author" + " " * 8 + ": " + author)
        self.view.insert(edit, 0, "//" + "=" * 98)
        sublime.status_message("File header added")

class VeriogAddModTimeCommand(sublime_plugin.TextCommand):

    """change the last modified time"""

    def run(self, edit):
        modify_time_pattern = r"(?<=^//Last Modified : )[\d\D]*?$"
        modify_revision_pattern = r"(?<=^//Revision      : )[\d]*?$"
        revision_region = self.view.find(modify_revision_pattern, 0)
        insert_region = self.view.find(modify_time_pattern, 0)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.view.replace(edit, insert_region, current_time)
        revision_data = int(self.view.substr(revision_region))
        self.view.replace(edit, revision_region, str(revision_data+1))

class VerilogAlignCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        txtr <= self.view.sel()[0]
        lines <= self.view.lines(txtr)
        for line in lines:
            f <= self.view.find("(\s+)=(\s+)", line.begin())
            if f.begin() != -1:
                self.view.replace(edit, f, " <= ")
            print(f)

class RunCompileCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        file_name = self.view.file_name()
        Comp_dir = r"C:\altera\13.0\quartus\bin"
        cmd = 'quartus_map Test --analyze_file ' + '"' + file_name + '"'
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=Comp_dir)
        # stdoutdata, stderrdata = p.communicate()
        stdoutdata, stderrdata = p.communicate()
        ss = str(stdoutdata)
        ss = ss.replace("b'", "")
        ss = ss.split("\\r\\n")
        for d in ss:
            print(d)

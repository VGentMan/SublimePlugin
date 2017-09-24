import sublime
import sublime_plugin
import re
import os
import time
import sys
import subprocess
import shutil

def file_ext(file_name):
    ext = os.path.splitext(os.path.split(file_name)[1])[1]   
    return ext

class VerilogBackupCommand(sublime_plugin.TextCommand):

    """create backup verilog files"""
        
    def run(self, edit):
        file_name = self.view.file_name()
        file_only_name = os.path.splitext(os.path.split(file_name)[1])[0]
        current_data = time.strftime('%d_%m_%Y', time.localtime())
        current_time = time.strftime('(%H_%M_%S)', time.localtime())
        backup_path = os.path.split(file_name)[0] + '\\Backup\\' + current_data
        try:
            os.makedirs(backup_path)
        except:
            pass
        backup_name = backup_path + '\\' + file_only_name + current_time + file_ext(file_name)     
        if not os.path.isfile(backup_name):    
            shutil.copyfile(file_name, backup_name)
        sublime.message_dialog('Бэкап успешно сделан!')
        
        
class VerilogAddHeaderCommand(sublime_plugin.TextCommand):

    """add header comment to file"""

    def header_modifier(self, edit):
        modify_time_pattern = r"(?<=^//Last Modified : )[\d\D]*?$"
        modify_revision_pattern = r"(?<=^//Revision      : )[\d]*?$"
        revision_region = self.view.find(modify_revision_pattern, 0)
        insert_region = self.view.find(modify_time_pattern, 0)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.view.replace(edit, insert_region, current_time)
        revision_data = int(self.view.substr(revision_region))
        self.view.replace(edit, revision_region, str(revision_data+1))

    def run(self, edit):
        file_name = self.view.file_name()
        plugin_settings = sublime.load_settings("SublimePlugin.sublime-settings")
        file_name_without_path = os.path.split(file_name)[1]
        author = plugin_settings.get("Author")
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        header = \
        "//" + "-" * 100 + \
        "\n//Author        : " + author +\
        "\n//File          : " + file_name_without_path +\
        "\n//Create        : " + current_time +\
        "\n//Last Modified : " + current_time +\
        "\n//Revision      : " + "0" +\
        "\n//" +\
        "\n//Description   : " +\
        "\n//" + "-" * 100 + "\n"       
        header_pattern = r"(?<=^//)[-]{100}"
        if self.view.find(header_pattern, 0).empty():    
            self.view.insert(edit, 0, header)
            sublime.status_message("File header added")
        else:
            self.header_modifier(edit)
            sublime.status_message("File header was changed!")
        


class VerilogAlignCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        align_pattern = r"(?<=[\w+])(\s*<=\s*)(?=\w+;)"
        align_txt = self.view.sel()[0]
        lines = self.view.lines(align_txt)
        for line in reversed(lines):
            f = self.view.find(align_pattern, line.begin())
            if not f.empty():
                self.view.replace(edit, f, " <= ")
        
        align_txt = self.view.sel()[0]
        lines = self.view.lines(align_txt)
        wrap = []
        for line in lines:
            f = self.view.find(" <= ", line.begin())
            wrap.append(f.begin() - line.begin())       
        wrap_max = max(wrap)
        ind_max = wrap.index(wrap_max)
        ind = len(wrap) - 1
        for line in reversed(lines):
            f = self.view.find(" <= ", line.begin())
            pattern = " " * (wrap_max - wrap[ind]) + " <= "
            if not f.empty():
                if ind != ind_max:
                    self.view.replace(edit, f, pattern)
            ind -=1    


class RunCompileCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        file_name = self.view.file_name()
        plugin_settings = sublime.load_settings("SublimePlugin.sublime-settings")
        Comp_dir = plugin_settings.get("Quartus dir")
        cmd = 'quartus_map Test --analyze_file ' + '"' + file_name + '"'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=Comp_dir)
        stdoutdata, stderrdata = p.communicate()
        ss = str(stdoutdata)
        ss = ss.replace("b'", "")
        ss = ss.split("\\r\\n")
        if 'successful' in ss[-6]:
            sublime.message_dialog(ss[-6])
        else:
            sublime.error_message(ss[-6])



        
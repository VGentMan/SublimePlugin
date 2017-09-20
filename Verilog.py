import sublime
import sublime_plugin
import re

class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.d = self.view.sel()
        self.view.insert(edit, 0, "\'" + str(self.d) + "\'")

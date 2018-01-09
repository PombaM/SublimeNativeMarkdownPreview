'''
Preview your markdown files with the default app installed in your system.
'''

import os
import sublime
import sublime_plugin
import subprocess
import sys


class NativeMarkdownPreview(sublime_plugin.TextCommand):
    # returns true only if the current file is a markdown file
    def can_procceed(self):
        if 'markdown' in self.get_scope():
            return True
        else:
            return False

    # get filetype aka scope
    def get_scope(self):
        return self.view.scope_name(self.view.sel()[0].begin())

    def try_open(self, command=lambda: command):
        try:
            command()
        except Exception as e:
            sublime.error_message(e)

    def open_file(self):
        platform = sys.platform
        file = self.view.file_name()

        if platform.startswith('linux'):
            cmd = 'xdg-open {}'.format(file)
            self.try_open(subprocess.call(cmd, shell=True))

        elif platform.startswith('darwin'):
            cmd = 'open {}'.format(file)
            self.try_open(subprocess.call(cmd, shell=True))

        elif platform.startswith('win32') or platform.startswith('cygwin'):
            try_open(os.startfile(file))

        else:
            sublime.message_dialog('Unsupported OS')

    # decide when to show the plugin's contextual menue
    def is_visible(self):
        return self.can_procceed()

    # adds captions to context menu
    def description(self):
        if self.can_procceed():
            return 'Preview markdown'

    def run(self, edit):
        self.open_file()

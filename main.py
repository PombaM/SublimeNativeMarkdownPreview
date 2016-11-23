'''
This plugin requires Remarkable (https://remarkableapp.github.io/) to work.
This plugin aims to provide a quicker way to view/edit markdown files using Remarkable.
'''

import sublime
import sublime_plugin
import subprocess
import webbrowser


class PreviewMarkdownWithRemarkableCommand(sublime_plugin.TextCommand):

    '''
        Checks - if Remarkable is installed
               - if current file's a markdown file
    '''
    def run_checks(self, scope):
        # POSIX way to check if a program is installed
        parameter = 'command -v remarkable'
        # This will return 0 if Remarkable is installed
        has_remarkable = subprocess.call(parameter, shell=True)

        if has_remarkable is 0 and 'markdown' in scope:
            self.open_file()
            return True

        if has_remarkable is not 0:
            self.offer_install('Remarkable is not installed, do you want to install it?')
            return False

        if 'markdown' not in scope:
            self.notify_user('The file you are trying to open is not a markdown file.')
            return False

    def notify_user(self, msg):
        self.view.set_status('OWR_STATUS', msg)
        sublime.message_dialog(msg)
        sublime.set_timeout(self.clear_status_bar, 7000)

    def clear_status_bar(self):
        self.view.erase_status('OWR_STATUS')

    def offer_install(self, msg):
        additional_help = '\n\n(Clicking OK will open Remarkable\'s homepage in your default webbrowser)'
        confirm_install = sublime.ok_cancel_dialog(msg + additional_help)

        if confirm_install:
            webbrowser.open_new_tab(url='https://remarkableapp.github.io/')
        else:
            sublime.message_dialog('This plugin won\'t work without Remarkable.')

    # call remarkable
    def open_file(self):
        subprocess.Popen(['remarkable', self.view.file_name()])

    def run(self, edit):
        # get file's scope
        scope = self.view.scope_name(self.view.sel()[0].begin())
        self.run_checks(scope)

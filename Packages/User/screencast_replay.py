import sublime
import sublime_plugin
import time


class ScreencastReplayCommand(sublime_plugin.TextCommand):
    def run_commands(self):
        self.view.run_command("undo")
        self.view.run_command("move", {"by": "characters", "forward": True})

    def delayed_undo(self, delay):
        sublime.set_timeout_async(lambda: self.run_commands(), delay)
        command, _, _ = self.view.command_history(-1, True)

        if command == "" or command == None:
            print("no more history, stopping replay")
            return

        sublime.set_timeout_async(lambda: self.delayed_undo(delay), delay)

    def run(self, edit):
        print("screencast replay called")

        self.delayed_undo(1000)

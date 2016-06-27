import sublime, sublime_plugin

class CloseOtherWindows(sublime_plugin.TextCommand):
  def run(self, edit):
    current_window = self.view.window()

    for window in sublime.windows():
      if current_window != window:
        window.run_command("close_window")

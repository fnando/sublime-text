import sublime
import sublime_plugin
import os
import subprocess

class RubyFormatOnSave(sublime_plugin.EventListener):
  def on_post_save_async(self, view):
    if view.match_selector(0, "source.ruby"):
      (row, col) = view.rowcol(view.sel()[0].begin())
      filename = view.file_name()

      subprocess.call(
        ["rubocop", "-a", filename],
        cwd=os.path.dirname(filename)
      )

      view.sel().add(sublime.Region(view.text_point(row, col)))

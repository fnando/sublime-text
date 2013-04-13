"""
SplitScreen-Resizer v3.0.0
by Jesus Leon
https://github.com/iamjessu/sublime-SplitScreen-Resizer


Contributors, THANKS!:
Artis Raugulis <artis@devart.lv>


A fork of:

    SplitScreen v1.0.0
    by Nick Fisher
    https://github.com/spadgos/sublime-SplitScreen

Combined with:

    Split Navigation
    by Linus Oleander
    https://github.com/oleander/sublime-split-navigation
"""
import sublime, sublime_plugin
import re


def addUp(lst):
    out = [0.0]
    for i in lst:
        out.append(out[-1] + i)

    return out

class PanelChangedCommand(sublime_plugin.EventListener):
    last_work_group = None
    settings = None
    def on_activated(self, view):
        # Load settings.
        if self.settings == None:
            self.settings = sublime.load_settings("splitscreen-resizer.sublime-settings")

        # If mouse focus disabled. Exit.
        if self.settings.get('resize_on_focus') == False:
            return 0

        # If theres only one group in current window. Do nothing.
        if view.window().num_groups() == 1:
            return 0

        # Current active group.
        current_active_group = view.window().active_group()

        # Working group not changed. Do nothing.
        if self.last_work_group == current_active_group:
            return 0

        # Update last work group.
        self.last_work_group = current_active_group

        # By default we show left side.
        # Note the extra parameter ignore_focus_on_resize. 
        # It prevents an infinite loop. A short circuit! :O
        args = {"side":"left", "ignore_focus_on_resize":True}

        # If right side active, update args to right side version.
        if(current_active_group == 1):
            args = {"side":"right", "ignore_focus_on_resize":True}

        win = view.window()
        win.run_command("split_screen_resizer", args)


class SplitScreenResizerCommand(sublime_plugin.WindowCommand):
    settings = None
    def run(self, side, ignore_focus_on_resize=False):
        # Load settings
        if self.settings == None:
            self.settings = sublime.load_settings("splitscreen-resizer.sublime-settings")
        win = self.window
        num = win.num_groups()
        act = win.active_group()

        #If theres only one group in current window. Do nothing.
        if num == 1:
            return 0

        if side == "left":
            ratio = self.settings.get('ratio_left')
            act = act - 1

        if side == "right":
            ratio = self.settings.get('ratio_right')
            act = act + 1

        # By keeping it as modulus operation we ensure that:
        #     - It continues focusing the next/previous column in case we're 
        #       working with more than 2 columns.
        #     - It acts as a loop, focusing the first/last column when the
        #       last/first is reached respectively.
        if self.settings.get('focus_on_resize') and ignore_focus_on_resize == False:
            win.focus_group(act % num)


        """
        Keep original code in case we want to add vertical resizing.
        """
        parts = re.split("\\s*,\\s*", ratio)

        horiz = parts[0] or "1"
        vert = parts[1] or "1" if len(parts) > 1 else "1"

        vert = map(float, re.split(":", vert))
        horiz = map(float, re.split(":", horiz))
        vertTotal = sum(vert)
        horizTotal = sum(horiz)
        vert = map((lambda x: x / vertTotal), vert)
        horiz = map((lambda x: x / horizTotal), horiz)

        cols = addUp(horiz)
        rows = addUp(vert)

        cells = []
        for x, val1 in enumerate(horiz):
            for y, val2 in enumerate(vert):
                cells.append([x, y, x + 1, y + 1])

        self.window.run_command('set_layout', {
            "cols": cols,
            "rows": rows,
            "cells": cells
        })
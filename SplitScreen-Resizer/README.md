SplitScreen-Resizer
===================

A [Sublime Text 2][sublime_link] plugin created to switch and resize a 2-Columns layout in the easiest and most confortable way. Just press the keyboard shortcuts and the plugin will make the indicated column your working column, by automatically focusing on it and making it wider.

No more going back to the mouse to manually resize your columns everytime you want to switch from one side to another.


Keys
----

Pressing <kbd>Alt+Ctrl+left</kbd> or <kbd>Alt+Ctrl+right</kbd> (or <kbd>Ctrl+Super+left</kbd> / <kbd>Ctrl+Super+right</kbd> on Linux) will switch focus to the respective column and resize it according to the configured ratio (which by default is "7:3" and "3:7"). You can change these ratios, the keyboard shortcuts and the ability to autofocus when resizing in the settings of this package following the *Preferences > Package Settings > SplitScreen-Resizer* menu. You can even make it autosize the columns on mouse click or on Sublime's default *Focus Group* command. 

So if you are a full-keyboard coder or a mouse lover, this plugin got you covered.


Credits
-------

**Created by**

Jesus Leon ([@iamjessu][iamjessu_link]).

**Contributors:**

* [ArtisR][ArtisR_link] (Artis Raugulis) - Added mouse focus.

This plugin combines functionalities from these plugins:

* [SplitScreen][splitscreen_link] by [spadgos][spadgos_link] (Nick Fisher).
* [Split Navigation][splitnavigation_link] by [oleander][oleander_link] (Linus Oleander).



Updates
-------

**v1.3** 

* Added *onFocus* support.
* Ratios and behavior are configured in the settings file.

**v1.2** 

* Added autofocus feature.


**v1.0** 

* Resize columns by pressing the configured keys.


Notes
-----

Numbers are treated as a ratio, so `50:50` is identical to `1:1`.

For example:

    50:50
    (2 columns, equal width. 1 row)

    --------------------
    |        |         |
    |        |         |
    |        |         |
    |        |         |
    |        |         |
    |        |         |
    --------------------

    1:2
    (2 columns, one twice the width of the other. 1 row)

    --------------------
    |      |           |
    |      |           |
    |      |           |
    |      |           |
    |      |           |
    --------------------


[sublime_link]: http://www.sublimetext.com/
[iamjessu_link]: https://twitter.com/iamjessu
[splitscreen_link]: https://github.com/spadgos/sublime-SplitScreen
[spadgos_link]: https://github.com/spadgos
[splitnavigation_link]: https://github.com/oleander/sublime-split-navigation
[oleander_link]: https://github.com/oleander
[ArtisR_link]: https://github.com/ArtisR

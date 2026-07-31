# Sublime Text

This is my set up for [Sublime Text](https://sublimetext.com/).

## Installation

First, make sure you install [Package Control](https://packagecontrol.io). Then
you have to install my [custom repository](https://sublime.fnando.com/).

Finally, close Sublime Text and reopen it.

## GitHub token

`Packages/User/Package Control.sublime-settings` is tracked by this repo and
synced across machines, so it must never contain secrets. To authenticate
Package Control against GitHub's API (avoids rate limiting), create a gitignored
file at `Packages/PackageControl.Local/Package Control.sublime-settings` with
your own [personal access token](https://github.com/settings/tokens):

```json
{
  "github_token": "github_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "http_basic_auth": {
    "api.github.com": [
      "your-github-username",
      "github_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ]
  }
}
```

Sublime Text merges `.sublime-settings` files with the same name across all
package folders, so these values get combined with the tracked settings file at
runtime without ever being committed. This file needs to be created on every
machine individually.

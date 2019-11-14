import sublime, sublime_plugin
from os import environ
import sys
import subprocess
import re

def plugin_loaded():
  if sys.platform != "darwin":
    return

  command = "/usr/bin/login -fqpl %s %s -l -c 'echo $PATH'" % (environ["USER"], environ["SHELL"])
  result = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  path = result.stdout.read().decode("utf-8").rstrip()

  system_dirs = []
  user_dirs = []
  dirs = path.split(":")

  for dir in dirs:
    if re.match(r"^/(usr|bin|sbin|opt)", dir):
      system_dirs.append(dir)
    else:
      user_dirs.append(dir)

  environ["PATH"] = ":".join(user_dirs + system_dirs)
  environ["RUBYOPT"] = "-I. -I./lib -I./test"

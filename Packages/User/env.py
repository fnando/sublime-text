import sublime, sublime_plugin
from os import environ
import sys
import subprocess

def plugin_loaded():
  if sys.platform != "darwin":
    return

  command = "/usr/bin/login -fqpl %s %s -l -c 'echo $PATH'" % (environ["USER"], environ["SHELL"])
  result = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  path = result.stdout.read().decode("utf-8").rstrip()

  environ["PATH"] = path
  environ["RUBYOPT"] = "-I. -I./lib -I./test"

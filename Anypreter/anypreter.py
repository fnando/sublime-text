import sublime, sublime_plugin, subprocess, os, re, thread, functools, json, time


class anypreter(sublime_plugin.TextCommand):

	def interpret(self):

		code = self.get_code() # Get the code
		if not code: return False # No code, what are you trying to do?

		code = self.replacements(code)	# Do all the replacements
		code = self.custom_code(code)	# This is for syntax specific code adjustments
		code = self.plain_wrapper(code)	# Wrap the code in something
		code = self.encryption(code)	# Encrypt it if needed
		code = self.wrapper(code)		# Wrapp it again in something

		self.run_command(code) # Do all the magic :)

		self.cleanup() # Delete all the Variables



	def cleanup(self):

		# Delete all the important variables
		if hasattr(self, "settings"): del self.settings
		if hasattr(self, "current_view"): del self.current_view
		if hasattr(self, "syntax"): del self.syntax
		if hasattr(self, "output_panel"): del self.output_panel
		if hasattr(self, "buffer_finish"): del self.buffer_full
		if hasattr(self, "output_buffer"): del self.output_buffer



	def get_view(self):

		# Get the current view if not has already been set
		if not hasattr(self, "current_view"):
			self.current_view = sublime.active_window().active_view()

		# Return the current view
		return self.current_view



	def get_syntax(self):
		
		# Get the current syntax if not has already been set
		if not hasattr(self, "syntax"):
			self.syntax = self.get_view().settings().get("syntax").rsplit("/")[2].split(".")[0]

		# Return the current syntax
		return self.syntax



	def get_settings(self, return_list = False, settings_index = 0):
		
		# If we already have set a specific setting and dont need a list of settings, simply return it
		if hasattr(self, "settings") and return_list is False: return self.settings
		
		# Build the possible settings-path and convert it into a real path (OS specific)
		settings_file = self.get_syntax() + ".sublime-settings"
		path = os.path.realpath(sublime.packages_path() + "/Anypreter/interpreters/" + self.get_syntax() + "/" + settings_file)
		
		# Return False if there is no such settings-file
		if not os.path.exists(path): return False
		
		# Convert settings file into list or dictionary and get its type
		settings = json.loads(open(path).read())
		settings_type = type(settings)
		
		# If a list should be returned, make sure it is one
		if return_list is True:
			if settings_type is list:
				return settings
			elif settings_type is dict:
				return [settings]
			else: return False

		# If we dont need a list, we want a specific setting
		# and safe it so we dont need to read it again
		if settings_type is list:
			self.settings = settings[settings_index]
		elif settings_type is dict:
			self.settings = settings
		else: self.settings = False
		
		return self.settings



	def get_option(self, setting_name, default = None, return_list = False):

		# Get a List of all available settings for this syntax if a list should be returned
		if return_list is True:
			settings = self.get_settings(True)
			setting_list = []
			for mode in settings:
				setting_list.append(mode.get(setting_name, default))
			return setting_list

		# Get specific settings for current syntax
		settings = self.get_settings()
		if type(settings) is dict:
			return settings.get(setting_name, default)

		return False



	def get_code(self):

		# Return selection if there is one
		code_selection = self.get_view().substr(self.get_view().sel()[0])
		if len(code_selection) != 0:
			return code_selection

		# Return full file if there is no selection and there is something in the file
		code_full = self.get_view().substr(sublime.Region(0, self.get_view().size()))
		if len(code_full) != 0:
			return code_full

		return False # Return false if there is nothing else to return



	def replacements(self, code):

		# Get replacements if there are some
		replacements = self.get_option("replacements")
		if not replacements: return code # Else return untouched code

		# Do the replacements
		for replacement in replacements:
			pattern = re.compile(replacement["search"])
			code = pattern.sub(replacement["replace"], code)

		return code # And return the resulting code



	def custom_code(self, code):

		# Get the name of the custom code file if there is one
		custom_code_file = self.get_option("custom_code_file")
		if not custom_code_file: return code # Else return untouched code

		# Build the real path to the custom code file
		custom_code_file = self.get_syntax() + "/" + custom_code_file
		path = os.path.realpath(sublime.packages_path() + "/anypreter/interpreters/" + custom_code_file)
		if not os.path.exists(path): return code # Return the untouched code if the file does not exist

		# Run the custom code
		custom_stuff = open(path).read().replace('\r\n', '\n')

		#lMapping = os.linesep.join(lMapping.splitlines())
		exec custom_stuff
		return code # Return its resulting code



	def plain_wrapper(self, code):

		# Get the plain wrapper if there is one
		wrapper = self.get_option("plain_wrapper")
		if not wrapper: return code # Else return untouched code

		# Return the wrapped code
		return wrapper.replace("%code%", code)



	def encryption(self, code):

		# Get the encryption-name if there is one
		encryption = self.get_option("encryption")
		if not encryption: return code # Else return untouched code

		# Return the encrypted and break-stripped code
		return str(code).encode(encryption).replace("\n", "")



	def wrapper(self, code):

		# Get the wrapper if there is one
		wrapper = self.get_option("wrapper")
		if not wrapper: return code # Else return untouched code

		# Return the wrapped code
		return wrapper.replace("%code%", code)



	def run_command(self, code):
		
		if self.get_view().settings().get("anypreter_set_envdir", True) and self.get_view().file_name():

			dirname = os.path.realpath(os.path.dirname(self.get_view().file_name()))
			if os.path.exists(dirname):
				#sublime.error_message(dirname)
				os.chdir(dirname)

		# Get the command if there is one
		command = self.get_option("command")
		if not command: return False # Else return False

		# Insert the code into the command
		command = command.replace("%code%", code)
		
		# Get the binarypath as realpath (OS specific), set it to False if it does not exist or its empty
		settings_name = self.get_syntax().lower() + "_binary_path"
		binary_path = self.get_view().settings().get(settings_name)
		
		if not binary_path: binary_path = False
		else:
			binary_path = os.path.realpath(binary_path)
			if not os.path.exists(binary_path): binary_path = False
		
		# Prepend it to the command if it exists
		if binary_path: command = binary_path + "/" + command

		# Start the process which executes the command
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

		# Decide if the output gets buffered and print the available text in a specific interval
		if self.get_view().settings().get("anypreter_stream_output", False):
			update_rate = self.get_view().settings().get("anypreter_output_inteval", 1)
			thread.start_new_thread(self.buffer_pipe, (process, update_rate))
		else: # Or if we should wait till the process has finished to print its output
			thread.start_new_thread(self.output_all, (process,))



	def output_all(self, process):

		sublime.set_timeout(functools.partial(self.output, process.stdout.read()), 0)



	def buffer_pipe(self, process, update_rate = 1):
		
		if not hasattr(self, "output_buffer"): self.output_buffer = ""

		self.buffer_finish = False

		thread.start_new_thread(self.output_from_buffer, (update_rate,))
		while True:
			line = process.stdout.readline()
			process.stdout.flush()
			if line == "" and process.poll() != None: break
			if line != "":
				self.output_buffer += line
				line = ""

		self.buffer_finish = True
		process.stdout.close()



	def output_from_buffer(self, update_rate = 1):
		

		if not hasattr(self, "buffer_finish") or not hasattr(self, "output_buffer"): return False

		while True:
			if self.output_buffer != "":

				output = self.output_buffer # Save the current buffer
				self.output_buffer = self.output_buffer[len(output):] # Delete everything we saved from the buffer
				
				# self.output needs to be called from the main-thread
				sublime.set_timeout(functools.partial(self.output, output), 0)
				output = "" # Reset the output variable

			# Break if buffering has finished and nothing is left in the buffer
			if self.buffer_finish == True and self.output_buffer == "": break

			# Wait some time, because we only need to update the output each x-seconds
			time.sleep(update_rate)



	def output(self, value, panel_name = "anypreter"):
		
		if not hasattr(self, 'output_panel'):
			self.output_panel = self.get_view().window().get_output_panel(panel_name)
		panel = self.output_panel

		# Unlock the output panel so we can put text in it
		panel.set_read_only(False)

		# Set its syntax to display line-numbers
		panel.set_syntax_file('Packages/Text/Plain text.tmLanguage')

		edit = panel.begin_edit() # Start editing

		panel.insert(edit, panel.size(), value.decode('utf-8')) # Insert the output
		panel.end_edit(edit) # End the editing

		# Lock and display the panel
		panel.set_read_only(True)
		self.get_view().window().run_command("show_panel", {"panel": "output." + panel_name})



	def is_available(self):
		
		# Build the possible settings-path and convert it into a real path (OS specific)
		settings_file = self.get_syntax() + ".sublime-settings"
		path = os.path.realpath(sublime.packages_path() + "/Anypreter/interpreters/" + self.get_syntax() + "/" + settings_file)
		
		# Return True if there is such a settings-file
		if os.path.exists(path): return True
		return False # Else return False



class anypreterCommand(anypreter):

	def run(self, edit):

		if not self.is_available(): return False
		
		# Just start the main-process
		self.interpret()



# Command to display Quick-Panel
class anypreterQuickPanelCommand(anypreter):

	def run(self, edit):
		
		if not self.is_available(): return False

		# Get the available mode-names and display them in a quick panel
		modes = self.get_option("Name", "Unnamed mode", True)
		self.get_view().window().show_quick_panel(modes, self.done)



	def done(self, settings_index):

		# Return false if no mode got selected
		if settings_index == -1: return False

		# Else load the correct settings and start the main-process
		self.get_settings(False, settings_index)
		self.interpret()
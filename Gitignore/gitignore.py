import sublime, sublime_plugin
import os


class rungiboCommand(sublime_plugin.WindowCommand, sublime.Window):

	chosen_array = []

	first_list = ['Actionscript', 'Android', 'Autotools', 'CakePHP', 'CFWheels', 'C', 'C++', 'Clojure', 'CMake', 'CodeIgniter', 'Compass', 'Concrete5', 'Coq', 'CSharp', 'Delphi', 'Django', 'Drupal', 'Erlang', 'ExpressionEngine', 'Finale', 'ForceDotCom', 'FuelPHP', 'gcov', 'Go', 'Grails', 'GWT', 'Haskell', 'Java', 'Jboss', 'Jekyll', 'Joomla', 'Jython', 'Kohana', 'LaTeX', 'Leiningen', 'LemonStand', 'Lilypond', 'Lithium', 'Magento', 'Maven', 'nanoc', 'Node', 'Objective-C', 'OCaml', 'Opa', 'opencart', 'OracleForms', 'Perl', 'PlayFramework', 'Python', 'Qooxdoo', 'Rails', 'R', 'RhodesRhomobile', 'Ruby', 'Scala', 'SeamGen', 'SketchUp', 'SugarCRM', 'Symfony2', 'Symfony', 'SymphonyCMS', 'Target3001', 'Tasm', 'Textpattern', 'TurboGears2', 'Unity', 'VB.Net', 'Waf', 'Wordpress', 'Yii', 'ZendFramework', 'Archives', 'CVS', 'Eclipse', 'Emacs', 'Espresso', 'FlexBuilder', 'IntelliJ', 'Linux', 'Matlab', 'Mercurial', 'ModelSim', 'MonoDevelop', 'NetBeans', 'OSX', 'Quartus2', 'Redcar', 'RubyMine', 'SASS', 'SBT', 'SublimeText', 'SVN', 'Tags', 'TextMate', 'vim', 'VisualStudio', 'Windows', 'XilinxISE']

	second_list = ['Done', 'Actionscript', 'Android', 'Autotools', 'CakePHP', 'CFWheels', 'C', 'C++', 'Clojure', 'CMake', 'CodeIgniter', 'Compass', 'Concrete5', 'Coq', 'CSharp', 'Delphi', 'Django', 'Drupal', 'Erlang', 'ExpressionEngine', 'Finale', 'ForceDotCom', 'FuelPHP', 'gcov', 'Go', 'Grails', 'GWT', 'Haskell', 'Java', 'Jboss', 'Jekyll', 'Joomla', 'Jython', 'Kohana', 'LaTeX', 'Leiningen', 'LemonStand', 'Lilypond', 'Lithium', 'Magento', 'Maven', 'nanoc', 'Node', 'Objective-C', 'OCaml', 'Opa', 'opencart', 'OracleForms', 'Perl', 'PlayFramework', 'Python', 'Qooxdoo', 'Rails', 'R', 'RhodesRhomobile', 'Ruby', 'Scala', 'SeamGen', 'SketchUp', 'SugarCRM', 'Symfony2', 'Symfony', 'SymphonyCMS', 'Target3001', 'Tasm', 'Textpattern', 'TurboGears2', 'Unity', 'VB.Net', 'Waf', 'Wordpress', 'Yii', 'ZendFramework', 'Archives', 'CVS', 'Eclipse', 'Emacs', 'Espresso', 'FlexBuilder', 'IntelliJ', 'Linux', 'Matlab', 'Mercurial', 'ModelSim', 'MonoDevelop', 'NetBeans', 'OSX', 'Quartus2', 'Redcar', 'RubyMine', 'SASS', 'SBT', 'SublimeText', 'SVN', 'Tags', 'TextMate', 'vim', 'VisualStudio', 'Windows', 'XilinxISE']


	def get_files(self):
		dir_list = os.listdir("/home/adam/Dropbox/Programming/Random/Sublime/Sublime-gitignore/boilerplates")
		count = 0
		while count < len(dir_list):
			dir_list[count] = dir_list[count].replace('.gitignore', '')
			count = count+1

		print dir_list

	def run(self):
		self.get_files
		self.window.show_quick_panel(self.first_list, self.first_select)

	def first_select(self, index):
		if index > -1:
			self.chosen_array.append(self.first_list[index])
			self.second_list.remove(self.first_list[index])
			self.window.show_quick_panel(self.second_list, self.second_select)


	def second_select(self, index):
		if index > -1:
			if index == 0:
				self.write_file()
			else:
				self.chosen_array.append(self.second_list[index])
				self.second_list.remove(self.second_list[index])
				self.window.show_quick_panel(self.second_list, self.second_select)


	def write_file(self):
		if os.path.exists(sublime.packages_path()+'/Gitignore'):
			path = sublime.packages_path()+'/Gitignore/boilerplates/'
		else:
			path = sublime.packages_path()+'/Sublime-Gitignore/boilerplates/'

		final = ''

		for bp in self.chosen_array:
			bpfile = open(path+bp+'.gitignore', 'r')
			text = bpfile.read()
			bpfile.close()

			final = final + '###'+bp+'###\n \n'+text+'\n\n'

		view = sublime.active_window().new_file()
		edit = view.begin_edit()
		view.insert(edit, 0, final)
		view.set_name('.gitignore')
		view.end_edit(edit)


		self.chosen_array = []
		self.first_list = ['Actionscript', 'Android', 'Autotools', 'CakePHP', 'CFWheels', 'C', 'C++', 'Clojure', 'CMake', 'CodeIgniter', 'Compass', 'Concrete5', 'Coq', 'CSharp', 'Delphi', 'Django', 'Drupal', 'Erlang', 'ExpressionEngine', 'Finale', 'ForceDotCom', 'FuelPHP', 'gcov', 'Go', 'Grails', 'GWT', 'Haskell', 'Java', 'Jboss', 'Jekyll', 'Joomla', 'Jython', 'Kohana', 'LaTeX', 'Leiningen', 'LemonStand', 'Lilypond', 'Lithium', 'Magento', 'Maven', 'nanoc', 'Node', 'Objective-C', 'OCaml', 'Opa', 'opencart', 'OracleForms', 'Perl', 'PlayFramework', 'Python', 'Qooxdoo', 'Rails', 'R', 'RhodesRhomobile', 'Ruby', 'Scala', 'SeamGen', 'SketchUp', 'SugarCRM', 'Symfony2', 'Symfony', 'SymphonyCMS', 'Target3001', 'Tasm', 'Textpattern', 'TurboGears2', 'Unity', 'VB.Net', 'Waf', 'Wordpress', 'Yii', 'ZendFramework', 'Archives', 'CVS', 'Eclipse', 'Emacs', 'Espresso', 'FlexBuilder', 'IntelliJ', 'Linux', 'Matlab', 'Mercurial', 'ModelSim', 'MonoDevelop', 'NetBeans', 'OSX', 'Quartus2', 'Redcar', 'RubyMine', 'SASS', 'SBT', 'SublimeText', 'SVN', 'Tags', 'TextMate', 'vim', 'VisualStudio', 'Windows', 'XilinxISE']

		self.second_list = ['Done', 'Actionscript', 'Android', 'Autotools', 'CakePHP', 'CFWheels', 'C', 'C++', 'Clojure', 'CMake', 'CodeIgniter', 'Compass', 'Concrete5', 'Coq', 'CSharp', 'Delphi', 'Django', 'Drupal', 'Erlang', 'ExpressionEngine', 'Finale', 'ForceDotCom', 'FuelPHP', 'gcov', 'Go', 'Grails', 'GWT', 'Haskell', 'Java', 'Jboss', 'Jekyll', 'Joomla', 'Jython', 'Kohana', 'LaTeX', 'Leiningen', 'LemonStand', 'Lilypond', 'Lithium', 'Magento', 'Maven', 'nanoc', 'Node', 'Objective-C', 'OCaml', 'Opa', 'opencart', 'OracleForms', 'Perl', 'PlayFramework', 'Python', 'Qooxdoo', 'Rails', 'R', 'RhodesRhomobile', 'Ruby', 'Scala', 'SeamGen', 'SketchUp', 'SugarCRM', 'Symfony2', 'Symfony', 'SymphonyCMS', 'Target3001', 'Tasm', 'Textpattern', 'TurboGears2', 'Unity', 'VB.Net', 'Waf', 'Wordpress', 'Yii', 'ZendFramework', 'Archives', 'CVS', 'Eclipse', 'Emacs', 'Espresso', 'FlexBuilder', 'IntelliJ', 'Linux', 'Matlab', 'Mercurial', 'ModelSim', 'MonoDevelop', 'NetBeans', 'OSX', 'Quartus2', 'Redcar', 'RubyMine', 'SASS', 'SBT', 'SublimeText', 'SVN', 'Tags', 'TextMate', 'vim', 'VisualStudio', 'Windows', 'XilinxISE']
def is_rails_file(file_name):
	try:
		# check to see if os.path has already been imported
		# this just needs to be something simple that will
		# raise an exception if it fails
		os.path.supports_unicode_filenames
	except Exception:
		import os.path

	path = os.path.dirname(file_name)
	file_name = os.path.basename(file_name).lower()
	name, extension = os.path.splitext(file_name)

	if name == 'gemfile':
		return True

	result = False

	# I doubt this is the most elegant way of identifying a Rails directory structure,
	# but it does work. The idea here is to work up the tree, checking at each level for
	# the existence of config/routes.rb. If it's found, the assumption is made that it's
	# a Rails app.
	while path != '':
		if os.path.exists(path + '/config/routes.rb'):
			result = True
			break
		else:
			dirs = path.split('/')
			dirs.pop()
			path = '/'.join(dirs)

	return extension in ['.rb', '.rake'] and result

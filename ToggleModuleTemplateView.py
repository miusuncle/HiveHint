import sublime_plugin
from os import path

class ToggleModuleTemplateViewCommand(sublime_plugin.WindowCommand):
	def run(self):
		window = self.window
		filename = window.active_view().file_name() or ''
		destfile = ''

		if filename.endswith('.html'):
			# basename without extension
			dirname, basename = path.split(path.splitext(filename)[0])
			# strip last pathname component(maybe `/templates`)
			dirname = path.split(dirname)[0]
			# get relevant js file
			destfile = path.sep.join([dirname, basename + '.js'])

		if filename.endswith('.js'):
			# basename without extension
			dirname, basename = path.split(path.splitext(filename)[0])
			# get relevant html file
			destfile = path.sep.join([dirname, 'templates', basename + '.html'])

		if path.isfile(destfile): window.open_file(destfile)

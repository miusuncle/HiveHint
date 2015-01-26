import sublime_plugin
from os import path

class ToggleModuleTemplateViewCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.do_exec(False)

	def is_visible(self):
		return self.do_exec(True)

	def do_exec(self, preflight):
		filename = self.get_file_name()
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

		if preflight:
			return path.isfile(destfile)
		else:
			if path.isfile(destfile):
				self.window.open_file(destfile)

	def description(self):
		filename = self.get_file_name()
		file_ext = str(path.splitext(filename)[-1])

		return ({
			'.js': 'Open Relevant Template File',
			'.html': 'Open Relevant Module File'
		}).get(file_ext, 'ignore me')

	def get_file_name(self):
		view = self.window.active_view()
		return (view.file_name() or '' if view else '')

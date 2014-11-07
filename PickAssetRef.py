import sublime, sublime_plugin
from os import path

# ============================================================
if int(sublime.version()) >= 3000:
	from .hive_loader import hive_loader
else:
	from hive_loader import hive_loader

FOLDERS = hive_loader.FOLDERS
# ============================================================

class PickAssetRefCommand(sublime_plugin.WindowCommand):
	def run(self):
		rel_path = self.get_relative_path()
		ref, ext = path.splitext(rel_path)

		if ext == '.js':
			sublime.set_clipboard(ref)
		elif ext == '.html':
			dirname, basename = path.split(rel_path)
			dirname = path.split(dirname)[-1]

			if dirname == 'templates':
				ref = './' + '/'.join([dirname, basename])
				sublime.set_clipboard(ref)

	def is_visible(self):
		rel_path = self.get_relative_path()
		if not rel_path: return False
		file_ext = path.splitext(rel_path)[-1]
		return file_ext in ['.js', '.html']

	def description(self):
		rel_path = self.get_relative_path()
		file_ext = str(path.splitext(rel_path)[-1])

		return ({
			'.js': 'Copy Module Id',
			'.html': 'Copy Relative Template Path'
		}).get(file_ext, 'HIVE, I & U')

	def get_relative_path(self):
		view = self.window.active_view()
		file_name = view.file_name() or ''
		FOLDERS.extend(self.window.folders())

		for folder in FOLDERS:
			if file_name.startswith(folder):
				file_name = file_name.partition(folder + path.sep)[-1]
				return file_name.replace('\\', '/')
		else:
			return ''

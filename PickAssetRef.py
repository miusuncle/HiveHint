import sublime, sublime_plugin
from os import path

# ============================================================
gte_st3 = int(sublime.version()) >= 3000

if gte_st3:
	from .hive_loader import hive_loader
else:
	from hive_loader import hive_loader

FOLDERS = hive_loader.FOLDERS
# ============================================================

class PickAssetRefCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.do_exec(False)

	def is_visible(self):
		return self.do_exec(True)

	def do_exec(self, preflight):
		rel_path = self.get_relative_path()
		if not rel_path: return False
		ref, ext = path.splitext(rel_path)

		if ext == '.js':
			return True if preflight else sublime.set_clipboard(ref)
		elif ext == '.html':
			dirname, basename = path.split(rel_path)
			dirname = path.split(dirname)[-1]

			if dirname == 'templates':
				ref = './' + '/'.join([dirname, basename])
				return True if preflight else sublime.set_clipboard(ref)
			else:
				return False
		else:
			return False

	def description(self):
		rel_path = self.get_relative_path()
		file_ext = str(path.splitext(rel_path)[-1])

		return ({
			'.js': 'Copy Module Id',
			'.html': 'Copy Relative Template Path'
		}).get(file_ext, 'HIVE, I & U')

	def get_relative_path(self):
		view = self.window.active_view()
		if not view: return ''

		file_name = view.file_name() or ''
		folders = self.window.folders() + FOLDERS

		for folder in folders:
			if file_name.startswith(folder):
				file_name = file_name.partition(folder + path.sep)[-1]
				return file_name.replace('\\', '/')
		else:
			return ''

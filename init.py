import sublime, sublime_plugin
from functools import partial
import os, errno

path = os.path
HIVE_NAME = 'HiveHint'
LINE_SIZE = 110

gte_st3 = int(sublime.version()) >= 3000

# ============================================================

class HiveHintEventListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		if self.file_in_hive_dir(view): view.set_read_only(False)

		file_name = view.file_name() or ''
		base_name = path.basename(file_name)

		if base_name == HIVE_NAME + '.sublime-settings':
			saved_dir = os.getcwd()

			os.chdir(sublime.packages_path())
			rel_path = path.relpath(file_name)
			dir_name = path.dirname(rel_path)

			os.chdir(saved_dir)

			if dir_name in [HIVE_NAME, 'User']:
				self.reload_plugin_async('hive_loader', 400)
				self.reload_plugin_async('PickAssetRef', 600)
				self.reload_plugin_async('ModuleIdHint', 1000)

	def reload_plugin_async(self, plugin_name, delay):
		sublime.set_timeout(partial(self.reload_plugin, plugin_name), delay)

	def reload_plugin(self, plugin_name):
		if gte_st3:
			plugin_name = '.'.join([HIVE_NAME, plugin_name])
		else:
			plugin_name = path.join(self.hive_dir(), plugin_name + '.py')

		sublime_plugin.reload_plugin(plugin_name)

	def file_in_hive_dir(self, view):
		return (view.file_name() or '').startswith(self.hive_dir())

	def hive_dir(self):
		pack_path = sublime.packages_path()
		return path.join(pack_path, HIVE_NAME) + path.sep

# ============================================================

def mkdir_p(p):
	try:
		os.makedirs(p)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST and path.isdir(p):
			pass
		else: raise

if gte_st3:
	def plugin_loaded():
		saved_dir = os.getcwd()
		print()
		print('*' * LINE_SIZE, '\nSAVING DIR: ', saved_dir)

		pack_path = sublime.packages_path()
		os.chdir(pack_path)
		print('*' * LINE_SIZE, '\nCHANGE DIR: ', pack_path)

		print('\tMAKE DIR: ', path.join(pack_path, HIVE_NAME))
		mkdir_p(HIVE_NAME)

		print('\tMAKE DIR: ', path.join(pack_path, HIVE_NAME, 'completions'))
		mkdir_p(HIVE_NAME + '/completions')

		print('*' * LINE_SIZE, '\nRESTORE DIR: ', saved_dir)
		os.chdir(saved_dir)

		print('*' * LINE_SIZE, '\n')
else:
	# intentionly do nothing with sublime text 2
	pass

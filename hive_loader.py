import sublime
from itertools import groupby
from os import path
import re

class HiveLoader():
	def __init__(self):
		self.FOLDERS = []
		self.MIDS = []

	def load(self):
		settings = sublime.load_settings('HiveHint.sublime-settings')

		# inject `FOLDERS`
		for folder in settings.get('scripts_root', []):
			folder = str(folder).rstrip('\/\\')
			if sublime.platform() == 'windows':
				folder = path.normpath(folder)
				folder = re.sub(r'^\\([A-Za-z])(?=\\)', r'\1:', folder)
			self.FOLDERS.append(folder)

		# inject `MIDS`
		for key in ('dojo_mids', 'hive_mids', 'misc_mids'):
			if settings.has(key):
				self.MIDS.extend(settings.get(key))

		# remove duplicates
		self.MIDS.sort()
		self.MIDS = list(key for key, _ in groupby(self.MIDS))

		# this should remove duplicates too, but the resulting order is messy
		# self.MIDS = list(set([tuple(mid) for mid in self.MIDS]))
		# self.MIDS = [list(mid) for mid in self.MIDS]

# ============================================================

hive_loader = HiveLoader()

if int(sublime.version()) >= 3000:
	def plugin_loaded():
		global hive_loader
		hive_loader.load()
else:
	hive_loader.load()

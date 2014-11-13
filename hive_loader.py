import sublime
from itertools import groupby

gte_st3 = int(sublime.version()) >= 3000

if gte_st3:
	from .hive_util import HiveUtil as HU
else:
	from hive_util import HiveUtil as HU

class HiveLoader():
	def __init__(self):
		self.FOLDERS = []
		self.MIDS = []

	def load(self):
		settings = sublime.load_settings('HiveHint.sublime-settings')

		# inject `FOLDERS`
		for folder in settings.get('scripts_root', []):
			self.FOLDERS.append(HU.normalize_path(folder))

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

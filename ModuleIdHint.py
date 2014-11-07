import sublime, sublime_plugin
from functools import partial

# ============================================================
if int(sublime.version()) >= 3000:
	from .hive_loader import hive_loader
else:
	from hive_loader import hive_loader

MIDS = hive_loader.MIDS
# ============================================================

class ModuleIdHintCommand(sublime_plugin.WindowCommand):
	insert_mode = None

	def run(self):
		if self.insert_mode == None: return
		self.window.show_quick_panel(MIDS, self.on_done, sublime.MONOSPACE_FONT)

	def on_done(self, index):
		if index == -1: return

		if self.insert_mode:
			sublime.set_timeout(partial(self.insert, MIDS[index]), 0)
		else:
			sublime.set_timeout(partial(self.preview, MIDS[index][0]), 0)

	def insert(self, mid_pairs):
		self.window.run_command('module_id_insertion', { 'mid_pairs': mid_pairs })

	def preview(self, text):
		self.window.run_command('show_overlay', {
			'overlay': 'goto',
			'text': text,
			'show_files': True
		})

class InsertModuleIdCommand(ModuleIdHintCommand):
	insert_mode = True

	def is_enabled(self):
		return can_insert(self.window.active_view())

class GotoModuleDefinitionCommand(ModuleIdHintCommand):
	insert_mode = False

# ============================================================

class ModuleIdInsertionCommand(sublime_plugin.TextCommand):
	def run(self, edit, mid_pairs=None):
		if not mid_pairs: return
		mid, ref = mid_pairs

		view = self.view
		selection = view.sel()
		size = len(selection)

		if size == 2:
			region = selection[0]
			renovate = getattr(view, 'insert' if region.empty() else 'replace')
			precusor = region.end() if region.empty() else region
			mid = "'" + mid + "',\n\t"
			renovate(edit, precusor, mid)

			region = selection[1]
			renovate = getattr(view, 'insert' if region.empty() else 'replace')
			precusor = region.end() if region.empty() else region
			ref and renovate(edit, precusor, ref + ', ')

		else:
			for region in selection:
				renovate = getattr(view, 'insert' if region.empty() else 'replace')
				precusor = region.end() if region.empty() else region
				renovate(edit, precusor, mid)

# ============================================================

def can_insert(view):
	sv = SyntaxViewer(view)
	return sv.is_javascript() or sv.is_html()

class SyntaxViewer():
	def __init__(self, view=None):
		self.view = view

	def is_javascript(self):
		return self.get_syntax() == 'javascript'

	def is_html(self):
		return self.get_syntax() == 'html'

	def get_syntax(self):
		syntax = self.view.settings().get('syntax')
		return syntax.split('/')[-1].split('.')[0].lower()

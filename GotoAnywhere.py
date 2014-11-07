import sublime, sublime_plugin
import re

class GotoAnywhereCommand(sublime_plugin.WindowCommand):
	def run(self, **args):
		self.gte_st3 = int(sublime.version()) >= 3000
		self.symbol_mode = args.get('symbol_mode', False)
		self.saved_view = self.window.active_view()

		region = self.save_regions()
		if region == None: return
		text = self.get_text(region)

		if self.symbol_mode:
			if self.gte_st3:
				self.goto_symbol(text)
			else:
				sublime.status_message('Please upgrade to Sublime Text 3 to use `Goto Symbol Definition` feature.')
		else:
			self.goto_anything(text)

	def save_regions(self):
		selection = self.saved_view.sel()
		# save region data as tuple so we can reverse serialization subsequently
		self.saved_regions = [(region.a, region.b) for region in selection]

		# return None if no selection(no viewable cursor)
		# otherwise we only care about the last region(regardless of multi-selection mode)
		return None if not len(selection) else selection[-1]

	def get_text(self, region):
		view = self.saved_view

		if region.empty():
			pattern = re.compile(r'^[-_|a-z|A-Z|0-9|\.|\/]$')

			while region.a >= 0:
				text = view.substr(region)
				if not text or re.match(pattern, text[0]):
					region = self.revise_region(region, -1, 0)
				else:
					region = self.revise_region(region, 1, 0)
					break

			while region.b <= view.size():
				text = view.substr(region)
				if not text or re.match(pattern, text[-1]):
					region = self.revise_region(region, 0, 1)
				else:
					region = self.revise_region(region, 0, -1)
					break

			text = view.substr(region)

			if self.symbol_mode:
				# get the last part splitted by dot
				text = text.split('.')[-1]

		else:
			text = view.substr(region)

		return text.strip('\/.\n')[:100]

	def revise_region(self, region, inc_a, inc_b):
		if self.gte_st3:
			region.a += inc_a
			region.b += inc_b

		# sublime text 2 does not support change region's border directly
		# so we generate a new instance to accommodate
		else:
			region = sublime.Region(region.a + inc_a, region.b + inc_b)

		return region

	def goto_anything(self, text):
		self.window.run_command('show_overlay', {
			'overlay': 'goto',
			'text': text,
			'show_files': True
		})

	def goto_symbol(self, symbol):
		window = self.window
		view = self.saved_view

		locations = window.lookup_symbol_in_index(symbol)
		locations.extend(window.lookup_symbol_in_open_files(symbol))

		# remove duplicates
		locations = list(set(locations))

		if not locations:
			sublime.status_message('Unable to find ' + symbol)
		else:
			settings = sublime.load_settings('HiveHint.sublime-settings')
			prefer_dart = settings.get('prefer_dart', True)

			locations = self.sorted_locations(locations)
			self.locations = locations

			if prefer_dart and len(locations) == 1:
				self.open_file(0)
			else:
				window.show_quick_panel(
					[str.join(':', [l[1], str(l[2][0])]) for l in locations],
					self.on_done,
					on_highlight=self.on_highlight
				)

	def sorted_locations(self, locations):
		view_name = self.view_name()
		untitled = re.compile(r'^<untitled \d+>$')

		# normalized file path if current file is not untitled and platform is windows
		if not re.match(untitled, view_name) and sublime.platform() == 'windows':
			view_name = '/' + view_name.replace('\\', '/').replace(':', '')

		for (index, location) in enumerate(locations):
			if index != 0 and location[0] == view_name:
				# symbol found in current file should be shown prior than others
				locations.insert(0, locations.pop(index))

		return locations

	def on_done(self, index):
		self.restore_regions() if index == -1 else self.open_file(index)

	def restore_regions(self):
		saved_view = self.saved_view

		# removes all regions currently if has any
		sublime.Selection.clear(saved_view)

		# restore previous saved regions
		for region in self.saved_regions:
			sublime.Selection.add(saved_view, sublime.Region(*region))

		# focus on previous saved view
		self.window.focus_view(saved_view)

		# scroll the view to center on the last region
		saved_view.show_at_center(saved_view.sel()[-1])

	def on_highlight(self, index):
		self.open_file(index, preview=True)

	def open_file(self, index, preview=False):
		flags = sublime.ENCODED_POSITION
		if preview: flags |= sublime.TRANSIENT

		location_name = self.location_name(self.locations[index])
		self.window.open_file(location_name, flags)

	def location_name(self, location):
		file_name, _, (row, col) = location
		return str.join(':', [file_name, str(row), str(col)])

	def view_name(self, view=None):
		view = view or self.saved_view
		return view.file_name() or '<untitled %d>' % view.buffer_id()

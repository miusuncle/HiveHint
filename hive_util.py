import sublime, re, os

class HiveUtil:
	@staticmethod
	def normalize_path(path):
		path = str(path).rstrip('\/\\')

		if sublime.platform() == 'windows':
			path = os.path.normpath(path)
			path = re.sub(r'^\\([A-Za-z])(?=\\)', r'\1:', path)

		return path

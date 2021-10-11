import re

from octoprint_autobim.async_command import AsyncCommand


class G30Handler(AsyncCommand):
	def __init__(self, printer):
		super(G30Handler, self).__init__()
		self._printer = printer
		# TODO: Move pattern to settings
		self.pattern = re.compile(r"^Bed X: -?\d+\.\d+ Y: -?\d+\.\d+ Z: (-?\d+\.\d+)$")

	def do(self, point, timeout=180):
		self._start(point)
		return self._get(timeout)

	def _start(self, point):
		self._set_running()
		self._printer.commands("G30 X%s Y%s" % point)

	def _handle_internal(self, line):
		if "ok" == line:
			self._register_result(float('nan'))
			return

		match = self.pattern.match(line)
		if match:
			self._register_result(float(match.group(1)))

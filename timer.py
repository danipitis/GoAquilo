# timer.py Version 1.0.0
# This is part of GoAquilo game
# Copyright (c) Pitis Daniel <pitis.dan@gmail.com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import datetime

class Timer:
	""" Timer class used to set fire state of the player for a given amount of time"""
	start_clock = datetime.datetime.now()
	end_clock   = datetime.datetime.now()

	def start(self):
		self.start_clock = datetime.datetime.now()

	def end(self):
		self.end_clock = datetime.datetime.now()

	def check_difference(self, time_period):
		difference = self.end_clock - self.start_clock

		if difference.microseconds >= time_period:
			return False
		else:
			return True
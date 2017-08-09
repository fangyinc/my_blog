#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import ceil

class Pagination:

	def __init__(self, page, per_page, total_count):
		self.page = page
		self.per_page = per_page
		self.total_count = total_count

	@property
	def pages(self):
		return int(ceil(self.total_count / float(self.per_page)))

	@property
	def has_prev(self):
		return self.page > 1

	@property
	def has_next(self):
		return self.page < self.pages

	@property
	def prev_num(self):
		return self.page - 1
	@property
	def next_num(self):
		return self.per_page + 1

	def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
		last = 0
		for num in range(1, self.pages + 1):
			if num <= left_edge or (num > self.page - left_current - 1 and
				num < self.page + right_current) or num > self.pages - right_edge:
				if last + 1 != num:
					yield None
				yield num
				last = num


class PageItem:
	def __init__(self, page, per_page, data, count):
		self.pages = (int(page)-1)*int(per_page)
		self.per_page = int(per_page)
		self.data = data
		self.count = int(count)
	def get_item(self):	#data 是可迭代对象
		if (self.count - self.pages) / self.per_page >=1:
			return self.data[self.pages:self.pages+self.per_page]
		else:
			return self.data[self.pages:]

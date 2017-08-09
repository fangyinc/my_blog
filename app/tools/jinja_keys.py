#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from .. import files, db
from flask import current_app
from ..models import User, Category, Spc, Tag, Post,Friend
from ..post.posts import Archive

class JinjaKeys:
	def __init__(self):
		self.re_keys={}

	def _base_keys(self):
		arch_obj = Archive()
		admin_user = User.query.filter_by(email=current_app.config['FLASKY_ADMIN']).first()
		cats = Category.query.all()
		spcs = Spc.query.all()
		archive = arch_obj.get_post()
		friends = Friend.query.all()
		temp_keys={
				'admin_user': admin_user,			#管理员
				'cats':cats,						#分类
				'spcs': spcs,						#专栏
				'archive': archive,					#归档
				'friends': friends,					#友链
				'Tag': Tag							#标签
		}

		return temp_keys
	def add_keys(self, data):
		self.re_keys.update(data)

	def keys(self):
		self.re_keys.update(self._base_keys())
		return self.re_keys

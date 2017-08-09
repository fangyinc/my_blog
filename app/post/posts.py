#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from .. import files, db
from ..models import Post, Tag, Category, Spc, User, R_Post_Tag
import time
import hashlib
from pypinyin import lazy_pinyin

class save_post:
	def __init__(self, title, spc, category, tags, summary, md_data, html_data):
		try:
			self.title = title.data
			self.spc = spc.data
			self.category = category.data
			self.tags = [s for s in tags.data.strip().split(' ') if s != '']
			self.summary = summary.data
			self.md_data = md_data.data
			self.html_data = html_data.data
			#self.post = self.get_post()
		except:
			print('error at init sava_post')
			raise

	def save(self):
		try:
			post = self.get_post()
			post.body = self.md_data
			post.body_html = self.html_data
			post.category = self.get_category()
			post.spc = self.get_spc()
			post.summary = self.summary
			#post.author = User.query.filter_by(id=self.author_id).first()
			db.session.add(post)
			db.session.commit()
			tags = self.get_tags()
			#old_tags = post.tags.all()
			old_tags = Tag.query.join(R_Post_Tag, R_Post_Tag.tag_id == Tag.id).filter_by(post_id=post.id).all()
			ax_tags = [a for a in old_tags if a not in tags]
			for tag in ax_tags:
				t = Tag.query.filter_by(name=tag.name).first()
				r = R_Post_Tag.query.filter_by(tag_id=t.id, post_id=post.id).first()
				db.session.delete(r)
				db.session.commit()
			for tag in tags:
				if post.tags.filter_by(tag_id=tag.id).first() is None:
					r = R_Post_Tag(post_id=post.id, tag_id=tag.id)
					db.session.add(r)
					db.session.commit()
			db.session.add(post)
			db.session.commit()
		except:
			print('error at sava')
			raise
		return True

	def get_post(self):
		post = Post.query.filter_by(title=self.title).first()
		if post == None:
			post = Post(title=self.title)
			db.session.add(post)
			db.session.commit()
		return post
	def get_spc(self):
		spc = Spc.query.filter_by(name=self.spc).first()
		if spc == None:
			spc = Spc(name=self.spc)
			db.session.add(spc)
			db.session.commit()
		return spc
	def get_category(self):
		cat = Category.query.filter_by(name=self.category).first()
		if cat == None:
			cat = Category(name=self.category)
			db.session.add(cat)
			db.session.commit()
		return cat
	def get_tags(self):
		tags=[]
		for name in self.tags:
			tag = Tag.query.filter_by(name=name).first()
			if tag == None:
				tag = Tag(name=name)
				db.session.add(tag)
				db.session.commit()
			tags.append(tag)
		return tags

class Archive:
	def __init__(self):
		self.posts = Post.query.order_by(Post.timestamp.desc()).all()
	def get_post(self):
		re_posts = [[]]
		posts = self.posts
		if len(posts) == 0:
			return re_posts
		re_posts[0].append(posts[0])
		j = 0
		for i in range(1, len(posts)):
			if (posts[i].timestamp.year == posts[i-1].timestamp.year) and \
					(posts[i].timestamp.month == posts[i-1].timestamp.month) and\
					(posts[i].timestamp.day == posts[i-1].timestamp.day):
				re_posts[j].append(posts[i])
			else:
				temp=[]
				temp.append(posts[i])
				re_posts.append(temp)
				j += 1
		return re_posts
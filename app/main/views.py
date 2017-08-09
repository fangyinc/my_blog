# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from .. import files
from . import main
from ..models import  Post, Tag, Category, Spc, User
from ..post.posts import Archive
from ..tools.jinja_keys import  JinjaKeys
from ..decorators import  admin_required
import os

@main.route('/')
def index():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	posts = pagination.items

	value = JinjaKeys()
	value.add_keys({'posts': posts, 'pagination': pagination})
	my_dict = value.keys()

	return render_template('index.html', **my_dict)

@main.route('/admin-images/', defaults={'page': 1})
@main.route('/admin-images/<int:page>')
@admin_required
def admin_images(page):
	from ..tools.pagination import Pagination, PageItem
	PER_PAGE = 20
	all_file = os.listdir(current_app.config['UPLOADED_FILES_DEST'])
	count = len(all_file)

	page_item = PageItem(page, PER_PAGE, all_file, count)
	files_list = page_item.get_item()
	pagination = Pagination(page, PER_PAGE, count)

	return render_template('admin/admin_images.html', pagination=pagination,
						   files_list=files_list, files=files)

@main.route('/delete-image/<filename>')
@admin_required
def delete_image(filename):
	file_path = files.path(filename)
	os.remove(file_path)
	return redirect(url_for('main.admin_images'))

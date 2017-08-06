# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from ..models import  Post, Tag, Category, Spc
from ..post.posts import Archive

@main.route('/')
def index():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	posts = pagination.items
	cats = Category.query.all()
	spcs = Spc.query.all()
	arch_obj = Archive()
	archive = arch_obj.get_post()
	return render_template('index.html', pagination=pagination,
			posts=posts, archive=archive, Tag=Tag, cats=cats, spcs=spcs)

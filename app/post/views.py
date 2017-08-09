# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, abort, flash, request,\
	current_app, make_response, jsonify

from flask import request
from werkzeug.contrib.atom import AtomFeed
from .forms import PostForm
from . import post
from .. import db
import os
from .. import files
from ..models import  Post, Tag, Category, R_Post_Tag, Spc, User
from ..decorators import author_required, admin_required
from .posts import Archive
from ..tools.jinja_keys import JinjaKeys

@post.route('/feed')
def atom_feed():
	feed = AtomFeed("My Blog", feed_url=request.url,
					url=request.host_url,
					subtitle="My example blog for a feed test.")
	for post in Post.query.limit(10).all():
		feed.add(post.title, post.body, content_type='html',
				 author='hello', url='#', id=post.id,
				 updated=post.timestamp, published='#')
	return feed.get_response()

@post.route('/upload', methods=['GET', 'POST'])
@admin_required
def upload():
	form = PostForm()
	if form.validate_on_submit():
		from .posts import save_post
		my_post = save_post(form.title, form.spc, form.category, form.tags,
							form.summary, form.md_data, form.md_data)
		if my_post.save() is not True:
			print('error at my_post.save')
			return render_template('500.html')
		post = Post.query.filter_by(title=form.title.data).first()
		return redirect(url_for('post.show_post', id=post.id))

	return render_template('post/upload.html', form=form)


@post.route('/img_upload/', methods=['GET', 'POST'])
def img_upload():
	'''
	editormd编辑器图片上传, 通过flask_uploads处理文件，
	flask_uploads上传配置分别在'config.py'和'app/__init__.py'文件中
	'''
	if request.method == 'POST':
		try:
			import hashlib, time
			name = hashlib.md5(('staneyffer' + str(time.time())).encode('utf-8')).hexdigest()[:15]
			file = request.files['editormd-image-file']
			filename = files.save(file, name=name+'.')
			file_url = files.url(filename)
		except Exception as e:
			return jsonify({'success': 0, 'message': e, 'url': ''})
		return jsonify({'success':1,'message':'upload success', 'url':file_url})
	return jsonify({'success':0,'message':'upload fail', 'url':''})

@post.route('/<int:id>')
def show_post(id):
	post = Post.query.get_or_404(id)
	value = JinjaKeys()
	value.add_keys({'post': post})
	my_dict = value.keys()
	return render_template('post/post.html', **my_dict)

@post.route('/md/<int:id>')
@admin_required
def get_md(id):
	post = Post.query.get_or_404(id)
	return render_template('post/get_resouces.html', post=post.body)

@post.route('/sum/<int:id>')
@admin_required
def get_sum(id):
	post = Post.query.get_or_404(id)
	return render_template('post/get_resouces.html', post=post.summary)

@post.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_post(id):
	form = PostForm()
	post = Post.query.get_or_404(id)
	tags_obj = Tag.query.join(R_Post_Tag, R_Post_Tag.tag_id==Tag.id).filter_by(post_id=post.id)

	tags=''
	for tag in tags_obj:
		tags +=tag.name + ' '

	if form.validate_on_submit():
		from .posts import save_post
		my_post = save_post(form.title, form.spc, form.category, form.tags,
							form.summary, form.md_data, form.md_data)
		if my_post.save() is not True:
			print('error at my_post.save')
			return render_template('500.html')
		post = Post.query.filter_by(title=form.title.data).first()
		return redirect(url_for('post.show_post', id=post.id))

	form.title.data = post.title
	form.spc.data = post.spc.name
	form.category.data = post.category.name
	form.summary.data = post.summary
	form.md_data.data = post.body
	form.tags.data = tags
	#value = JinjaKeys()
	#value.add_keys({'post':post})
	my_dict = {'post':post}

	return render_template('post/edit_post.html', form=form, **my_dict)

@post.route('/category/<int:id>', defaults={'page': 1},  methods=["POST", "GET"])
@post.route('/category/<int:id>/<int:page>', methods=["POST", "GET"])
def get_category(page, id):
	category = Category.query.get_or_404(id)
	posts_q = category.posts

	pagination = posts_q.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	posts = pagination.items

	value = JinjaKeys()
	value.add_keys({'posts':posts, 'id': id, 'site_url':'post.get_category',
					'pagination': pagination})
	my_dict = value.keys()
	count = len(posts_q.all())
	return render_template('post/show_posts.html', the_category=category,
						   count=count, **my_dict)

@post.route('/spc/<int:id>', defaults={'page': 1},  methods=["POST", "GET"])
@post.route('/spc/<int:id>/<int:page>', methods=["POST", "GET"])
def get_spc(page, id):
	spc = Spc.query.get_or_404(id)
	posts_q = spc.posts

	pagination = posts_q.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	posts = pagination.items

	value = JinjaKeys()
	value.add_keys({'posts':posts, 'id': id, 'site_url':'post.get_spc',
					'pagination': pagination})
	my_dict = value.keys()
	count = len(posts_q.all())
	return render_template('post/show_posts.html', the_spc=spc,
						   count=count, **my_dict)

@post.route('/tag/<int:id>', defaults={'page': 1},  methods=["POST", "GET"])
@post.route('/tag/<int:id>/<int:page>', methods=["POST", "GET"])
def get_tag(page, id):
	tag = Tag.query.get_or_404(id)
	posts_q = Post.query.join(R_Post_Tag, R_Post_Tag.post_id==Post.id).filter_by(tag_id=tag.id)
	pagination = posts_q.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	posts = pagination.items
	#tags = Tag.query.join(R_Post_Tag, R_Post_Tag.tag_id==Tag.id).filter_by(post_id=post.id).all()

	value = JinjaKeys()
	value.add_keys({'posts':posts, 'id': id, 'site_url':'post.get_tag',
					'pagination': pagination})
	my_dict = value.keys()
	count = len(posts_q.all())
	return render_template('post/show_posts.html', the_tag=tag,
						   count=count, **my_dict)

@post.route('/archive')
def get_archive():
	value = JinjaKeys()
	my_dict = value.keys()
	return render_template('post/archive.html', **my_dict)

@post.route('/category/delete/<int:id>')
@admin_required
def delete_cat(id):
	item = Category.query.get_or_404(id)
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('main.index'))


@post.route('/tag/delete/<int:id>')
@admin_required
def delete_tag(id):
	item = Tag.query.get_or_404(id)
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('main.index'))


@post.route('/spc/delete/<int:id>')
@admin_required
def delete_spc(id):
	item = Spc.query.get_or_404(id)
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('main.index'))


@post.route('/delete/<int:id>')
@admin_required
def delete_post(id):
	item = Post.query.get_or_404(id)
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('main.index'))

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from .. import db
from ..models import User, Category, Spc, Tag, Post,Friend
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,EditProfileAdminForm, FriendForm
from ..decorators import author_required, admin_required
from ..post.posts import Archive
from ..tools.jinja_keys import JinjaKeys

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		print("get data")
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('用户名或密码错误.')
	return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('您已经退出')
	return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
@admin_required		#注册保护
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('您已经成功注册')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@admin_required
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			flash('老铁，密码已经更新')
			return redirect(url_for('main.index'))
		else:
			flash('密码不对呀，老铁.')
	return render_template("auth/change_password.html", form=form)

'''
@auth.route('/admin')
@login_required
@admin_required
def admin_user():
	page = request.args.get('page', 1, type=int)
	pagination = User.query.paginate(
		page, per_page=20,
		error_out=False)
	users = pagination.items
	return render_template('admin_user.html', paths=users,
						   pagination=pagination)
'''

@auth.route('/info/<int:id>')
@admin_required
def get_about_me(id):
	user = User.query.get_or_404(id)
	return render_template('post/get_resouces.html', post=user.about_me)

@auth.route('/about-me')
def auth_get_user():
	user = User.query.filter_by(email='staneyffer@gmail.com').first()
	value = JinjaKeys()
	value.add_keys({'user': user})
	my_dict = value.keys()

	return render_template('auth/about_me.html', **my_dict)


@auth.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm()
	if form.validate_on_submit():
		user.username = form.username.data
		user.name = form.name.data
		user.img_url = form.img_url.data
		user.bg_img_url = form.bg_img_url.data
		user.signature = form.signature.data
		user.about_me = form.about_me.data.strip(' ')
		db.session.add(user)
		flash('用户信息已更新')
		return redirect(url_for('.auth_get_user'))
	form.username.data = user.username
	form.name.data = user.name
	form.img_url.data = user.img_url
	form.bg_img_url.data =user.bg_img_url
	form.signature.data = user.signature
	form.about_me.data = user.about_me
	return render_template('auth/edit_profile.html', form=form, user=user)



@auth.route('/add-friend', methods=['GET', 'POST'])
@login_required
@admin_required
def add_friend():
	#user = User.query.get_or_404(id)
	form = FriendForm()
	if form.validate_on_submit():
		user = Friend(name=form.name.data,
					site_url=form.site_url.data,
					img_url=form.img_url.data)
		db.session.add(user)
		db.session.commit()
		flash('成功添加友链')
		return redirect(url_for('main.index'))
	return render_template('auth/add_friend.html', form=form)


@auth.route('/edit-friend/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_friend(id):
	user = Friend.query.get_or_404(id)
	form = FriendForm()
	if form.validate_on_submit():
		user.name = form.name.data
		user.site_url = form.site_url.data
		user.img_url = form.img_url.data
		user.about_me = form.about_me.data
		db.session.add(user)
		db.session.commit()
		flash('成功修改友链')
		return redirect(url_for('main.index'))
	form.name.data = user.name
	form.site_url.data = user.site_url
	form.img_url.data = user.img_url
	form.about_me.data = user.about_me

	return render_template('auth/add_friend.html', form=form, user=user)


@auth.route('/delete-friend/<int:id>')
@login_required
@admin_required
def delete_friend(id):
	user=Friend.query.get_or_404(id)
	db.session.delete(user)
	db.session.commit()
	flash('成功删除用户')
	return redirect(url_for('main.index'))

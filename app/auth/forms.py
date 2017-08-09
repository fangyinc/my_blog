# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
	email = StringField('邮箱', validators=[Required(), Length(1, 64),
											 Email()])
	password = PasswordField('密码', validators=[Required()])
	remember_me = BooleanField('记住我')
	submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
	email = StringField('邮箱', validators=[Required(), Length(1, 64),
										   Email()])
	username = StringField('用户名', validators=[Length(0, 64)])
	password = PasswordField('密码', validators=[
		Required(), EqualTo('password2', message='您的密码必须一致')])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('该邮箱已存在')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('该用户名已被使用')


class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('原密码', validators=[Required()])
	password = PasswordField('新密码', validators=[
		Required(), EqualTo('password2', message='密码不一致')])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('更新密码')

class EditProfileAdminForm(FlaskForm):
	#IMG_URl TODO
	username = StringField('用户名', validators=[
		Required(), Length(1, 64)])
	name = StringField('真名', validators=[Length(0, 64)])
	#gender = StringField('性别', validators=[Length(0, 64)])
	#age = StringField('年龄', validators=[Length(0, 64)])
	#location = StringField('地址', validators=[Length(0, 64)])
	img_url = StringField('头像url')
	bg_img_url = StringField('背景图片url')
	signature = StringField('个性签名')
	about_me = TextAreaField('')
	#submit = SubmitField('提交')

class FriendForm(FlaskForm):
	name = StringField('用户名', validators=[
		Required(), Length(1, 64)])
	site_url = StringField('网站url')
	img_url = StringField('头像url')
	about_me = StringField('简介')
	submit = SubmitField('提交')

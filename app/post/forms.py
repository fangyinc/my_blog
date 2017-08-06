# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, SelectMultipleField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User, Category
from .. import files
class PostForm(FlaskForm):
	title = StringField('标题', validators=[Required(), Length(1, 64)])
	spc = StringField('专栏')
	category = StringField('分类', validators=[Required(), Length(1, 64)])
	tags = StringField('标签', validators=[Required(), Length(1, 64)])	#用空格分割
	summary = TextAreaField('简介', validators=[Required(), Length(1, 500)])
	md_data = TextAreaField('', validators=[Required()])


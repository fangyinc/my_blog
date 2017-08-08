# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager

from sqlalchemy.dialects.mysql import LONGTEXT, YEAR


class Permission:
	VISITOR = 0x01
	WRITE_ARTICLES = 0x02
	ADMINISTER = 0x80


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')

	@staticmethod
	def insert_roles():
		roles = {
			'Visitor': (Permission.VISITOR, True),
			'Author': (Permission.VISITOR | Permission.WRITE_ARTICLES, False),
			'Administrator': (0xff, False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()

	def __repr__(self):
		return '<Role %r>' % self.name


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean, default=False)
	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())			#个人介绍
	signature = db.Column(db.Text())		#个人签名
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
	avatar_hash = db.Column(db.String(32))
	img_url = db.Column(db.String(256), unique = True, index = True)
	#bg_img_url = db.Column(db.String(256), unique = True, index = True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	hello = db.relationship('Post', backref='author', lazy='dynamic')


	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['FLASKY_ADMIN']:
				self.role = Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()
		if self.email is not None and self.avatar_hash is None:
			self.avatar_hash = hashlib.md5(
				self.email.encode('utf-8')).hexdigest()

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def reset_password(self, new_password):
		self.password = new_password
		db.session.add(self)
		return True

	def can(self, permissions):
		return self.role is not None and \
			(self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.ADMINISTER)

	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)

	def gravatar(self, size=100, default='identicon', rating='g'):
		if request.is_secure:
			url = 'https://secure.gravatar.com/avatar'
		else:
			url = 'http://www.gravatar.com/avatar'
		hash = self.avatar_hash or hashlib.md5(
			self.email.encode('utf-8')).hexdigest()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
			url=url, hash=hash, size=size, default=default, rating=rating)

	def to_json(self):
		json_user = {
			'url': url_for('api.get_user', id=self.id, _external=True),
			'email': self.email,
			'username': self.username,
			'name': self.name,
			'member_since': self.member_since,
			'signature': self.signature,
			'about_me': self.about_me,
			'gravatar': self.gravatar(),
			'img_url': self.img_url,
			'last_seen': self.last_seen,
			'posts': url_for('api.get_user_posts', id=self.id, _external=True),
			'post_count': self.posts.count()
		}
		return json_user

	def __repr__(self):
		return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class R_Post_Tag(db.Model):
	__tablename__ = 'r_post_tag'
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
	tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), index=True)
	body = db.Column(db.Text)			#md or rst
	body_html = db.Column(LONGTEXT)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
	spc_id = db.Column(db.Integer, db.ForeignKey('spc.id'))		#专栏
	summary = db.Column(db.Text)			#简介
	tags = db.relationship('R_Post_Tag',
							foreign_keys=[R_Post_Tag.post_id],
							backref=db.backref('posts', lazy='joined'),
							lazy='dynamic',  # 不返回记录，而是返回查询对象
							cascade='all, delete, delete-orphan',  # 销毁联接
							)
	@staticmethod
	def generate_fake(count=100):
		from random import seed, randint
		import forgery_py

		seed()
		user_count = User.query.count()
		for i in range(count):
			u = User.query.offset(randint(0, user_count - 1)).first()
			p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
					 timestamp=forgery_py.date.date(True),
					 author=u)
			db.session.add(p)
			db.session.commit()

	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
						'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
						'h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify(bleach.clean(
			markdown(value, output_format='html'),
			tags=allowed_tags, strip=True))

	def to_json(self):
		json_post = {
			'url': url_for('api.get_post', id=self.id, _external=True),
			'body': self.body,
			'body_html': self.body_html,
			'timestamp': self.timestamp,
			'author': url_for('api.get_user', id=self.author_id,
							  _external=True),
			'comments': url_for('api.get_post_comments', id=self.id,
								_external=True),
			'comment_count': self.comments.count()
		}
		return json_post

	@staticmethod
	def from_json(json_post):
		body = json_post.get('body')
		if body is None or body == '':
			raise ValidationError('post does not have a body')
		return Post(body=body)


db.event.listen(Post.body, 'set', Post.on_changed_body)

class Category(db.Model):
	__tablename__ = 'categorys'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	posts = db.relationship('Post', backref='category', lazy='dynamic')

class Tag(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	posts = db.relationship('R_Post_Tag',
							foreign_keys=[R_Post_Tag.tag_id],
							backref=db.backref('tags', lazy='joined'),
							lazy='dynamic',  # 不返回记录，而是返回查询对象
							cascade='all, delete, delete-orphan',  # 销毁联接
							)

class Spc(db.Model):			#专栏
	__tablename__ = 'spc'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), index=True, unique=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	posts = db.relationship('Post', backref='spc', lazy='dynamic')

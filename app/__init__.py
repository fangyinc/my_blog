# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_material import Material
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, ALL, patch_request_class, IMAGES
from flask_assets import Bundle, Environment
import os



bootstrap = Bootstrap()
material = Material()
moment = Moment()
db = SQLAlchemy()
files = UploadSet('files', IMAGES)
assets_env = Environment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	material.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	assets_env.init_app(app)

	#assets 管理静态文件
	from .util.assets import bundle
	assets_env.register(bundle)

	#upload file
	configure_uploads(app, files)
	patch_request_class(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/admin')

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .category import category as category_blueprint
	app.register_blueprint(category_blueprint, url_prefix='/category')

	from .post import post as post_blueprint
	app.register_blueprint(post_blueprint, url_prefix='/post')

	from .tag import tag as tag_blueprint
	app.register_blueprint(post_blueprint, url_prefix='/tag')

	from .tools import tools as tools_blueprint
	app.register_blueprint(tools_blueprint, url_prefix='/tools')

	from .api_1_0 import api as api_1_0_blueprint
	app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

	return app

#angularJS Vue.js React
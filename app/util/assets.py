#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_assets import Bundle, Environment

bundle ={
	'main_css': Bundle(
		#'css/lib/materialize.min.css',
		'css/base_style.css',
		output='gen/main.css',
		filters='cssmin'
	),
	'main_js': Bundle(
		'js/lib/jquery-2.1.1.min.js',
		#'js/lib/materialize.min.js',
		'js/base.js',
		output='gen/main.js',
		filters='jsmin'
	),
	'md_css': Bundle(
		'css/lib/md_codehilite.css',
		'css/lib/katex.css',
		output='gen/md.css',
		filters='cssmin'
	),
	'md_js': Bundle(
		'js/lib/katex.js',
		output='gen/md.js',
		filters='jsmin'
	),
	'editormd_css': Bundle(
		'editormd/css/editormd.css',
		'editormd/lib/codemirror/theme/base16-dark.css',
		output='gen/editormd.css',
		filters='cssmin'
	),
	'editormd_js': Bundle(
		'editormd/editormd.js',
		'js/use_editormd.js',
		output='gen/editormd.js',
		filters='jsmin'
	),
	'show_editormd_css': Bundle(
		#'editormd/examples/css/style.css',
		#'editormd/lib/codemirror/codemirror.min.css',
		#'editormd/lib/codemirror/addon/dialog/dialog.css',
		#'editormd/lib/codemirror/addon/fold/foldgutter.css',
		'editormd/css/editormd.preview.css',
		output='gen/show_editormd.css',
		filters='cssmin'
	),
	'show_editormd_js': Bundle(
		#'editormd/examples/js/jquery.min.js',
		'editormd/lib/codemirror/codemirror.min.js',
		'editormd/lib/codemirror/modes.min.js',
		'editormd/lib/codemirror/addons.min.js',

		'editormd/lib/marked.min.js',
		'editormd/lib/prettify.min.js',
		'editormd/lib/raphael.min.js',
		'editormd/lib/underscore.min.js',
		'editormd/lib/flowchart.min.js',
		'editormd/lib/jquery.flowchart.min.js',
		'editormd/lib/sequence-diagram.min.js',
		'editormd/editormd.js',
		#'js/use_editormd.js',
		output='gen/show_editormd.js',
		filters='jsmin'
	)
}


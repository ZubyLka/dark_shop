# -*- coding: utf-8 -*-

from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Item
from app.forms import LoginForm, RegistrationForm, SearchingForm
from werkzeug.urls import url_parse
from app import db

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = 'qweqeqe', 
	items=['qqqq' , 'wwww']
	return render_template('index.html', title='Home', items=items)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Неверный логин или пароль')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, cash=1000, vip=0)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Поздравляем, теперь вы зарегистрированы!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route('/shop', methods=['GET', 'POST'])
@login_required
def shop():
	items_temp = []
	if current_user.is_authenticated:
		items_temp = Item.query.all()
		items = []
		for item in items_temp:
			if not item.is_vip:
				items.append(item)
		return render_template('shop.html', title='Shop', items=items)


@app.route('/vip', methods=['GET', 'POST'])
@login_required
def vip():
	items_temp = []
	if current_user.is_authenticated:
		if not current_user.vip:
			return redirect(url_for('shop'))
			
		items_temp = Item.query.all()
		items = []
		for item in items_temp:
			if item.is_vip:
				items.append(item)


	return render_template('vip.html', title='Vip Shop', items=items)



@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	items = []
	form = SearchingForm()
	if form.validate_on_submit():
		#item = request.args.get('item', default = 1, type = int)
		item = form.item_id.data
		print(Item.query.get(item))
		print(type(Item.query.get(item)))
		items.append(Item.query.get(item))
	return render_template('search.html', title='Search', items=items, form=form)

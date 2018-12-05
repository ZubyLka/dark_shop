from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


item_identifier = db.Table('item_identifier',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('item_id', db.Integer, db.ForeignKey('items.item_id'))
)

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	cash = db.Column(db.Integer)
	vip = db.Column(db.Boolean)
	items = db.relationship("Item", secondary=item_identifier)


	def __repr__(self):
		return '<User {}>'.format(self.username) 

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))



class Item(db.Model):
	__tablename__ = 'items'
	item_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(140))
	description = db.Column(db.String(1024))
	is_vip = db.Column(db.Boolean)
	price = db.Column(db.Integer)

	def __repr__(self):
		return '<Item {}>'.format(self.name)


#user = User()
#item = Item()
#user.items.append(item)
#db.session.add(user)
#db.session.commit()
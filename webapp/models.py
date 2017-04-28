from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
#from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

# engine = create_engine('sqlite:///database.db', echo=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()

# # Set your classes here.

# '''
# class User(Base):
#     __tablename__ = 'Users'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), unique=True)
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column(db.String(30))

#     def __init__(self, name=None, password=None):
#         self.name = name
#         self.password = password
# '''

# # Create tables.
# Base.metadata.create_all(bind=engine)

db = SQLAlchemy(app)

class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class Admin(db.Model):
	__tablename__ = 'admin_'
	admin_ = db.Column(db.String(30), primary_key=True)
	pwd = db.Column(db.String(30))
	def check_password(self, password):
		return True if self.pwd == password else False

class Team(db.Model, Serializer):
	__tablename__ = 'team'
	#__public__ = ('name', 'location', 'logo', 'webpage', 'mascot', 'mascoticon', 'stadium', 'conference')
	name = db.Column(db.String(50))
	team_name_abbr = db.Column(db.String(3), primary_key=True)
	location = db.Column(db.String(50))
	logo = db.Column(db.String(200))
	webpage = db.Column(db.String(200))
	mascot = db.Column(db.String(200))
	mascoticon = db.Column(db.String(200))
	stadium = db.Column(db.String(100))
	conference = db.Column(db.String(1))

	def serialize(self):
		d = Serializer.serialize(self)
		return d

# class Games(db.Model):
#	__tablename__ = 'games'
# 	pass

# class Players(db.Model):
#	__table__ = 'players'
# 	pass

class Seasons(db.Model):
	__tablename__ = 'seasons'
	s_id = db.Column(db.String(7), primary_key=True)
	lg = db.Column(db.String(3))
	champion = db.Column(db.String(30))
	mvp = db.Column(db.String(30))
	best_rookie = db.Column(db.String(30))
	score_leader = db.Column(db.String(30))
	reb_leader = db.Column(db.String(30))
	ass_leader = db.Column(db.String(30))
	win_share_leader = db.Column(db.String(30))

	def get_score_leader_name():
		return score_leader.split('(')[0].strip()

	def get_score_leader_stat():
		return score_leader.split('(')[1][:-1]

	def get_reb_leader_name():
		return reb_leader.split('(')[0].strip()

	def get_reb_leader_stat():
		return reb_leader.split('(')[1][:-1]

	def get_ass_leader_name():
		return ass_leader.split('(')[0].strip()

	def get_ass_leader_stat():
		return ass_leader.split('(')[1][:-1]

	def get_ws_leader_name():
		return win_share_leader.split('(')[0].strip()

	def get_ws_leader_stat():
		return win_share_leader.split('(')[1][:-1]


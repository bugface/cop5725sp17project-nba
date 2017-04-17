from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#oracle://xiyang:alex1988@cise.ufl.edu:1521/orcl

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://xiyang:alex1988@oracle.cise.ufl.edu:1521/orcl'

@app.route("/")
def index():
	res = Continent.query.all()
	a = []
	for each in res:
		a.append(each.getName())
	return "<h1>" + " ".join(a) + "</h1>"


class Continent(db.Model):
	name = db.Column(db.String(20), primary_key = True)
	#area = db.column(db.Integer)

	def __init__(self, name, area):
		self.name = name
		#self.area= area

	def __repr__(self):
		#return "<Continent {} has {} area>".format(self.name, self.area)
		return "<Continent {} >".format(self.name)

	def getName(self):
		return self.name

		

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
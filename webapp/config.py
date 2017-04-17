import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = False

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'cop5725'

# Connect to the database
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_DATABASE_URI = "oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl"
SQLALCHEMY_TRACK_MODIFICATIONS = True
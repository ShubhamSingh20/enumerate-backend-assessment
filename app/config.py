import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__package__))

# Enable debug mode.
DEBUG = True

SECRET_KEY = ']3QHOWLFH/LEFiwcEf+f^!M=T;]4[Ibh`X5?&v_7_JI103Ifi/A&C~_Cix>O5xc'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://kwuaupvv:x9JfeZCSox46Do-iLuNzsDyCuKazUCRN@tiny.db.elephantsql.com/kwuaupvv'

SQLALCHEMY_TRACK_MODIFICATIONS = True

TEST_DB_URI = 'sqlite:///' + os.path.join(basedir, 'test_database.db')

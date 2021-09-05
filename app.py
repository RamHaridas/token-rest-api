from resources.executives import ExcecutiveResource
from resources.booking import BookingResource
from resources.slot import SlotResource
from resources.admin import AdminResource
from resources.counter import CounterResource
from resources.service import ServiceResource
from flask import Flask, render_template
from resources.user import UserResource
from resources.branch import BranchResource
from flask_assets import Bundle, Environment
from flask_restful import Api
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import psycopg2
import os

online = True  # True for production and False for offline debug purposes

normal = os.environ.get('MY_DATABASE_URL')

heroku_postgres_url = "postgresql://bwmjdsgabtnqld:bd3dcb534f017b39a4d10b5409d4c0867a2be0c4068b937f18ace2cf8b114b04@ec2-52-45-183-77.compute-1.amazonaws.com:5432/d5khtrd1vucud7"
postgres_url = {
    'user': 'ram',
    'pw': 'ram',
    'db': 'token',
    'host': 'localhost',
    'port': '5432',
}

local_url = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % postgres_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = normal if online else local_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

# to integrate js file with html
# js = Bundle('app.js',output='gen/main.js')
# assets = Environment(app)
# assets.register('main_js',js)
# assets.init_app(app)


# add api endpoints here
api.add_resource(UserResource, '/user')
api.add_resource(BranchResource, '/branch')
api.add_resource(ServiceResource, '/service')
api.add_resource(CounterResource, '/counter')
api.add_resource(AdminResource, '/admin')
api.add_resource(SlotResource, '/slots')
api.add_resource(BookingResource, '/book')
api.add_resource(ExcecutiveResource, '/executives')


@app.route('/')
def home():
    return "YOU DON NOT HAVE PERMISSION TO VISIT THIS PAGE"


# keep this commented out for online
# @app.before_first_request
# def create_tables():
#     db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    # migrate = Migrate(app,db)
    # manager = Manager(app)
    # manager.add_command('db', MigrateCommand)
    # manager.run()
    app.run(port=5000, debug=True)

from flask import Blueprint
from flask_restplus import Api, Resource,Namespace,fields
mod = Blueprint('chungkhoan', __name__,
                        template_folder='templates',url_prefix='/')
namespace = Namespace(name='chungkhoan',path='/',description='run task and service')
from . import routes, events
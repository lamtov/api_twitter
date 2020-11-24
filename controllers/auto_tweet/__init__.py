from flask import Blueprint
from flask_restplus import Api, Resource,Namespace,fields
mod = Blueprint('auto_tweet', __name__,
                        template_folder='templates',url_prefix='/')
namespace = Namespace(name='auto_tweet',path='/',description='run auto_tweet')
from . import routes, events
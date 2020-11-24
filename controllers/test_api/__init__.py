from flask import Blueprint

mod = Blueprint('test_api', __name__,
                        template_folder='templates',url_prefix='/')
from . import  routes
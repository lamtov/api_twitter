from flask import Blueprint

mod = Blueprint('video_streaming', __name__,
                        template_folder='templates')


from . import routes
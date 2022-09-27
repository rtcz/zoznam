from flask import (
    Blueprint, render_template
)

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    # TODO
    posts = []
    return render_template(
        'index.html',
        title='title',
        description='description',
        posts=posts
    )

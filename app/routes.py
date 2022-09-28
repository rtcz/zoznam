import filecmp
import os.path

from flask import Blueprint, render_template, current_app as app, request
from sqlalchemy import desc, asc, collate

from app.video import download_videos_json, videos_json_to_db
from app.models import Video

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    # process the parameters
    order = request.args.get('order', 'asc')
    filter = request.args.get('filter', '')

    # check if videos json was updated
    data_dir = app.config['DATA_FOLDER']
    tmp_file = os.path.join(data_dir, 'videos.json.tmp')
    curr_file = os.path.join(data_dir, 'videos.json')
    url = app.config['VIDEOS_JSON_URL']
    if download_videos_json(url, tmp_file):
        app.logger.info('the videos json file was downloaded')

        if not os.path.isfile(curr_file) or not filecmp.cmp(tmp_file, curr_file):
            # the downloaded file is new
            os.replace(tmp_file, curr_file)
            # update the db
            videos_json_to_db(curr_file)
        else:
            # remove temp file
            os.remove(tmp_file)
    else:
        app.logger.warn('the videos json file in not available')

    # use case insensitive ordering
    if order == 'asc':
        videos = Video.query.order_by(asc(collate(Video.name, 'NOCASE'))).all()
    elif order == 'desc':
        videos = Video.query.order_by(desc(collate(Video.name, 'NOCASE'))).all()

    return render_template(
        'index.html',
        title='Videos',
        description='The list of videos',
        videos=videos,
        order=order,
        filter=filter
    )

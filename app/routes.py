import filecmp
import os.path

from flask import Blueprint, render_template, current_app as app, request
from sqlalchemy import desc, asc, collate
from sqlalchemy.orm import Query

from app.models import Video, db, VideoFeature, Feature
from app.video import download_videos_json, videos_json_to_db

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    # process the parameters
    order = request.args.get('order', 'asc')
    filter = request.args.get('filter')

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

    # assemble the video db query
    query = db.session.query(Video)  # type: Query

    # filter according to the selected tag
    if filter == 'is_featured':
        query = query.filter_by(is_featured=True)
    elif filter == 'disabled':
        query = query.filter_by(disabled=True)
    elif filter is not None:
        query = query.join(VideoFeature).join(Feature).filter_by(name=filter)

    # use case insensitive ordering
    if order == 'asc':
        query = query.order_by(asc(collate(Video.name, 'NOCASE')))
    elif order == 'desc':
        query = query.order_by(desc(collate(Video.name, 'NOCASE')))

    videos = query.all()

    if filter == 'is_featured':
        nice_filter = 'FEATURED'
    elif filter == 'disabled':
        nice_filter = 'DISABLED'
    elif filter is not None:
        nice_filter = filter.removeprefix('DEMO_')
    else:
        nice_filter = filter

    return render_template(
        'index.html',
        title='Videos',
        description='The list of videos',
        videos=videos,
        order=order,
        filter=filter,
        nice_filter=nice_filter
    )

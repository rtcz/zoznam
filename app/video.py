import requests
from flask import json, current_app as app
from requests import Response

from app import db
from app.models import VideoFeature, Video, Feature


def download_videos_json(source: str, target: str) -> bool:
    response = requests.get(source)  # type: Response
    if response.ok:
        data = response.content.decode()
        with open(target, 'wt') as target_file:
            target_file.write(data)
            return True
    else:
        return False


def videos_json_to_db(source: str):
    with open(source, 'rt') as source_file:
        data = json.load(source_file)
        if len(data):
            # data are not empty, proceed

            # truncate the video related tables
            VideoFeature.query.delete()
            Video.query.delete()
            Feature.query.delete()
            db.session.commit()

            feature_set = set()

            # load videos
            for item in data:
                video = Video()
                video.name = item.get('name')
                video.description = item.get('description')
                video.icon_uri = item.get('iconUri')
                video.disabled = item.get('disabled')
                video.is_featured = item.get('isFeatured')
                db.session.add(video)

                video_feature_list = item.get('features', ())
                for feature_name in video_feature_list: # type: str
                    # feature_name = feature_name.removeprefix('DEMO_')
                    feature_set.add(feature_name)

            db.session.commit()

            # load features
            for feature_name in feature_set:
                feature = Feature()
                feature.name = feature_name
                db.session.add(feature)

            db.session.commit()

            # load associations
            for item in data:
                video = db.session.query(Video).filter_by(name=item.get('name')).one()
                video_feature_set = set(item.get('features', ()))
                for feature_name in video_feature_set:
                    feature = db.session.query(Feature).filter_by(name=feature_name).one()

                    video_feature = VideoFeature()
                    video_feature.video = video
                    video_feature.feature = feature
                    db.session.add(video_feature)
                    db.session.commit()

        app.logger.info('video db updated')

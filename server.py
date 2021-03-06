import falcon
import json
from waitress import serve
from Settings import *
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from Model import *


class Symptoms(object):
     def on_get(self, req, resp):
        resp.content_type = falcon.MEDIA_JSON
        session = Session()

        resp.body = json.dumps([{
            'id': location.id,
            'name': location.name,
            'symptoms': [{
                'id': s.id,
                'name': s.name,
                'gender': s.gender,
                'description': s.description
                } for s in session.query(Symptom)
                    .filter(Symptom.location == location.id)
                    .filter(or_(
                        Symptom.gender == None,
                        Symptom.gender == req.get_header('gender')
                        ))
                    .all()
                ]
            } for location in session.query(SymptomLocation).all()])

        session.close()
        resp.status = falcon.HTTP_200


if __name__ == "__main__":
    # Database connection setup
    engine = create_engine(DB_TYPE+'://'+DB_LOGIN+':'+DB_PASSWORD+'@'+DB_HOST+':'+DB_PORT+'/'+DB, echo=True)
    Session = sessionmaker(bind=engine)

    # HTTP server setup
    app = falcon.API()
    app.add_route('/symptoms', Symptoms())
    serve(app, listen='*:5678')

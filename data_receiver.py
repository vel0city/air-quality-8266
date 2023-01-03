import falcon
import duckdb
import json
from datetime import datetime, timedelta
from wsgiref.simple_server import make_server
from falcon import media

class AirData():
    def __init__(self) -> None:
        self.db = duckdb.connect('air_data.duckdb', read_only=False)
        db_create = '''
        CREATE TABLE IF NOT EXISTS main.samples (
	        ts TIMESTAMP NOT NULL,
	        temp FLOAT NOT NULL,
	        humid FLOAT NOT NULL,
	        eco2 FLOAT NOT NULL,
        	tvoc FLOAT NOT NULL,
        	location VARCHAR
        );
        '''
        self.db.execute(db_create)

    def on_post(self, req, resp):
        self.db.execute('INSERT INTO samples VALUES (?, ?, ?, ?, ?, ?)', req.media)
        resp.media = 'ok'
        resp.status = falcon.HTTP_201

    def on_get(self, req, resp):
        days = int(req.params.get('days', 5))
        self.db.execute('SELECT * FROM samples WHERE ts > ?', [str(datetime.now() - timedelta(days=days))])
        resp.media = json.loads(json.dumps(self.db.fetchall(), default=str))
        resp.status = falcon.HTTP_200


class AirDataHandler(media.BaseHandler):
    def serialize(media, content_type):
        return str(media)

    def deserialize(stream, content_type, length):
        return json.loads(stream.read())


app = falcon.App()
app.req_options.media_handlers.update({'text/plain':AirDataHandler})
app.add_route('/air_data', AirData())

if __name__ == '__main__':
    with make_server('', 8080, app) as httpd:
        httpd.serve_forever()
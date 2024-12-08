from config import db
from models import Trail, trails_schema

def read_all_trails():
    trails = Trail.query.all()
    return trails_schema.dump(trails)

def create_trail():
    request_json = request.get_json()
    trail_data = request_json.get("Trail")
    new_trail = Trail(**trail_data)
    db.session.add(new_trail)
    db.session.commit()
    return trails_schema.dump(new_trail)
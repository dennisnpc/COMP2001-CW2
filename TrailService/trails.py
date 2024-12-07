from config import db
from models import Trail, trails_schema

def read_all_trails():
    trails = Trail.query.all()
    return trails_schema.dump(trails)
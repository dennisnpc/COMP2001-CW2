from config import db
from models import Trail, trails_schema

# Trail CRUD operations
# To read (GET) all Trails
def read_all_trails():
    trails = Trail.query.all()
    return trails_schema.dump(trails)

# To create (POST) a Trail
def create_trail():
    request_json = request.get_json()
    trail_data = request_json.get("Trail")
    new_trail = Trail(**trail_data)
    db.session.add(new_trail)
    db.session.commit()
    return trails_schema.dump(new_trail)

# To update (PUT) a Trail by name
# To update (PUT) a Trail by name
def update_trail(trail_name):
    request_json = request.get_json()
    trail_data = request_json.get("Trail")
    existing_trail = Trail.query.filter(Trail.Name == trail_name).one_or_none()

    if existing_trail:
        for key in ['Name', 'Difficulty', 'Rating', 'Length', 'ElevationGain', 'RouteType', 'CompletionTime', 'Description']:
            if key in trail_data:
                setattr(existing_trail, key, trail_data[key])

    # Extract Trail

    # Check user owns the Trail

    # Update Trail
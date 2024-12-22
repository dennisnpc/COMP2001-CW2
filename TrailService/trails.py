from flask import abort, make_response, request, g, jsonify
from config import db
from models import (
    Trail, trail_schema, trails_schema,
    Point, Tag, Location,
    TrailPoint, TrailTag,
    location_schema, point_schema, tag_schema
)
from auth import requires_authentication
from math import ceil

# Trail CRUD operations
# To read (GET) all Trails
def read_all_trails():
    # Get pagination parameters from query string
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Define the maximum number of trails per page
    MAX_PER_PAGE = 100

    if page < 1 or per_page < 1:
        abort(400, "Page and per_page must be positive integers.")

    # Enforce the maximum number of trails per page
    if per_page > MAX_PER_PAGE:
        per_page = MAX_PER_PAGE

    total_trails = Trail.query.count()

    total_pages = ceil(total_trails / per_page)

    # Get the Trails for the requested page
    trails = (
        Trail.query
        .order_by(Trail.TrailId)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    result = trails_schema.dump(trails)

    # Include pagination info
    response = {
        'TotalTrails': total_trails,
        'TotalPages': total_pages,
        'CurrentPage': page,
        'PerPage': per_page,
        'Trails': result
    }

    return jsonify(response)

# To read (GET) a Trail by name
def read_trail_by_name(trail_name):
    trail = Trail.query.filter(Trail.Name == trail_name).one_or_none()
    if trail is None:
        abort(404, f"Trail with name '{trail_name}' not found.")
    return trail_schema.dump(trail)

# To create (POST) a Trail
@requires_authentication
def create_trail():
    request_json = request.get_json()

    if not request_json:
        abort(400, "Invalid JSON.")

    # Extract and remove Credentials
    request_json.pop("Credentials", None)

    # Extract the Trail object
    trail_data = request_json.get("Trail")
    if not trail_data:
        abort(400, "Trail data is required.")

    user = g.current_user

    location_data = trail_data.pop('Location', None)
    if not location_data:
        abort(400, "Location data is required.")

    # Create the Location
    location = Location(**location_data)
    db.session.add(location)
    db.session.flush()

    # Create the Trail
    trail_fields = {
        key: trail_data[key] for key in [
            'Name', 'Difficulty', 'Rating', 'Length', 'ElevationGain',
            'RouteType', 'CompletionTime', 'Description'
        ] if key in trail_data
    }
    new_trail = Trail(**trail_fields)
    new_trail.UserId = user.UserId
    new_trail.LocationId = location.LocationId
    db.session.add(new_trail)
    db.session.flush()

    points_data = trail_data.get('Points', [])
    if len(points_data) < 1:
        abort(400, "At least one point is required.")

    for sequence_number, point_data in enumerate(points_data, start=1):
        point = Point(**point_data)
        db.session.add(point)
        db.session.flush()
        trail_point = TrailPoint(
            TrailId = new_trail.TrailId,
            PointId = point.PointId,
            SequenceNumber = sequence_number # Automatically assign sequence number
        )
        db.session.add(trail_point)

    # Create Tags and TrailTags
    tags_data = trail_data.get('Tags', [])
    for tag_data in tags_data:
        tag = Tag(**tag_data)
        db.session.add(tag)
        db.session.flush()
        trail_tag = TrailTag(TrailId=new_trail.TrailId, TagId=tag.TagId)
        db.session.add(trail_tag)

    db.session.commit()
    return trail_schema.dump(new_trail), 201

# To update (PUT) a Trail by name
@requires_authentication
def update_trail(trail_name):
    request_json = request.get_json()

    if not request_json:
        abort(400, "Invalid JSON.")

    # Extract and remove Credentials
    request_json.pop("Credentials", None)

    # Extract the Trail object
    trail_data = request_json.get("Trail")
    if not trail_data:
        abort(400, "Trail data is required.")

    user = g.current_user
    existing_trail = Trail.query.filter(Trail.Name == trail_name).one_or_none()

    # Check user owns the Trail
    if existing_trail:
        if existing_trail.UserId != user.UserId:
            abort(403, "You do not have permission to update this trail.")

        try:
            # Update Trail fields
            for key in [
                'Name', 'Difficulty', 'Rating', 'Length', 'ElevationGain',
                'RouteType', 'CompletionTime', 'Description'
            ]:
                if key in trail_data:
                    setattr(existing_trail, key, trail_data[key])

            # Update Location if provided
            location_data = trail_data.get('Location')
            if location_data:
                new_location = Location(**location_data)
                db.session.add(new_location)
                db.session.flush()
                existing_trail.LocationId = new_location.LocationId

            # Update Points if provided
            points_data = trail_data.get('Points')
            if points_data is not None:
                if len(points_data) < 1:
                    abort(400, "At least one point is required when updating points.")
                # Remove existing Points
                TrailPoint.query.filter_by(TrailId=existing_trail.TrailId).delete()
                db.session.flush()

                for sequence_number, point_data in enumerate(points_data, start=1):
                    point = Point(**point_data)
                    db.session.add(point)
                    db.session.flush()
                    trail_point = TrailPoint(
                        TrailId = existing_trail.TrailId,
                        PointId = point.PointId,
                        SequenceNumber = sequence_number  # Automatically assign sequence number
                    )
                    db.session.add(trail_point)

            # Update Tags if provided
            tags_data = trail_data.get('Tags')
            if tags_data is not None:
                # Remove existing Tags
                TrailTag.query.filter_by(TrailId=existing_trail.TrailId).delete()
                db.session.flush()

                for tag_data in tags_data:
                    tag = Tag(**tag_data)
                    db.session.add(tag)
                    db.session.flush()
                    trail_tag = TrailTag(TrailId=existing_trail.TrailId, TagId=tag.TagId)
                    db.session.add(trail_tag)

            db.session.commit()
            return trail_schema.dump(existing_trail)

        except Exception as e:
            db.session.rollback()
            abort(400, f"Could not update trail: {str(e)}")
    else:
        abort(404, f"Trail with name '{trail_name}' not found.")

# To delete (DELETE) a Trail
@requires_authentication
def delete_trail(trail_name):
    user = g.current_user
    existing_trail = Trail.query.filter(Trail.Name == trail_name).one_or_none()

    # Check user owns the Trail
    if existing_trail:
        if existing_trail.UserId != user.UserId:
            abort(403, "You do not have permission to delete this trail.")

        try:
            # Delete associated Points and Tags first from link tables
            TrailPoint.query.filter_by(TrailId=existing_trail.TrailId).delete()
            TrailTag.query.filter_by(TrailId=existing_trail.TrailId).delete()
            
            # Delete Trail
            db.session.delete(existing_trail)
            db.session.commit()
            return make_response(f"Trail with name '{trail_name}' deleted", 204)
        except Exception as e:
            db.session.rollback()
            abort(400, f"Could not delete trail: {str(e)}")
    else:
        abort(404, f"Trail with name '{trail_name}' not found.")
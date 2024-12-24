from config import db, ma

# Define the schema for the database
SCHEMA = 'CW2'

# User model
class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {'schema': SCHEMA}
    UserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(60), unique=True, nullable=False)

    # Relationship to Trail
    trails = db.relationship('Trail', back_populates='user')

# Location model
class Location(db.Model):
    __tablename__ = 'Location'
    __table_args__ = {'schema': SCHEMA}
    LocationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    City = db.Column(db.String(40))
    County = db.Column(db.String(40), nullable=False)
    Country = db.Column(db.String(40), nullable=False)

    # Relationship to Trail
    trails = db.relationship('Trail', back_populates='location')

# Point model
class Point(db.Model):
    __tablename__ = 'Point'
    __table_args__ = {'schema': SCHEMA}
    PointId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Latitude = db.Column(db.Numeric(7, 5), nullable=False)
    Longitude = db.Column(db.Numeric(8, 5), nullable=False)
    Description = db.Column(db.String(2000))

    # Relationship to Trail
    trails = db.relationship('Trail', secondary=f'{SCHEMA}.TrailPoint', back_populates='points')

# Tag model
class Tag(db.Model):
    __tablename__ = 'Tag'
    __table_args__ = {'schema': SCHEMA}
    TagId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(40), unique=True, nullable=False)

    # Relationship to Trail
    trails = db.relationship('Trail', secondary=f'{SCHEMA}.TrailTag', back_populates='tags')

# Trail model
class Trail(db.Model):
    __tablename__ = 'Trail'
    __table_args__ = {'schema': SCHEMA}
    TrailId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.User.UserId'), nullable=False)
    LocationId = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.Location.LocationId'), nullable=False)
    Name = db.Column(db.String(150), unique=True, nullable=False)
    Difficulty = db.Column(db.String(25), nullable=False)
    Rating = db.Column(db.Numeric(2, 1), nullable=False)
    Length = db.Column(db.Numeric(5, 1), nullable=False)
    ElevationGain = db.Column(db.SmallInteger, nullable=False)
    RouteType = db.Column(db.String(25), nullable=False)
    CompletionTime = db.Column(db.Integer)
    Description = db.Column(db.String(2000), nullable=False, default='No description provided.')

    # Relationships
    user = db.relationship('User', back_populates='trails')
    location = db.relationship('Location', back_populates='trails')
    points = db.relationship('Point', secondary=f'{SCHEMA}.TrailPoint', back_populates='trails')
    tags = db.relationship('Tag', secondary=f'{SCHEMA}.TrailTag', back_populates='trails')

# Link table for Trail and Point
class TrailPoint(db.Model):
    __tablename__ = 'TrailPoint'
    __table_args__ = {'schema': SCHEMA}
    TrailId = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.Trail.TrailId'), primary_key=True)
    PointId = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.Point.PointId'), primary_key=True)
    SequenceNumber = db.Column(db.SmallInteger, nullable=False)

# Link table for Trail and Tag
class TrailTag(db.Model):
    __tablename__ = 'TrailTag'
    __table_args__ = {'schema': SCHEMA}
    TagId = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.Tag.TagId'), primary_key=True)
    TrailId = db.Column(db.Integer, db.ForeignKey(f'{SCHEMA}.Trail.TrailId'), primary_key=True)

# Schemas for (de)serialisation
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ('UserId',)

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        sqla_session = db.session
        exclude = ('LocationId',)

    City = ma.auto_field()
    County = ma.auto_field()
    Country = ma.auto_field()

class PointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Point
        load_instance = True
        sqla_session = db.session
        exclude = ('PointId',)

    Description = ma.auto_field()
    Latitude = ma.auto_field()
    Longitude = ma.auto_field()

class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True
        sqla_session = db.session
        exclude = ('TagId',)

    Name = ma.auto_field()

class TrailPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailPoint
        load_instance = True
        sqla_session = db.session
        exclude = ('TrailId', 'PointId', 'SequenceNumber')  # Exclude SequenceNumber

    Point = ma.Nested(PointSchema)

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        exclude = ('TrailId', 'UserId', 'LocationId')

    CompletionTime = ma.auto_field()
    Description = ma.auto_field()
    Difficulty = ma.auto_field()
    ElevationGain = ma.auto_field()
    Length = ma.auto_field()
    Name = ma.auto_field()
    Rating = ma.auto_field()
    RouteType = ma.auto_field()
    
    Location = ma.Nested(LocationSchema, attribute='location')
    Points = ma.List(ma.Nested(PointSchema), attribute='points')
    Tags = ma.List(ma.Nested(TagSchema), attribute='tags')

# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
point_schema = PointSchema()
points_schema = PointSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
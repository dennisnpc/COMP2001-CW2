from config import db, ma

# Define the schema for the database
SCHEMA = 'CW2'

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

# Trail schema
class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        include_fk = True

# Schema instances
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
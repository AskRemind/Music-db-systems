from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'user'
    UserID = db.Column(db.String(50), primary_key=True)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Age = db.Column(db.Integer)
    Country = db.Column(db.String(50))
    Gender = db.Column(db.String(1))
    PasswordHash = db.Column(db.String(255), nullable=False)

class UserRating(db.Model):
    RatingID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    SongID = db.Column(db.Integer, db.ForeignKey('song.SongID'))
    RatingScore = db.Column(db.Integer)

class UserComment(db.Model):
    CommentID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    SongID = db.Column(db.Integer, db.ForeignKey('song.SongID'))
    CommentText = db.Column(db.String(500))

class Song(db.Model):
    __tablename__ = 'song'
    SongID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    ArtistID = db.Column(db.Integer, db.ForeignKey('artist.ArtistID'))
    AlbumID = db.Column(db.Integer, db.ForeignKey('album.AlbumID'))
    Genre = db.Column(db.String(50))
    Duration = db.Column(db.String(10))
    ReleaseDate = db.Column(db.Date)

class Album(db.Model):
    __tablename__ = 'album'
    AlbumID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    ArtistID = db.Column(db.Integer, db.ForeignKey('artist.ArtistID'))
    ReleaseDate = db.Column(db.Date)

class Artist(db.Model):
    __tablename__ = 'artist'
    ArtistID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Country = db.Column(db.String(50))

class ListeningHistory(db.Model):
    __tablename__ = 'listening_history'
    HistoryID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    SongID = db.Column(db.Integer, db.ForeignKey('song.SongID'))
    StartTime = db.Column(db.DateTime, nullable=False)
    EndTime = db.Column(db.DateTime)

class Playlist(db.Model):
    __tablename__ = 'playlist'
    PlaylistID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    Title = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(255))

class PlaylistSong(db.Model):
    __tablename__ = 'playlist_song'
    PlaylistID = db.Column(db.Integer, db.ForeignKey('playlist.PlaylistID'), primary_key=True)
    SongID = db.Column(db.Integer, db.ForeignKey('song.SongID'), primary_key=True)

class Follow(db.Model):
    __tablename__ = 'follow'
    FollowID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    FollowedID = db.Column(db.Integer, db.ForeignKey('artist.ArtistID'))
    FollowType = db.Column(db.Enum('Artist'), nullable=False)

class Subscription(db.Model):
    __tablename__ = 'subscription'
    SubscriptionID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    PlanType = db.Column(db.String(50), nullable=False)
    StartDate = db.Column(db.Date, nullable=False)
    EndDate = db.Column(db.Date)
    IsActive = db.Column(db.Boolean, default=True)

class Billing(db.Model):
    __tablename__ = 'billing'
    BillingID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    SubscriptionID = db.Column(db.Integer, db.ForeignKey('subscription.SubscriptionID'))
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    BillingDate = db.Column(db.Date, nullable=False)
    PaymentMethod = db.Column(db.String(50))
    Status = db.Column(db.String(50))

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    SearchID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    SearchTerm = db.Column(db.String(255), nullable=False)
    SearchDate = db.Column(db.DateTime, nullable=False)

class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    RecommendationID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    PlaylistID = db.Column(db.Integer, db.ForeignKey('playlist.PlaylistID'))
    RecommendedDate = db.Column(db.DateTime, nullable=False)

class StreamingMetrics(db.Model):
    __tablename__ = 'streaming_metrics'
    MetricID = db.Column(db.Integer, primary_key=True)
    SongID = db.Column(db.Integer, db.ForeignKey('song.SongID'))
    PlatformID = db.Column(db.Integer)
    PlayCount = db.Column(db.Integer, default=0)
    LikeCount = db.Column(db.Integer, default=0)
    Date = db.Column(db.Date)

class RecordLabel(db.Model):
    __tablename__ = 'record_label'
    LabelID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Country = db.Column(db.String(50))
    FoundedYear = db.Column(db.Integer)

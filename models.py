from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    name_vi = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    description_vi = db.Column(db.Text)
    description_en = db.Column(db.Text)
    price = db.Column(db.Integer)
    area = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    room_type = db.Column(db.String(50))
    amenities = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    images = db.relationship('RoomImage', backref='room', lazy=True, cascade='all, delete-orphan')

class RoomImage(db.Model):
    __tablename__ = 'room_images'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    alt_vi = db.Column(db.String(200))
    alt_en = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    name_vi = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    description_vi = db.Column(db.Text)
    description_en = db.Column(db.Text)
    category_vi = db.Column(db.String(100))
    category_en = db.Column(db.String(100))
    hours = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    images = db.relationship('RestaurantImage', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy=True, cascade='all, delete-orphan')

class RestaurantImage(db.Model):
    __tablename__ = 'restaurant_images'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    alt_vi = db.Column(db.String(200))
    alt_en = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    name_vi = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    description_vi = db.Column(db.Text)
    description_en = db.Column(db.Text)
    price = db.Column(db.Integer)
    sort_order = db.Column(db.Integer, default=0)

class Amenity(db.Model):
    __tablename__ = 'amenities'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    name_vi = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    description_vi = db.Column(db.Text)
    description_en = db.Column(db.Text)
    icon = db.Column(db.String(50))
    video_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    images = db.relationship('AmenityImage', backref='amenity', lazy=True, cascade='all, delete-orphan')

class AmenityImage(db.Model):
    __tablename__ = 'amenity_images'
    
    id = db.Column(db.Integer, primary_key=True)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenities.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    alt_vi = db.Column(db.String(200))
    alt_en = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)

class Experience(db.Model):
    __tablename__ = 'experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title_vi = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    short_desc_vi = db.Column(db.Text)
    short_desc_en = db.Column(db.Text)
    content_vi = db.Column(db.Text)
    content_en = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    images = db.relationship('ExperienceImage', backref='experience', lazy=True, cascade='all, delete-orphan')
    videos = db.relationship('ExperienceVideo', backref='experience', lazy=True, cascade='all, delete-orphan')

class ExperienceImage(db.Model):
    __tablename__ = 'experience_images'
    
    id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    alt_vi = db.Column(db.String(200))
    alt_en = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)

class ExperienceVideo(db.Model):
    __tablename__ = 'experience_videos'
    
    id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    title_vi = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)

class SteamProgram(db.Model):
    __tablename__ = 'steam_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title_vi = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    short_desc_vi = db.Column(db.Text)
    short_desc_en = db.Column(db.Text)
    content_vi = db.Column(db.Text)
    content_en = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    images = db.relationship('SteamImage', backref='steam_program', lazy=True, cascade='all, delete-orphan')
    videos = db.relationship('SteamVideo', backref='steam_program', lazy=True, cascade='all, delete-orphan')

class SteamImage(db.Model):
    __tablename__ = 'steam_images'
    
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.Integer, db.ForeignKey('steam_programs.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    alt_vi = db.Column(db.String(200))
    alt_en = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)

class SteamVideo(db.Model):
    __tablename__ = 'steam_videos'
    
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.Integer, db.ForeignKey('steam_programs.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    title_vi = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title_vi = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    description_vi = db.Column(db.Text)
    description_en = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    features = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    images = db.relationship('EventImage', backref='event', lazy=True, cascade='all, delete-orphan')

class EventImage(db.Model):
    __tablename__ = 'event_images'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    alt_vi = db.Column(db.String(200))
    alt_en = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title_vi = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    excerpt_vi = db.Column(db.Text)
    excerpt_en = db.Column(db.Text)
    content_vi = db.Column(db.Text)
    content_en = db.Column(db.Text)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='draft')
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GalleryItem(db.Model):
    __tablename__ = 'gallery_items'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    title_vi = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    url = db.Column(db.String(500), nullable=False)
    thumb_url = db.Column(db.String(500))
    category = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    contact_type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Banner(db.Model):
    __tablename__ = 'banners'
    
    id = db.Column(db.Integer, primary_key=True)
    title_vi = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    subtitle_vi = db.Column(db.String(300))
    subtitle_en = db.Column(db.String(300))
    description_vi = db.Column(db.Text)
    description_en = db.Column(db.Text)
    button_text_vi = db.Column(db.String(100))
    button_text_en = db.Column(db.String(100))
    button_link = db.Column(db.String(500))
    image_url = db.Column(db.String(500), nullable=False)
    icon = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    unsubscribed_at = db.Column(db.DateTime)

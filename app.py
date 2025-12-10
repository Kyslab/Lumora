import os
import uuid
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, session
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024
app.secret_key = os.environ.get("SESSION_SECRET", "lumora-resort-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 5,
    'max_overflow': 10,
    'connect_args': {
        'connect_timeout': 10,
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5
    }
}

from models import db, User, Contact, Room, RoomImage, Restaurant, RestaurantImage, MenuItem, Amenity, AmenityImage, Experience, ExperienceImage, ExperienceVideo, SteamProgram, SteamImage, SteamVideo, Event, EventImage, News, GalleryItem, Banner, Newsletter
db.init_app(app)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from admin import admin_bp
app.register_blueprint(admin_bp)

def create_admin_user():
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@lumoraresort.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin / admin123")

def room_to_dict(room):
    return {
        "id": room.slug,
        "slug": room.slug,
        "name": {"vi": room.name_vi, "en": room.name_en},
        "description": {"vi": room.description_vi or "", "en": room.description_en or ""},
        "price": room.price or 0,
        "area": room.area or 0,
        "capacity": room.capacity or 0,
        "room_type": room.room_type or "",
        "amenities": (room.amenities or "").split("\n") if room.amenities else [],
        "images": [img.url for img in room.images],
        "video": room.video_url or "",
        "is_featured": room.is_featured
    }

def restaurant_to_dict(restaurant):
    return {
        "id": restaurant.slug,
        "slug": restaurant.slug,
        "name": {"vi": restaurant.name_vi, "en": restaurant.name_en},
        "description": {"vi": restaurant.description_vi or "", "en": restaurant.description_en or ""},
        "category": {"vi": restaurant.category_vi or "", "en": restaurant.category_en or ""},
        "hours": restaurant.hours or "",
        "images": [img.url for img in restaurant.images],
        "menu": [
            {"name": {"vi": item.name_vi, "en": item.name_en}, "price": item.price or 0}
            for item in restaurant.menu_items
        ]
    }

def amenity_to_dict(amenity):
    return {
        "id": amenity.slug,
        "slug": amenity.slug,
        "name": {"vi": amenity.name_vi, "en": amenity.name_en},
        "description": {"vi": amenity.description_vi or "", "en": amenity.description_en or ""},
        "icon": amenity.icon or "",
        "images": [img.url for img in amenity.images],
        "video": amenity.video_url or ""
    }

def experience_to_dict(experience):
    return {
        "id": experience.slug,
        "slug": experience.slug,
        "name": {"vi": experience.title_vi, "en": experience.title_en},
        "short_desc": {"vi": experience.short_desc_vi or "", "en": experience.short_desc_en or ""},
        "content": {"vi": experience.content_vi or "", "en": experience.content_en or ""},
        "images": [img.url for img in experience.images],
        "videos": [
            {"url": vid.url, "title": {"vi": vid.title_vi or "", "en": vid.title_en or ""}}
            for vid in experience.videos
        ]
    }

def steam_to_dict(steam):
    return {
        "id": steam.slug,
        "slug": steam.slug,
        "name": {"vi": steam.title_vi, "en": steam.title_en},
        "short_desc": {"vi": steam.short_desc_vi or "", "en": steam.short_desc_en or ""},
        "content": {"vi": steam.content_vi or "", "en": steam.content_en or ""},
        "images": [img.url for img in steam.images],
        "videos": [
            {"url": vid.url, "title": {"vi": vid.title_vi or "", "en": vid.title_en or ""}}
            for vid in steam.videos
        ]
    }

def event_to_dict(event):
    return {
        "id": event.slug,
        "slug": event.slug,
        "name": {"vi": event.title_vi, "en": event.title_en},
        "description": {"vi": event.description_vi or "", "en": event.description_en or ""},
        "capacity": event.capacity or 0,
        "price": event.price or 0,
        "features": (event.features or "").split("\n") if event.features else [],
        "images": [img.url for img in event.images]
    }

def news_to_dict(news):
    return {
        "id": news.id,
        "slug": news.slug,
        "title": {"vi": news.title_vi, "en": news.title_en},
        "excerpt": {"vi": news.excerpt_vi or "", "en": news.excerpt_en or ""},
        "content": {"vi": news.content_vi or "", "en": news.content_en or ""},
        "image": news.image_url or "",
        "date": news.published_at.strftime("%Y-%m-%d") if news.published_at else "",
        "category": {"vi": get_category_label(news.category, "vi"), "en": get_category_label(news.category, "en")}
    }

def get_category_label(category, lang):
    labels = {
        "news": {"vi": "Tin tức", "en": "News"},
        "promotion": {"vi": "Ưu đãi", "en": "Promotion"},
        "event": {"vi": "Sự kiện", "en": "Event"}
    }
    return labels.get(category, {}).get(lang, category or "")

@app.route('/')
def home():
    lang = request.args.get('lang', 'vi')
    rooms = Room.query.filter_by(is_active=True, is_featured=True).all()
    rooms_data = {r.slug: room_to_dict(r) for r in rooms}
    
    amenities = Amenity.query.filter_by(is_active=True).all()
    amenities_data = {a.slug: amenity_to_dict(a) for a in amenities}
    
    news_items = News.query.filter_by(status='published').order_by(News.published_at.desc()).limit(3).all()
    news_data = [news_to_dict(n) for n in news_items]
    
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.sort_order, Banner.created_at).all()
    
    return render_template('home.html', 
                         lang=lang,
                         rooms=rooms_data,
                         amenities=amenities_data,
                         news=news_data,
                         banners=banners)

@app.route('/accommodation')
def accommodation():
    lang = request.args.get('lang', 'vi')
    room_type = request.args.get('type', None)
    
    query = Room.query.filter_by(is_active=True)
    if room_type:
        query = query.filter_by(room_type=room_type)
    rooms = query.all()
    rooms_data = {r.slug: room_to_dict(r) for r in rooms}
    
    return render_template('accommodation.html', 
                         lang=lang,
                         rooms=rooms_data,
                         selected_type=room_type)

@app.route('/accommodation/<room_id>')
def room_detail(room_id):
    lang = request.args.get('lang', 'vi')
    room = Room.query.filter_by(slug=room_id, is_active=True).first()
    if not room:
        return render_template('404.html', lang=lang), 404
    return render_template('room_detail.html', lang=lang, room=room_to_dict(room))

@app.route('/dining')
def dining():
    lang = request.args.get('lang', 'vi')
    restaurants = Restaurant.query.filter_by(is_active=True).all()
    restaurants_data = {r.slug: restaurant_to_dict(r) for r in restaurants}
    return render_template('dining.html', lang=lang, restaurants=restaurants_data)

@app.route('/dining/<restaurant_id>')
def restaurant_detail(restaurant_id):
    lang = request.args.get('lang', 'vi')
    restaurant = Restaurant.query.filter_by(slug=restaurant_id, is_active=True).first()
    if not restaurant:
        return render_template('404.html', lang=lang), 404
    return render_template('restaurant_detail.html', lang=lang, restaurant=restaurant_to_dict(restaurant))

@app.route('/amenities')
def amenities():
    lang = request.args.get('lang', 'vi')
    amenities_list = Amenity.query.filter_by(is_active=True).all()
    amenities_data = {a.slug: amenity_to_dict(a) for a in amenities_list}
    return render_template('amenities.html', lang=lang, amenities=amenities_data)

@app.route('/experiences/checkin')
def experience_checkin():
    lang = request.args.get('lang', 'vi')
    experience = Experience.query.filter_by(slug='checkin', is_active=True).first()
    if not experience:
        return render_template('404.html', lang=lang), 404
    return render_template('experience_detail.html', lang=lang, experience=experience_to_dict(experience))

@app.route('/experiences/adventure')
def experience_adventure():
    lang = request.args.get('lang', 'vi')
    experience = Experience.query.filter_by(slug='adventure', is_active=True).first()
    if not experience:
        return render_template('404.html', lang=lang), 404
    return render_template('experience_detail.html', lang=lang, experience=experience_to_dict(experience))

@app.route('/steam/intro')
def steam_intro():
    lang = request.args.get('lang', 'vi')
    steam_item = SteamProgram.query.filter_by(slug='intro', is_active=True).first()
    if not steam_item:
        return render_template('404.html', lang=lang), 404
    return render_template('steam_detail.html', lang=lang, steam=steam_to_dict(steam_item))

@app.route('/steam/workshop')
def steam_workshop():
    lang = request.args.get('lang', 'vi')
    steam_item = SteamProgram.query.filter_by(slug='workshop', is_active=True).first()
    if not steam_item:
        return render_template('404.html', lang=lang), 404
    return render_template('steam_detail.html', lang=lang, steam=steam_to_dict(steam_item))

@app.route('/steam/register')
def steam_register():
    lang = request.args.get('lang', 'vi')
    return render_template('steam_register.html', lang=lang)

@app.route('/events')
def events():
    lang = request.args.get('lang', 'vi')
    events_list = Event.query.filter_by(is_active=True).all()
    events_data = {e.slug: event_to_dict(e) for e in events_list}
    return render_template('events.html', lang=lang, events=events_data)

@app.route('/news')
def news():
    lang = request.args.get('lang', 'vi')
    news_items = News.query.filter_by(status='published').order_by(News.published_at.desc()).all()
    news_data = [news_to_dict(n) for n in news_items]
    return render_template('news.html', lang=lang, news=news_data)

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    lang = request.args.get('lang', 'vi')
    article = News.query.filter_by(id=news_id, status='published').first()
    if not article:
        return render_template('404.html', lang=lang), 404
    return render_template('news_detail.html', lang=lang, article=news_to_dict(article))

@app.route('/gallery')
def gallery():
    lang = request.args.get('lang', 'vi')
    
    images = GalleryItem.query.filter_by(type='image', is_active=True).order_by(GalleryItem.sort_order).all()
    videos = GalleryItem.query.filter_by(type='video', is_active=True).order_by(GalleryItem.sort_order).all()
    
    gallery_data = {
        "images": [
            {"url": img.url, "title": {"vi": img.title_vi or "", "en": img.title_en or ""}}
            for img in images
        ],
        "videos": [
            {"url": vid.url, "title": {"vi": vid.title_vi or "", "en": vid.title_en or ""}}
            for vid in videos
        ]
    }
    
    return render_template('gallery.html', lang=lang, gallery=gallery_data)

@app.route('/contact')
def contact():
    lang = request.args.get('lang', 'vi')
    return render_template('contact.html', lang=lang)

@app.route('/api/contact', methods=['POST'])
@csrf.exempt
def submit_contact():
    data = request.get_json()
    try:
        contact_type = data.get('type', 'contact')
        
        if contact_type == 'steam_register':
            programs = {
                'steam_camp': 'STEAM Camp (3-5 ngày)',
                'steam_weekend': 'STEAM Weekend (2 ngày)', 
                'steam_day': 'STEAM Day Trip (1 ngày)',
                'robot_workshop': 'Workshop Làm Robot',
                'science_workshop': 'Workshop Thí Nghiệm Khoa Học',
                'art_workshop': 'Workshop Nghệ Thuật Tái Chế',
                'gardening_workshop': 'Workshop Làm Vườn',
                'survival_workshop': 'Workshop Kỹ Năng Sinh Tồn',
                'cooking_workshop': 'Workshop Nấu Ăn'
            }
            program_name = programs.get(data.get('program', ''), data.get('program', ''))
            
            message_parts = [
                f"Tên phụ huynh: {data.get('parent_name', '')}",
                f"Tên học viên: {data.get('student_name', '')}",
                f"Tuổi học viên: {data.get('student_age', '')}",
                f"Chương trình: {program_name}",
                f"Ngày dự kiến: {data.get('expected_date', 'Chưa xác định')}",
                f"Số lượng học viên: {data.get('num_students', '1')}",
            ]
            if data.get('notes'):
                message_parts.append(f"Ghi chú: {data.get('notes')}")
            formatted_message = '\n'.join(message_parts)
            subject = f"Đăng ký STEAM - {program_name}"
        else:
            formatted_message = data.get('message', '')
            subject = data.get('subject', '')
        
        contact = Contact(
            name=data.get('name') or data.get('parent_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            subject=subject,
            message=formatted_message,
            contact_type=contact_type,
            status='new'
        )
        db.session.add(contact)
        db.session.commit()
    except Exception as e:
        print(f"Error saving contact: {e}")
    return jsonify({"success": True, "message": "Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất."})

@app.route('/api/booking', methods=['POST'])
@csrf.exempt
def submit_booking():
    data = request.get_json()
    try:
        room_types = {'deluxe': 'Phòng Deluxe', 'glamping': 'Glamping / Cabin', 'bungalow': 'Bungalow'}
        room_type = room_types.get(data.get('room_type', ''), data.get('room_type', ''))
        
        message_parts = [
            f"Ngày nhận phòng: {data.get('checkin', '')}",
            f"Ngày trả phòng: {data.get('checkout', '')}",
            f"Loại phòng: {room_type}",
            f"Số người lớn: {data.get('adults', '1')}",
            f"Số trẻ em: {data.get('children', '0')}",
        ]
        if data.get('notes'):
            message_parts.append(f"Ghi chú: {data.get('notes')}")
        
        formatted_message = '\n'.join(message_parts)
        
        contact = Contact(
            name=data.get('name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            subject='Đặt phòng',
            message=formatted_message,
            contact_type='booking',
            status='new'
        )
        db.session.add(contact)
        db.session.commit()
    except Exception as e:
        print(f"Error saving booking: {e}")
    return jsonify({"success": True, "message": "Yêu cầu đặt phòng đã được gửi! Chúng tôi sẽ liên hệ xác nhận."})

@app.route('/api/newsletter', methods=['POST'])
@csrf.exempt
def subscribe_newsletter():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    lang = data.get('lang', 'vi')
    
    if not email:
        msg = 'Vui lòng nhập email.' if lang == 'vi' else 'Please enter your email.'
        return jsonify({"success": False, "message": msg})
    
    try:
        existing = Newsletter.query.filter_by(email=email).first()
        if existing:
            if existing.is_active:
                msg = 'Email này đã được đăng ký nhận tin.' if lang == 'vi' else 'This email is already subscribed.'
                return jsonify({"success": False, "message": msg})
            else:
                existing.is_active = True
                existing.unsubscribed_at = None
                db.session.commit()
                msg = 'Đăng ký thành công! Cảm ơn bạn đã quan tâm.' if lang == 'vi' else 'Subscribed successfully! Thank you for your interest.'
                return jsonify({"success": True, "message": msg})
        
        newsletter = Newsletter(email=email)
        db.session.add(newsletter)
        db.session.commit()
        msg = 'Đăng ký thành công! Cảm ơn bạn đã quan tâm đến Lumora Resort.' if lang == 'vi' else 'Subscribed successfully! Thank you for your interest in Lumora Resort.'
        return jsonify({"success": True, "message": msg})
    except Exception as e:
        print(f"Error subscribing newsletter: {e}")
        msg = 'Có lỗi xảy ra, vui lòng thử lại sau.' if lang == 'vi' else 'An error occurred, please try again later.'
        return jsonify({"success": False, "message": msg})

@app.errorhandler(413)
def request_entity_too_large(error):
    from flask import flash
    flash('File quá lớn! Vui lòng chọn file nhỏ hơn 25MB.', 'error')
    return render_template('error.html', error_code=413, error_message='File quá lớn! Vui lòng chọn file nhỏ hơn 25MB.'), 413

if __name__ == '__main__':
    create_admin_user()
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from models import db, User, Room, RoomImage, Restaurant, RestaurantImage, MenuItem
from models import Amenity, AmenityImage, Experience, ExperienceImage, ExperienceVideo
from models import SteamProgram, SteamImage, SteamVideo, Event, EventImage, News, GalleryItem, Contact, Banner, Newsletter, SiteSetting
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, subfolder):
    """Save uploaded file and return the URL path"""
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        upload_path = os.path.join(UPLOAD_FOLDER, subfolder)
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        return f"/{file_path}"
    return None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Bạn cần đăng nhập với tài khoản admin.', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_admin:
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user)
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng.', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất.', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'rooms': Room.query.count(),
        'restaurants': Restaurant.query.count(),
        'amenities': Amenity.query.count(),
        'experiences': Experience.query.count(),
        'steam': SteamProgram.query.count(),
        'events': Event.query.count(),
        'news': News.query.count(),
        'gallery': GalleryItem.query.count(),
        'contacts': Contact.query.filter_by(status='new').count()
    }
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_contacts=recent_contacts)

@admin_bp.route('/rooms')
@admin_required
def rooms_list():
    rooms = Room.query.order_by(Room.created_at.desc()).all()
    return render_template('admin/rooms/list.html', rooms=rooms)

@admin_bp.route('/rooms/create', methods=['GET', 'POST'])
@admin_required
def rooms_create():
    if request.method == 'POST':
        room = Room(
            slug=request.form.get('slug'),
            name_vi=request.form.get('name_vi'),
            name_en=request.form.get('name_en'),
            description_vi=request.form.get('description_vi'),
            description_en=request.form.get('description_en'),
            price=int(request.form.get('price', 0)) if request.form.get('price') else None,
            area=int(request.form.get('area', 0)) if request.form.get('area') else None,
            capacity=int(request.form.get('capacity', 0)) if request.form.get('capacity') else None,
            room_type=request.form.get('room_type'),
            amenities=request.form.get('amenities'),
            video_url=request.form.get('video_url'),
            is_featured=request.form.get('is_featured') == 'on',
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(room)
        db.session.commit()
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        
        sort_order = 0
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'rooms')
                if url:
                    room_img = RoomImage(room_id=room.id, url=url, sort_order=sort_order)
                    db.session.add(room_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                room_img = RoomImage(room_id=room.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(room_img)
                sort_order += 1
        
        db.session.commit()
        
        flash('Đã tạo phòng mới thành công!', 'success')
        return redirect(url_for('admin.rooms_list'))
    
    return render_template('admin/rooms/form.html', room=None)

@admin_bp.route('/rooms/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def rooms_edit(id):
    room = Room.query.get_or_404(id)
    
    if request.method == 'POST':
        room.slug = request.form.get('slug')
        room.name_vi = request.form.get('name_vi')
        room.name_en = request.form.get('name_en')
        room.description_vi = request.form.get('description_vi')
        room.description_en = request.form.get('description_en')
        room.price = int(request.form.get('price', 0)) if request.form.get('price') else None
        room.area = int(request.form.get('area', 0)) if request.form.get('area') else None
        room.capacity = int(request.form.get('capacity', 0)) if request.form.get('capacity') else None
        room.room_type = request.form.get('room_type')
        room.amenities = request.form.get('amenities')
        room.video_url = request.form.get('video_url')
        room.is_featured = request.form.get('is_featured') == 'on'
        room.is_active = request.form.get('is_active') == 'on'
        
        keep_images = request.form.getlist('keep_images[]')
        RoomImage.query.filter(RoomImage.room_id == room.id, ~RoomImage.id.in_([int(x) for x in keep_images if x])).delete(synchronize_session=False)
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        
        max_order = db.session.query(db.func.max(RoomImage.sort_order)).filter_by(room_id=room.id).scalar() or -1
        sort_order = max_order + 1
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'rooms')
                if url:
                    room_img = RoomImage(room_id=room.id, url=url, sort_order=sort_order)
                    db.session.add(room_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                room_img = RoomImage(room_id=room.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(room_img)
                sort_order += 1
        
        db.session.commit()
        flash('Đã cập nhật phòng thành công!', 'success')
        return redirect(url_for('admin.rooms_list'))
    
    return render_template('admin/rooms/form.html', room=room)

@admin_bp.route('/rooms/<int:id>/delete', methods=['POST'])
@admin_required
def rooms_delete(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    flash('Đã xóa phòng thành công!', 'success')
    return redirect(url_for('admin.rooms_list'))

@admin_bp.route('/restaurants')
@admin_required
def restaurants_list():
    restaurants = Restaurant.query.order_by(Restaurant.created_at.desc()).all()
    return render_template('admin/restaurants/list.html', restaurants=restaurants)

@admin_bp.route('/restaurants/create', methods=['GET', 'POST'])
@admin_required
def restaurants_create():
    if request.method == 'POST':
        restaurant = Restaurant(
            slug=request.form.get('slug'),
            name_vi=request.form.get('name_vi'),
            name_en=request.form.get('name_en'),
            description_vi=request.form.get('description_vi'),
            description_en=request.form.get('description_en'),
            category_vi=request.form.get('category_vi'),
            category_en=request.form.get('category_en'),
            hours=request.form.get('hours'),
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(restaurant)
        db.session.commit()
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        sort_order = 0
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'restaurants')
                if url:
                    rest_img = RestaurantImage(restaurant_id=restaurant.id, url=url, sort_order=sort_order)
                    db.session.add(rest_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                rest_img = RestaurantImage(restaurant_id=restaurant.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(rest_img)
                sort_order += 1
        
        db.session.commit()
        flash('Đã tạo nhà hàng mới thành công!', 'success')
        return redirect(url_for('admin.restaurants_list'))
    
    return render_template('admin/restaurants/form.html', restaurant=None)

@admin_bp.route('/restaurants/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def restaurants_edit(id):
    restaurant = Restaurant.query.get_or_404(id)
    
    if request.method == 'POST':
        restaurant.slug = request.form.get('slug')
        restaurant.name_vi = request.form.get('name_vi')
        restaurant.name_en = request.form.get('name_en')
        restaurant.description_vi = request.form.get('description_vi')
        restaurant.description_en = request.form.get('description_en')
        restaurant.category_vi = request.form.get('category_vi')
        restaurant.category_en = request.form.get('category_en')
        restaurant.hours = request.form.get('hours')
        restaurant.is_active = request.form.get('is_active') == 'on'
        
        keep_images = request.form.getlist('keep_images[]')
        RestaurantImage.query.filter(RestaurantImage.restaurant_id == restaurant.id, ~RestaurantImage.id.in_([int(x) for x in keep_images if x])).delete(synchronize_session=False)
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        max_order = db.session.query(db.func.max(RestaurantImage.sort_order)).filter_by(restaurant_id=restaurant.id).scalar() or -1
        sort_order = max_order + 1
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'restaurants')
                if url:
                    rest_img = RestaurantImage(restaurant_id=restaurant.id, url=url, sort_order=sort_order)
                    db.session.add(rest_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                rest_img = RestaurantImage(restaurant_id=restaurant.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(rest_img)
                sort_order += 1
        
        db.session.commit()
        flash('Đã cập nhật nhà hàng thành công!', 'success')
        return redirect(url_for('admin.restaurants_list'))
    
    return render_template('admin/restaurants/form.html', restaurant=restaurant)

@admin_bp.route('/restaurants/<int:id>/delete', methods=['POST'])
@admin_required
def restaurants_delete(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    flash('Đã xóa nhà hàng thành công!', 'success')
    return redirect(url_for('admin.restaurants_list'))

@admin_bp.route('/amenities')
@admin_required
def amenities_list():
    amenities = Amenity.query.order_by(Amenity.created_at.desc()).all()
    return render_template('admin/amenities/list.html', amenities=amenities)

@admin_bp.route('/amenities/create', methods=['GET', 'POST'])
@admin_required
def amenities_create():
    if request.method == 'POST':
        amenity = Amenity(
            slug=request.form.get('slug'),
            name_vi=request.form.get('name_vi'),
            name_en=request.form.get('name_en'),
            description_vi=request.form.get('description_vi'),
            description_en=request.form.get('description_en'),
            icon=request.form.get('icon'),
            video_url=request.form.get('video_url'),
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(amenity)
        db.session.commit()
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        sort_order = 0
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'amenities')
                if url:
                    am_img = AmenityImage(amenity_id=amenity.id, url=url, sort_order=sort_order)
                    db.session.add(am_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                am_img = AmenityImage(amenity_id=amenity.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(am_img)
                sort_order += 1
        
        db.session.commit()
        flash('Đã tạo tiện ích mới thành công!', 'success')
        return redirect(url_for('admin.amenities_list'))
    
    return render_template('admin/amenities/form.html', amenity=None)

@admin_bp.route('/amenities/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def amenities_edit(id):
    amenity = Amenity.query.get_or_404(id)
    
    if request.method == 'POST':
        amenity.slug = request.form.get('slug')
        amenity.name_vi = request.form.get('name_vi')
        amenity.name_en = request.form.get('name_en')
        amenity.description_vi = request.form.get('description_vi')
        amenity.description_en = request.form.get('description_en')
        amenity.icon = request.form.get('icon')
        amenity.video_url = request.form.get('video_url')
        amenity.is_active = request.form.get('is_active') == 'on'
        
        keep_images = request.form.getlist('keep_images[]')
        AmenityImage.query.filter(AmenityImage.amenity_id == amenity.id, ~AmenityImage.id.in_([int(x) for x in keep_images if x])).delete(synchronize_session=False)
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        max_order = db.session.query(db.func.max(AmenityImage.sort_order)).filter_by(amenity_id=amenity.id).scalar() or -1
        sort_order = max_order + 1
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'amenities')
                if url:
                    am_img = AmenityImage(amenity_id=amenity.id, url=url, sort_order=sort_order)
                    db.session.add(am_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                am_img = AmenityImage(amenity_id=amenity.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(am_img)
                sort_order += 1
        
        db.session.commit()
        flash('Đã cập nhật tiện ích thành công!', 'success')
        return redirect(url_for('admin.amenities_list'))
    
    return render_template('admin/amenities/form.html', amenity=amenity)

@admin_bp.route('/amenities/<int:id>/delete', methods=['POST'])
@admin_required
def amenities_delete(id):
    amenity = Amenity.query.get_or_404(id)
    db.session.delete(amenity)
    db.session.commit()
    flash('Đã xóa tiện ích thành công!', 'success')
    return redirect(url_for('admin.amenities_list'))

@admin_bp.route('/experiences')
@admin_required
def experiences_list():
    experiences = Experience.query.order_by(Experience.created_at.desc()).all()
    return render_template('admin/experiences/list.html', experiences=experiences)

@admin_bp.route('/experiences/create', methods=['GET', 'POST'])
@admin_required
def experiences_create():
    if request.method == 'POST':
        experience = Experience(
            slug=request.form.get('slug'),
            title_vi=request.form.get('title_vi'),
            title_en=request.form.get('title_en'),
            short_desc_vi=request.form.get('short_desc_vi'),
            short_desc_en=request.form.get('short_desc_en'),
            content_vi=request.form.get('content_vi'),
            content_en=request.form.get('content_en'),
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(experience)
        db.session.commit()
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        sort_order = 0
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'experiences')
                if url:
                    exp_img = ExperienceImage(experience_id=experience.id, url=url, sort_order=sort_order)
                    db.session.add(exp_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                exp_img = ExperienceImage(experience_id=experience.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(exp_img)
                sort_order += 1
        
        video_urls = request.form.getlist('video_urls[]')
        video_titles_vi = request.form.getlist('video_titles_vi[]')
        video_titles_en = request.form.getlist('video_titles_en[]')
        for i, video_url in enumerate(video_urls):
            if video_url:
                exp_vid = ExperienceVideo(
                    experience_id=experience.id,
                    url=video_url,
                    title_vi=video_titles_vi[i] if i < len(video_titles_vi) else '',
                    title_en=video_titles_en[i] if i < len(video_titles_en) else '',
                    sort_order=i
                )
                db.session.add(exp_vid)
        
        db.session.commit()
        flash('Đã tạo trải nghiệm mới thành công!', 'success')
        return redirect(url_for('admin.experiences_list'))
    
    return render_template('admin/experiences/form.html', experience=None)

@admin_bp.route('/experiences/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def experiences_edit(id):
    experience = Experience.query.get_or_404(id)
    
    if request.method == 'POST':
        experience.slug = request.form.get('slug')
        experience.title_vi = request.form.get('title_vi')
        experience.title_en = request.form.get('title_en')
        experience.short_desc_vi = request.form.get('short_desc_vi')
        experience.short_desc_en = request.form.get('short_desc_en')
        experience.content_vi = request.form.get('content_vi')
        experience.content_en = request.form.get('content_en')
        experience.is_active = request.form.get('is_active') == 'on'
        
        keep_images = request.form.getlist('keep_images[]')
        ExperienceImage.query.filter(ExperienceImage.experience_id == experience.id, ~ExperienceImage.id.in_([int(x) for x in keep_images if x])).delete(synchronize_session=False)
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        max_order = db.session.query(db.func.max(ExperienceImage.sort_order)).filter_by(experience_id=experience.id).scalar() or -1
        sort_order = max_order + 1
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'experiences')
                if url:
                    exp_img = ExperienceImage(experience_id=experience.id, url=url, sort_order=sort_order)
                    db.session.add(exp_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                exp_img = ExperienceImage(experience_id=experience.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(exp_img)
                sort_order += 1
        
        ExperienceVideo.query.filter_by(experience_id=experience.id).delete()
        video_urls = request.form.getlist('video_urls[]')
        video_titles_vi = request.form.getlist('video_titles_vi[]')
        video_titles_en = request.form.getlist('video_titles_en[]')
        for i, video_url in enumerate(video_urls):
            if video_url:
                exp_vid = ExperienceVideo(
                    experience_id=experience.id,
                    url=video_url,
                    title_vi=video_titles_vi[i] if i < len(video_titles_vi) else '',
                    title_en=video_titles_en[i] if i < len(video_titles_en) else '',
                    sort_order=i
                )
                db.session.add(exp_vid)
        
        db.session.commit()
        flash('Đã cập nhật trải nghiệm thành công!', 'success')
        return redirect(url_for('admin.experiences_list'))
    
    return render_template('admin/experiences/form.html', experience=experience)

@admin_bp.route('/experiences/<int:id>/delete', methods=['POST'])
@admin_required
def experiences_delete(id):
    experience = Experience.query.get_or_404(id)
    db.session.delete(experience)
    db.session.commit()
    flash('Đã xóa trải nghiệm thành công!', 'success')
    return redirect(url_for('admin.experiences_list'))

@admin_bp.route('/steam')
@admin_required
def steam_list():
    programs = SteamProgram.query.order_by(SteamProgram.created_at.desc()).all()
    return render_template('admin/steam/list.html', programs=programs)

@admin_bp.route('/steam/create', methods=['GET', 'POST'])
@admin_required
def steam_create():
    if request.method == 'POST':
        program = SteamProgram(
            slug=request.form.get('slug'),
            title_vi=request.form.get('title_vi'),
            title_en=request.form.get('title_en'),
            short_desc_vi=request.form.get('short_desc_vi'),
            short_desc_en=request.form.get('short_desc_en'),
            content_vi=request.form.get('content_vi'),
            content_en=request.form.get('content_en'),
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(program)
        db.session.commit()
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        sort_order = 0
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'steam')
                if url:
                    st_img = SteamImage(steam_id=program.id, url=url, sort_order=sort_order)
                    db.session.add(st_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                st_img = SteamImage(steam_id=program.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(st_img)
                sort_order += 1
        
        video_urls = request.form.getlist('video_urls[]')
        video_titles_vi = request.form.getlist('video_titles_vi[]')
        video_titles_en = request.form.getlist('video_titles_en[]')
        for i, video_url in enumerate(video_urls):
            if video_url:
                st_vid = SteamVideo(
                    steam_id=program.id,
                    url=video_url,
                    title_vi=video_titles_vi[i] if i < len(video_titles_vi) else '',
                    title_en=video_titles_en[i] if i < len(video_titles_en) else '',
                    sort_order=i
                )
                db.session.add(st_vid)
        
        db.session.commit()
        flash('Đã tạo chương trình STEAM mới thành công!', 'success')
        return redirect(url_for('admin.steam_list'))
    
    return render_template('admin/steam/form.html', program=None)

@admin_bp.route('/steam/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def steam_edit(id):
    program = SteamProgram.query.get_or_404(id)
    
    if request.method == 'POST':
        program.slug = request.form.get('slug')
        program.title_vi = request.form.get('title_vi')
        program.title_en = request.form.get('title_en')
        program.short_desc_vi = request.form.get('short_desc_vi')
        program.short_desc_en = request.form.get('short_desc_en')
        program.content_vi = request.form.get('content_vi')
        program.content_en = request.form.get('content_en')
        program.is_active = request.form.get('is_active') == 'on'
        
        keep_images = request.form.getlist('keep_images[]')
        SteamImage.query.filter(SteamImage.steam_id == program.id, ~SteamImage.id.in_([int(x) for x in keep_images if x])).delete(synchronize_session=False)
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        max_order = db.session.query(db.func.max(SteamImage.sort_order)).filter_by(steam_id=program.id).scalar() or -1
        sort_order = max_order + 1
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'steam')
                if url:
                    st_img = SteamImage(steam_id=program.id, url=url, sort_order=sort_order)
                    db.session.add(st_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                st_img = SteamImage(steam_id=program.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(st_img)
                sort_order += 1
        
        SteamVideo.query.filter_by(steam_id=program.id).delete()
        video_urls = request.form.getlist('video_urls[]')
        video_titles_vi = request.form.getlist('video_titles_vi[]')
        video_titles_en = request.form.getlist('video_titles_en[]')
        for i, video_url in enumerate(video_urls):
            if video_url:
                st_vid = SteamVideo(
                    steam_id=program.id,
                    url=video_url,
                    title_vi=video_titles_vi[i] if i < len(video_titles_vi) else '',
                    title_en=video_titles_en[i] if i < len(video_titles_en) else '',
                    sort_order=i
                )
                db.session.add(st_vid)
        
        db.session.commit()
        flash('Đã cập nhật chương trình STEAM thành công!', 'success')
        return redirect(url_for('admin.steam_list'))
    
    return render_template('admin/steam/form.html', program=program)

@admin_bp.route('/steam/<int:id>/delete', methods=['POST'])
@admin_required
def steam_delete(id):
    program = SteamProgram.query.get_or_404(id)
    db.session.delete(program)
    db.session.commit()
    flash('Đã xóa chương trình STEAM thành công!', 'success')
    return redirect(url_for('admin.steam_list'))

@admin_bp.route('/events')
@admin_required
def events_list():
    events = Event.query.order_by(Event.created_at.desc()).all()
    return render_template('admin/events/list.html', events=events)

@admin_bp.route('/events/create', methods=['GET', 'POST'])
@admin_required
def events_create():
    if request.method == 'POST':
        event = Event(
            slug=request.form.get('slug'),
            title_vi=request.form.get('title_vi'),
            title_en=request.form.get('title_en'),
            description_vi=request.form.get('description_vi'),
            description_en=request.form.get('description_en'),
            capacity=int(request.form.get('capacity', 0)) if request.form.get('capacity') else None,
            price=int(request.form.get('price', 0)) if request.form.get('price') else None,
            features=request.form.get('features'),
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(event)
        db.session.commit()
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        sort_order = 0
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'events')
                if url:
                    ev_img = EventImage(event_id=event.id, url=url, sort_order=sort_order)
                    db.session.add(ev_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                ev_img = EventImage(event_id=event.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(ev_img)
                sort_order += 1
        
        db.session.commit()
        flash('Đã tạo sự kiện mới thành công!', 'success')
        return redirect(url_for('admin.events_list'))
    
    return render_template('admin/events/form.html', event=None)

@admin_bp.route('/events/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def events_edit(id):
    event = Event.query.get_or_404(id)
    
    if request.method == 'POST':
        event.slug = request.form.get('slug')
        event.title_vi = request.form.get('title_vi')
        event.title_en = request.form.get('title_en')
        event.description_vi = request.form.get('description_vi')
        event.description_en = request.form.get('description_en')
        event.capacity = int(request.form.get('capacity', 0)) if request.form.get('capacity') else None
        event.price = int(request.form.get('price', 0)) if request.form.get('price') else None
        event.features = request.form.get('features')
        event.is_active = request.form.get('is_active') == 'on'
        
        keep_images = request.form.getlist('keep_images[]')
        EventImage.query.filter(EventImage.event_id == event.id, ~EventImage.id.in_([int(x) for x in keep_images if x])).delete(synchronize_session=False)
        
        uploaded_files = request.files.getlist('image_files[]')
        image_urls = request.form.getlist('images[]')
        max_order = db.session.query(db.func.max(EventImage.sort_order)).filter_by(event_id=event.id).scalar() or -1
        sort_order = max_order + 1
        
        for file in uploaded_files:
            if file and file.filename:
                url = save_uploaded_file(file, 'events')
                if url:
                    ev_img = EventImage(event_id=event.id, url=url, sort_order=sort_order)
                    db.session.add(ev_img)
                    sort_order += 1
        
        for img_url in image_urls:
            if img_url and img_url.strip():
                ev_img = EventImage(event_id=event.id, url=img_url.strip(), sort_order=sort_order)
                db.session.add(ev_img)
                sort_order += 1
        
        db.session.commit()
        flash('Đã cập nhật sự kiện thành công!', 'success')
        return redirect(url_for('admin.events_list'))
    
    return render_template('admin/events/form.html', event=event)

@admin_bp.route('/events/<int:id>/delete', methods=['POST'])
@admin_required
def events_delete(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Đã xóa sự kiện thành công!', 'success')
    return redirect(url_for('admin.events_list'))

@admin_bp.route('/news')
@admin_required
def news_list():
    news_items = News.query.order_by(News.created_at.desc()).all()
    return render_template('admin/news/list.html', news_items=news_items)

@admin_bp.route('/news/create', methods=['GET', 'POST'])
@admin_required
def news_create():
    if request.method == 'POST':
        image_url = request.form.get('image_url', '')
        
        uploaded_file = request.files.get('image_file')
        if uploaded_file and uploaded_file.filename:
            url = save_uploaded_file(uploaded_file, 'news')
            if url:
                image_url = url
        
        news = News(
            slug=request.form.get('slug'),
            title_vi=request.form.get('title_vi'),
            title_en=request.form.get('title_en'),
            excerpt_vi=request.form.get('excerpt_vi'),
            excerpt_en=request.form.get('excerpt_en'),
            content_vi=request.form.get('content_vi'),
            content_en=request.form.get('content_en'),
            category=request.form.get('category'),
            image_url=image_url,
            status=request.form.get('status', 'draft'),
            published_at=datetime.utcnow() if request.form.get('status') == 'published' else None
        )
        db.session.add(news)
        db.session.commit()
        
        flash('Đã tạo tin tức mới thành công!', 'success')
        return redirect(url_for('admin.news_list'))
    
    return render_template('admin/news/form.html', news=None)

@admin_bp.route('/news/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def news_edit(id):
    news = News.query.get_or_404(id)
    
    if request.method == 'POST':
        news.slug = request.form.get('slug')
        news.title_vi = request.form.get('title_vi')
        news.title_en = request.form.get('title_en')
        news.excerpt_vi = request.form.get('excerpt_vi')
        news.excerpt_en = request.form.get('excerpt_en')
        news.content_vi = request.form.get('content_vi')
        news.content_en = request.form.get('content_en')
        news.category = request.form.get('category')
        
        uploaded_file = request.files.get('image_file')
        if uploaded_file and uploaded_file.filename:
            url = save_uploaded_file(uploaded_file, 'news')
            if url:
                news.image_url = url
        elif request.form.get('image_url'):
            news.image_url = request.form.get('image_url')
        
        news.status = request.form.get('status', 'draft')
        if news.status == 'published' and not news.published_at:
            news.published_at = datetime.utcnow()
        
        db.session.commit()
        flash('Đã cập nhật tin tức thành công!', 'success')
        return redirect(url_for('admin.news_list'))
    
    return render_template('admin/news/form.html', news=news)

@admin_bp.route('/news/<int:id>/delete', methods=['POST'])
@admin_required
def news_delete(id):
    news = News.query.get_or_404(id)
    db.session.delete(news)
    db.session.commit()
    flash('Đã xóa tin tức thành công!', 'success')
    return redirect(url_for('admin.news_list'))

@admin_bp.route('/gallery')
@admin_required
def gallery_list():
    items = GalleryItem.query.order_by(GalleryItem.sort_order, GalleryItem.created_at.desc()).all()
    return render_template('admin/gallery/list.html', items=items)

@admin_bp.route('/gallery/create', methods=['GET', 'POST'])
@admin_required
def gallery_create():
    if request.method == 'POST':
        item_type = request.form.get('type')
        url = request.form.get('url', '')
        thumb_url = request.form.get('thumb_url', '')
        
        if item_type == 'image':
            uploaded_file = request.files.get('image_file')
            if uploaded_file and uploaded_file.filename:
                uploaded_url = save_uploaded_file(uploaded_file, 'gallery')
                if uploaded_url:
                    url = uploaded_url
                    thumb_url = uploaded_url
        
        item = GalleryItem(
            type=item_type,
            title_vi=request.form.get('title_vi'),
            title_en=request.form.get('title_en'),
            url=url,
            thumb_url=thumb_url,
            category=request.form.get('category'),
            sort_order=int(request.form.get('sort_order', 0)) if request.form.get('sort_order') else 0,
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(item)
        db.session.commit()
        
        flash('Đã thêm mục gallery mới thành công!', 'success')
        return redirect(url_for('admin.gallery_list'))
    
    return render_template('admin/gallery/form.html', item=None)

@admin_bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def gallery_edit(id):
    item = GalleryItem.query.get_or_404(id)
    
    if request.method == 'POST':
        item.type = request.form.get('type')
        item.title_vi = request.form.get('title_vi')
        item.title_en = request.form.get('title_en')
        item.category = request.form.get('category')
        item.sort_order = int(request.form.get('sort_order', 0)) if request.form.get('sort_order') else 0
        item.is_active = request.form.get('is_active') == 'on'
        
        if item.type == 'image':
            uploaded_file = request.files.get('image_file')
            if uploaded_file and uploaded_file.filename:
                uploaded_url = save_uploaded_file(uploaded_file, 'gallery')
                if uploaded_url:
                    item.url = uploaded_url
                    item.thumb_url = uploaded_url
            elif request.form.get('url'):
                item.url = request.form.get('url')
                item.thumb_url = request.form.get('thumb_url') or request.form.get('url')
        else:
            item.url = request.form.get('url')
            item.thumb_url = request.form.get('thumb_url')
        
        db.session.commit()
        flash('Đã cập nhật mục gallery thành công!', 'success')
        return redirect(url_for('admin.gallery_list'))
    
    return render_template('admin/gallery/form.html', item=item)

@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
@admin_required
def gallery_delete(id):
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Đã xóa mục gallery thành công!', 'success')
    return redirect(url_for('admin.gallery_list'))

@admin_bp.route('/contacts')
@admin_required
def contacts_list():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts/list.html', contacts=contacts)

@admin_bp.route('/contacts/<int:id>')
@admin_required
def contacts_view(id):
    contact = Contact.query.get_or_404(id)
    if contact.status == 'new':
        contact.status = 'read'
        db.session.commit()
    return render_template('admin/contacts/view.html', contact=contact)

@admin_bp.route('/contacts/<int:id>/delete', methods=['POST'])
@admin_required
def contacts_delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Đã xóa liên hệ thành công!', 'success')
    return redirect(url_for('admin.contacts_list'))

@admin_bp.route('/newsletters')
@admin_required
def newsletters_list():
    newsletters = Newsletter.query.order_by(Newsletter.subscribed_at.desc()).all()
    return render_template('admin/newsletters/list.html', newsletters=newsletters)

@admin_bp.route('/newsletters/<int:id>/toggle', methods=['POST'])
@admin_required
def newsletters_toggle(id):
    newsletter = Newsletter.query.get_or_404(id)
    newsletter.is_active = not newsletter.is_active
    if not newsletter.is_active:
        newsletter.unsubscribed_at = datetime.utcnow()
    else:
        newsletter.unsubscribed_at = None
    db.session.commit()
    status = 'kích hoạt' if newsletter.is_active else 'hủy kích hoạt'
    flash(f'Đã {status} email {newsletter.email}!', 'success')
    return redirect(url_for('admin.newsletters_list'))

@admin_bp.route('/newsletters/<int:id>/delete', methods=['POST'])
@admin_required
def newsletters_delete(id):
    newsletter = Newsletter.query.get_or_404(id)
    db.session.delete(newsletter)
    db.session.commit()
    flash('Đã xóa email thành công!', 'success')
    return redirect(url_for('admin.newsletters_list'))

@admin_bp.route('/upload', methods=['POST'])
@admin_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        return jsonify({'url': '/' + filepath})
    
    return jsonify({'error': 'File type not allowed'}), 400

@admin_bp.route('/banners')
@admin_required
def banners_list():
    banners = Banner.query.order_by(Banner.sort_order, Banner.created_at.desc()).all()
    return render_template('admin/banners/list.html', banners=banners)

@admin_bp.route('/banners/create', methods=['GET', 'POST'])
@admin_required
def banners_create():
    if request.method == 'POST':
        image_url = None
        
        uploaded_file = request.files.get('image_file')
        if uploaded_file and uploaded_file.filename:
            image_url = save_uploaded_file(uploaded_file, 'banners')
        
        if not image_url:
            image_url = request.form.get('image_url')
        
        if not image_url:
            flash('Vui lòng chọn hình ảnh cho banner.', 'error')
            return render_template('admin/banners/form.html', banner=None)
        
        banner = Banner(
            title_vi=request.form.get('title_vi'),
            title_en=request.form.get('title_en'),
            subtitle_vi=request.form.get('subtitle_vi'),
            subtitle_en=request.form.get('subtitle_en'),
            description_vi=request.form.get('description_vi'),
            description_en=request.form.get('description_en'),
            button_text_vi=request.form.get('button_text_vi'),
            button_text_en=request.form.get('button_text_en'),
            button_link=request.form.get('button_link'),
            image_url=image_url,
            icon=request.form.get('icon'),
            sort_order=int(request.form.get('sort_order', 0)) if request.form.get('sort_order') else 0,
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(banner)
        db.session.commit()
        
        flash('Đã tạo banner mới thành công!', 'success')
        return redirect(url_for('admin.banners_list'))
    
    return render_template('admin/banners/form.html', banner=None)

@admin_bp.route('/banners/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def banners_edit(id):
    banner = Banner.query.get_or_404(id)
    
    if request.method == 'POST':
        banner.title_vi = request.form.get('title_vi')
        banner.title_en = request.form.get('title_en')
        banner.subtitle_vi = request.form.get('subtitle_vi')
        banner.subtitle_en = request.form.get('subtitle_en')
        banner.description_vi = request.form.get('description_vi')
        banner.description_en = request.form.get('description_en')
        banner.button_text_vi = request.form.get('button_text_vi')
        banner.button_text_en = request.form.get('button_text_en')
        banner.button_link = request.form.get('button_link')
        banner.icon = request.form.get('icon')
        banner.sort_order = int(request.form.get('sort_order', 0)) if request.form.get('sort_order') else 0
        banner.is_active = request.form.get('is_active') == 'on'
        
        uploaded_file = request.files.get('image_file')
        if uploaded_file and uploaded_file.filename:
            image_url = save_uploaded_file(uploaded_file, 'banners')
            if image_url:
                banner.image_url = image_url
        elif request.form.get('image_url'):
            banner.image_url = request.form.get('image_url')
        
        db.session.commit()
        flash('Đã cập nhật banner thành công!', 'success')
        return redirect(url_for('admin.banners_list'))
    
    return render_template('admin/banners/form.html', banner=banner)

@admin_bp.route('/banners/<int:id>/delete', methods=['POST'])
@admin_required
def banners_delete(id):
    banner = Banner.query.get_or_404(id)
    db.session.delete(banner)
    db.session.commit()
    flash('Đã xóa banner thành công!', 'success')
    return redirect(url_for('admin.banners_list'))

@admin_bp.route('/banners/<int:id>/toggle', methods=['POST'])
@admin_required
def banners_toggle(id):
    banner = Banner.query.get_or_404(id)
    banner.is_active = not banner.is_active
    db.session.commit()
    status = 'bật' if banner.is_active else 'tắt'
    flash(f'Đã {status} banner thành công!', 'success')
    return redirect(url_for('admin.banners_list'))

@admin_bp.route('/effects')
@admin_required
def effects():
    setting = SiteSetting.query.filter_by(key='holiday_effect').first()
    current_effect = setting.value if setting else 'none'
    return render_template('admin/effects.html', current_effect=current_effect)

@admin_bp.route('/effects', methods=['POST'])
@admin_required
def effects_save():
    effect = request.form.get('effect', 'none')
    
    setting = SiteSetting.query.filter_by(key='holiday_effect').first()
    if setting:
        setting.value = effect
    else:
        setting = SiteSetting(key='holiday_effect', value=effect)
        db.session.add(setting)
    
    db.session.commit()
    
    effect_names = {
        'none': 'Tắt hiệu ứng',
        'snow': 'Tuyết rơi (Giáng sinh)',
        'fireworks': 'Pháo hoa (Năm mới)',
        'sakura': 'Hoa anh đào (Xuân)',
        'leaves': 'Lá rơi (Thu)',
        'hearts': 'Trái tim (Valentine)'
    }
    flash(f'Đã bật: {effect_names.get(effect, effect)}', 'success')
    return redirect(url_for('admin.effects'))

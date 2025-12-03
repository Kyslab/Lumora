# Lumora Resort Website

## Overview
Website resort đa ngôn ngữ (Việt/Anh) cho Lumora Resort với đầy đủ các tính năng giới thiệu và đặt phòng. Bao gồm admin panel để quản lý nội dung.

## Tech Stack
- **Backend**: Python Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Database**: PostgreSQL (Neon-backed)
- **Frontend**: HTML5, TailwindCSS (CDN), JavaScript
- **Template Engine**: Jinja2
- **Fonts**: Google Fonts (Playfair Display, Open Sans)
- **Icons**: Font Awesome

## Project Structure
```
├── app.py                 # Main Flask application with routes and data
├── models.py              # SQLAlchemy database models
├── admin.py               # Admin blueprint with CRUD routes
├── templates/
│   ├── base.html          # Base template with header, footer, nav
│   ├── home.html          # Homepage with hero, rooms preview, amenities
│   ├── accommodation.html # Room listing page
│   ├── room_detail.html   # Individual room details
│   ├── dining.html        # Restaurant listing
│   ├── restaurant_detail.html
│   ├── amenities.html     # Amenities (pool, zoo, garden)
│   ├── experiences.html   # Activities and experiences
│   ├── steam.html         # STEAM education programs
│   ├── events.html        # Event spaces
│   ├── news.html          # News and promotions
│   ├── news_detail.html
│   ├── gallery.html       # Photo and video gallery
│   ├── contact.html       # Contact form and booking
│   ├── 404.html           # Error page
│   └── admin/             # Admin panel templates
│       ├── base.html      # Admin base layout
│       ├── login.html     # Admin login page
│       ├── dashboard.html # Admin dashboard
│       ├── rooms/         # Room CRUD templates
│       ├── restaurants/   # Restaurant CRUD templates
│       ├── amenities/     # Amenity CRUD templates
│       ├── experiences/   # Experience CRUD templates
│       ├── steam/         # STEAM CRUD templates
│       ├── events/        # Event CRUD templates
│       ├── news/          # News CRUD templates
│       ├── gallery/       # Gallery CRUD templates
│       └── contacts/      # Contact view templates
└── attached_assets/       # User uploaded files
```

## Features
1. **Trang Chủ**: Hero banner, video YouTube, giới thiệu resort, phòng nổi bật, tiện ích
2. **Lưu Trú**: Danh sách phòng (Deluxe, Glamping, Bungalow), filter theo loại, chi tiết phòng
3. **Ẩm Thực**: 3 nhà hàng (Restaurant, BBQ Garden, Café & Bar), menu món ăn
4. **Tiện Ích**: Vườn thú, vườn cây, bể bơi vô cực
5. **Trải Nghiệm**: 
   - Tham Quan Check-in: Bài viết với hình ảnh và video
   - Khu Trò Chơi Mạo Hiểm: Bài viết với hình ảnh và video
6. **Giáo Dục STEAM** (Menu riêng):
   - Giới Thiệu Chương Trình: Bài viết chi tiết về STEAM
   - Workshop Kỹ Năng: Các workshop thực hành
   - Đăng Ký Tham Gia: Form đăng ký với validation
7. **Sự Kiện**: Hội trường, sân team building
8. **Tin Tức**: Blog, ưu đãi, sự kiện
9. **Thư Viện**: Gallery hình ảnh và video
10. **Liên Hệ**: Form đặt phòng, form liên hệ, Google Maps

## Admin Panel
- **URL**: `/admin`
- **Default credentials**: admin / admin123 (CHANGE IMMEDIATELY IN PRODUCTION)
- **Features**:
  - Dashboard với thống kê tổng quan
  - Quản lý Phòng (thêm, sửa, xóa)
  - Quản lý Nhà Hàng và Menu
  - Quản lý Tiện Ích
  - Quản lý Trải Nghiệm
  - Quản lý Chương Trình STEAM
  - Quản lý Sự Kiện
  - Quản lý Tin Tức
  - Quản lý Thư Viện Ảnh/Video
  - Xem Liên Hệ từ khách hàng

## Database Models
- User: Tài khoản admin
- Room, RoomImage: Phòng và hình ảnh phòng
- Restaurant, MenuItem: Nhà hàng và menu
- Amenity, AmenityImage: Tiện ích
- Experience, ExperienceImage, ExperienceVideo: Trải nghiệm
- SteamProgram, SteamProgramImage, SteamProgramVideo: Chương trình STEAM
- Event, EventImage: Sự kiện
- News: Tin tức
- GalleryItem: Thư viện ảnh/video
- Contact: Liên hệ từ khách

## Đa Ngôn Ngữ
- Hỗ trợ Tiếng Việt và Tiếng Anh
- Chuyển đổi qua URL parameter `?lang=vi` hoặc `?lang=en`
- Tất cả nội dung admin hỗ trợ nhập song ngữ

## Responsive Design
- Mobile-first với TailwindCSS
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Mobile menu với slide animation
- Admin panel responsive

## Running the App
```bash
python app.py
```
Server chạy trên port 5000.

## Color Palette
- Primary: #2D5A27 (xanh lá đậm)
- Secondary: #8B7355 (nâu)
- Accent: #D4AF37 (vàng gold)
- Dark: #1A1A1A
- Light: #F5F5F0

## Security Notes
- Default admin password should be changed immediately after first login
- Session-based authentication with Flask-Login
- CSRF protection enabled via Flask-WTF
- Password hashing with Werkzeug

## Data Management
- Tất cả dữ liệu được lưu trong PostgreSQL database
- Dữ liệu ban đầu được seed từ script `seed_data.py`
- Admin có thể thêm/sửa/xóa tất cả nội dung qua admin panel
- Hỗ trợ song ngữ (Việt/Anh) cho tất cả các trường nội dung

## Recent Changes
- 2024-12-03: Migrated all content to database, public routes now read from database
- 2024-12-03: Added seed_data.py script for initial data population
- 2024-12-03: Added admin panel with full CRUD for all content types
- 2024-12-03: Integrated PostgreSQL database with SQLAlchemy ORM
- 2024-12-03: Contact/Booking forms now save to database
- 2024-12-02: Initial setup with all pages and features

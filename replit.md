# Lumora Resort Website

## Overview
Website resort đa ngôn ngữ (Việt/Anh) cho Lumora Resort với đầy đủ các tính năng giới thiệu và đặt phòng.

## Tech Stack
- **Backend**: Python Flask
- **Frontend**: HTML5, TailwindCSS (CDN), JavaScript
- **Template Engine**: Jinja2
- **Fonts**: Google Fonts (Playfair Display, Open Sans)
- **Icons**: Font Awesome

## Project Structure
```
├── app.py                 # Main Flask application with routes and data
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
│   └── 404.html           # Error page
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

## Đa Ngôn Ngữ
- Hỗ trợ Tiếng Việt và Tiếng Anh
- Chuyển đổi qua URL parameter `?lang=vi` hoặc `?lang=en`

## Responsive Design
- Mobile-first với TailwindCSS
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Mobile menu với slide animation

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

## Recent Changes
- 2024-12-02: Initial setup with all pages and features

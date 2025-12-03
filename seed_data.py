import os
from datetime import datetime
from app import app
from models import db, Room, RoomImage, Restaurant, RestaurantImage, MenuItem, Amenity, AmenityImage, Experience, ExperienceImage, ExperienceVideo, SteamProgram, SteamImage, SteamVideo, Event, EventImage, News, GalleryItem

def seed_rooms():
    rooms_data = [
        {
            "slug": "deluxe",
            "name_vi": "Phòng Tiêu Chuẩn / Deluxe",
            "name_en": "Standard / Deluxe Room",
            "description_vi": "Phòng tiêu chuẩn với đầy đủ tiện nghi hiện đại, view đẹp ra khu vườn hoặc hồ bơi.",
            "description_en": "Standard room with modern amenities, beautiful garden or pool view.",
            "price": 1500000,
            "area": 35,
            "capacity": 2,
            "room_type": "deluxe",
            "amenities": "WiFi miễn phí\nĐiều hòa\nTV màn hình phẳng\nMinibar\nPhòng tắm riêng",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "is_featured": True,
            "images": [
                "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
                "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800"
            ]
        },
        {
            "slug": "glamping",
            "name_vi": "Glamping / Cabin / Homestay",
            "name_en": "Glamping / Cabin / Homestay",
            "description_vi": "Trải nghiệm cắm trại sang trọng giữa thiên nhiên với đầy đủ tiện nghi.",
            "description_en": "Luxury camping experience in nature with full amenities.",
            "price": 2000000,
            "area": 40,
            "capacity": 4,
            "room_type": "glamping",
            "amenities": "WiFi miễn phí\nĐiều hòa\nKhông gian ngoài trời\nKhu BBQ riêng\nPhòng tắm riêng",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "is_featured": True,
            "images": [
                "https://images.unsplash.com/photo-1499696010180-025ef6e1a8f9?w=800",
                "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"
            ]
        },
        {
            "slug": "bungalow",
            "name_vi": "Dorm / Bungalow",
            "name_en": "Dorm / Bungalow",
            "description_vi": "Bungalow riêng biệt giữa khu vườn nhiệt đới, không gian yên tĩnh và riêng tư.",
            "description_en": "Private bungalow in tropical garden, peaceful and private space.",
            "price": 2500000,
            "area": 50,
            "capacity": 4,
            "room_type": "bungalow",
            "amenities": "WiFi miễn phí\nĐiều hòa\nBếp nhỏ\nSân vườn riêng\nPhòng tắm riêng",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "is_featured": True,
            "images": [
                "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800",
                "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800"
            ]
        }
    ]
    
    for room_data in rooms_data:
        existing = Room.query.filter_by(slug=room_data['slug']).first()
        if existing:
            continue
            
        images = room_data.pop('images')
        room = Room(**room_data)
        db.session.add(room)
        db.session.flush()
        
        for i, img_url in enumerate(images):
            img = RoomImage(room_id=room.id, url=img_url, sort_order=i)
            db.session.add(img)
    
    db.session.commit()
    print("Seeded rooms")

def seed_restaurants():
    restaurants_data = [
        {
            "slug": "restaurant1",
            "name_vi": "Nhà Hàng Lumora",
            "name_en": "Lumora Restaurant",
            "description_vi": "Nhà hàng chính phục vụ ẩm thực Việt Nam và quốc tế với không gian sang trọng.",
            "description_en": "Main restaurant serving Vietnamese and international cuisine in elegant setting.",
            "category_vi": "Nhà hàng",
            "category_en": "Restaurant",
            "hours": "06:00 - 22:00",
            "images": [
                "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800"
            ],
            "menu": [
                {"name_vi": "Phở Bò", "name_en": "Beef Pho", "price": 85000},
                {"name_vi": "Bún Chả", "name_en": "Bun Cha", "price": 75000},
                {"name_vi": "Cơm Tấm", "name_en": "Broken Rice", "price": 70000}
            ]
        },
        {
            "slug": "restaurant2",
            "name_vi": "BBQ Garden",
            "name_en": "BBQ Garden",
            "description_vi": "Khu BBQ ngoài trời với không gian xanh mát, thích hợp cho nhóm bạn và gia đình.",
            "description_en": "Outdoor BBQ area with green space, perfect for groups and families.",
            "category_vi": "BBQ",
            "category_en": "BBQ",
            "hours": "17:00 - 23:00",
            "images": [
                "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
                "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=800"
            ],
            "menu": [
                {"name_vi": "Set BBQ Hải Sản", "name_en": "Seafood BBQ Set", "price": 450000},
                {"name_vi": "Set BBQ Bò Wagyu", "name_en": "Wagyu Beef BBQ Set", "price": 650000},
                {"name_vi": "Set BBQ Gia Đình", "name_en": "Family BBQ Set", "price": 850000}
            ]
        },
        {
            "slug": "cafe",
            "name_vi": "Café & Bar Lounge",
            "name_en": "Café & Bar Lounge",
            "description_vi": "Quán café và bar với view đẹp, phục vụ đồ uống và cocktail đặc biệt.",
            "description_en": "Café and bar with beautiful view, serving drinks and special cocktails.",
            "category_vi": "Café / Bar",
            "category_en": "Café / Bar",
            "hours": "07:00 - 24:00",
            "images": [
                "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800",
                "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800"
            ],
            "menu": [
                {"name_vi": "Cà Phê Sữa Đá", "name_en": "Vietnamese Iced Coffee", "price": 45000},
                {"name_vi": "Mojito", "name_en": "Mojito", "price": 120000},
                {"name_vi": "Smoothie Trái Cây", "name_en": "Fruit Smoothie", "price": 65000}
            ]
        }
    ]
    
    for rest_data in restaurants_data:
        existing = Restaurant.query.filter_by(slug=rest_data['slug']).first()
        if existing:
            continue
            
        images = rest_data.pop('images')
        menu = rest_data.pop('menu')
        restaurant = Restaurant(**rest_data)
        db.session.add(restaurant)
        db.session.flush()
        
        for i, img_url in enumerate(images):
            img = RestaurantImage(restaurant_id=restaurant.id, url=img_url, sort_order=i)
            db.session.add(img)
        
        for i, item in enumerate(menu):
            menu_item = MenuItem(restaurant_id=restaurant.id, sort_order=i, **item)
            db.session.add(menu_item)
    
    db.session.commit()
    print("Seeded restaurants")

def seed_amenities():
    amenities_data = [
        {
            "slug": "zoo",
            "name_vi": "Vườn Thú Mini",
            "name_en": "Mini Zoo",
            "description_vi": "Vườn thú mini với nhiều loài động vật dễ thương, thích hợp cho trẻ em khám phá.",
            "description_en": "Mini zoo with cute animals, perfect for children to explore.",
            "icon": "paw",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "images": ["https://images.unsplash.com/photo-1534567153574-2b12153a87f0?w=800"]
        },
        {
            "slug": "garden",
            "name_vi": "Vườn Cây Xanh",
            "name_en": "Green Garden",
            "description_vi": "Khu vườn nhiệt đới với đa dạng cây xanh, không gian thư giãn lý tưởng.",
            "description_en": "Tropical garden with diverse plants, ideal relaxation space.",
            "icon": "leaf",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "images": ["https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800"]
        },
        {
            "slug": "pool",
            "name_vi": "Bể Bơi Vô Cực",
            "name_en": "Infinity Pool",
            "description_vi": "Bể bơi vô cực với tầm nhìn tuyệt đẹp, mở cửa từ 6h sáng đến 10h tối.",
            "description_en": "Infinity pool with stunning views, open from 6am to 10pm.",
            "icon": "swimming-pool",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "images": ["https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?w=800"]
        }
    ]
    
    for amenity_data in amenities_data:
        existing = Amenity.query.filter_by(slug=amenity_data['slug']).first()
        if existing:
            continue
            
        images = amenity_data.pop('images')
        amenity = Amenity(**amenity_data)
        db.session.add(amenity)
        db.session.flush()
        
        for i, img_url in enumerate(images):
            img = AmenityImage(amenity_id=amenity.id, url=img_url, sort_order=i)
            db.session.add(img)
    
    db.session.commit()
    print("Seeded amenities")

def seed_experiences():
    experiences_data = [
        {
            "slug": "checkin",
            "title_vi": "Tham Quan Check-in",
            "title_en": "Check-in Tour",
            "short_desc_vi": "Khám phá những điểm check-in đẹp nhất tại Lumora Resort.",
            "short_desc_en": "Discover the most beautiful check-in spots at Lumora Resort.",
            "content_vi": """<p>Lumora Resort tự hào sở hữu hàng chục điểm check-in tuyệt đẹp, mỗi góc nhỏ đều là một khung cảnh hoàn hảo cho những bức ảnh đáng nhớ của bạn.</p>
                
<h3>Các Điểm Check-in Nổi Bật</h3>

<h4>1. Cầu Gỗ Giữa Hồ Sen</h4>
<p>Cây cầu gỗ uốn lượn giữa hồ sen rộng lớn, với những bông sen hồng nở rộ vào mùa hè. Đây là điểm check-in được yêu thích nhất với ánh sáng hoàng hôn tuyệt đẹp.</p>

<h4>2. Vườn Hoa Bốn Mùa</h4>
<p>Khu vườn với hàng nghìn loài hoa từ khắp nơi trên thế giới, thay đổi theo từng mùa.</p>

<h4>3. Khu Rừng Tre Xanh</h4>
<p>Con đường nhỏ xuyên qua rừng tre xanh mát, tạo nên không gian yên bình và những bức ảnh mang phong cách Nhật Bản độc đáo.</p>

<h4>4. Bể Bơi Vô Cực</h4>
<p>Bể bơi vô cực nhìn ra núi đồi xa xa, đặc biệt đẹp vào lúc bình minh và hoàng hôn.</p>

<h3>Lịch Trình Tour Tham Quan</h3>
<ul>
    <li><strong>Tour Sáng (7:00 - 9:00):</strong> Bắt đầu từ khu vườn hoa, hồ sen, rừng tre</li>
    <li><strong>Tour Chiều (15:00 - 17:00):</strong> Khu nhà sàn, bể bơi vô cực, đồi cỏ</li>
    <li><strong>Tour Hoàng Hôn (17:00 - 19:00):</strong> Các điểm view hoàng hôn đẹp nhất</li>
</ul>

<h3>Dịch Vụ Chụp Ảnh Chuyên Nghiệp</h3>
<p>Lumora Resort cung cấp dịch vụ nhiếp ảnh chuyên nghiệp với photographer có kinh nghiệm. Liên hệ lễ tân để đặt lịch.</p>""",
            "content_en": """<p>Lumora Resort proudly features dozens of stunning check-in spots, where every corner is a perfect frame for your memorable photos.</p>

<h3>Featured Check-in Spots</h3>

<h4>1. Wooden Bridge Over Lotus Lake</h4>
<p>A winding wooden bridge across the vast lotus lake, with pink lotus blooming in summer. This is the most beloved check-in spot with beautiful sunset lighting.</p>

<h4>2. Four Seasons Flower Garden</h4>
<p>A garden with thousands of flower species from around the world, changing with each season.</p>

<h4>3. Green Bamboo Forest</h4>
<p>A small path through the cool green bamboo forest, creating a peaceful atmosphere and unique Japanese-style photos.</p>

<h4>4. Infinity Pool</h4>
<p>The infinity pool overlooking distant hills, especially beautiful at sunrise and sunset.</p>

<h3>Tour Schedule</h3>
<ul>
    <li><strong>Morning Tour (7:00 - 9:00):</strong> Starting from flower garden, lotus lake, bamboo forest</li>
    <li><strong>Afternoon Tour (15:00 - 17:00):</strong> Stilt houses, infinity pool, grass hills</li>
    <li><strong>Sunset Tour (17:00 - 19:00):</strong> Best sunset viewing spots</li>
</ul>

<h3>Professional Photography Service</h3>
<p>Lumora Resort provides professional photography services. Contact reception to book.</p>""",
            "images": [
                "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
                "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=800",
                "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800",
                "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800"
            ],
            "videos": [
                {"url": "https://www.youtube.com/embed/LXb3EKWsInQ", "title_vi": "Tour Tham Quan Resort", "title_en": "Resort Tour"},
                {"url": "https://www.youtube.com/embed/5qap5aO4i9A", "title_vi": "Điểm Check-in Đẹp Nhất", "title_en": "Best Check-in Spots"}
            ]
        },
        {
            "slug": "adventure",
            "title_vi": "Khu Trò Chơi Mạo Hiểm",
            "title_en": "Adventure Playground",
            "short_desc_vi": "Thử thách bản thân với các hoạt động mạo hiểm đầy thú vị.",
            "short_desc_en": "Challenge yourself with exciting adventure activities.",
            "content_vi": """<p>Khu Trò Chơi Mạo Hiểm tại Lumora Resort là điểm đến lý tưởng cho những ai yêu thích cảm giác mạnh.</p>

<h3>Các Hoạt Động Mạo Hiểm</h3>

<h4>1. Zipline Xuyên Rừng</h4>
<p>Bay lượn trên dây zipline dài 500m xuyên qua tán rừng xanh mát, với độ cao 50m so với mặt đất.</p>
<p><strong>Độ tuổi:</strong> Từ 10 tuổi | <strong>Thời gian:</strong> 15-20 phút</p>

<h4>2. Leo Vách Đá</h4>
<p>Khu vực leo núi nhân tạo với 5 cấp độ từ dễ đến khó.</p>
<p><strong>Độ tuổi:</strong> Từ 8 tuổi | <strong>Thời gian:</strong> 30-45 phút</p>

<h4>3. Cầu Treo Vượt Thác</h4>
<p>Đi qua cầu treo bằng gỗ dài 100m bắc qua thác nước.</p>
<p><strong>Độ tuổi:</strong> Từ 6 tuổi | <strong>Thời gian:</strong> 10-15 phút</p>

<h3>Gói Trải Nghiệm</h3>
<ul>
    <li><strong>Gói Cơ Bản:</strong> 2 hoạt động tự chọn - 300.000đ/người</li>
    <li><strong>Gói Tiêu Chuẩn:</strong> 4 hoạt động - 500.000đ/người</li>
    <li><strong>Gói VIP:</strong> Tất cả hoạt động + ảnh kỷ niệm - 800.000đ/người</li>
</ul>""",
            "content_en": """<p>The Adventure Playground at Lumora Resort is the ideal destination for thrill-seekers.</p>

<h3>Adventure Activities</h3>

<h4>1. Forest Zipline</h4>
<p>Soar on a 500m zipline through the cool green canopy, 50m above ground.</p>
<p><strong>Age:</strong> From 10 years | <strong>Duration:</strong> 15-20 minutes</p>

<h4>2. Rock Climbing</h4>
<p>Artificial climbing area with 5 difficulty levels from easy to hard.</p>
<p><strong>Age:</strong> From 8 years | <strong>Duration:</strong> 30-45 minutes</p>

<h4>3. Waterfall Suspension Bridge</h4>
<p>Cross a 100m wooden suspension bridge over a waterfall.</p>
<p><strong>Age:</strong> From 6 years | <strong>Duration:</strong> 10-15 minutes</p>

<h3>Experience Packages</h3>
<ul>
    <li><strong>Basic Package:</strong> 2 activities of choice - 300,000 VND/person</li>
    <li><strong>Standard Package:</strong> 4 activities - 500,000 VND/person</li>
    <li><strong>VIP Package:</strong> All activities + souvenir photos - 800,000 VND/person</li>
</ul>""",
            "images": [
                "https://images.unsplash.com/photo-1551632811-561732d1e306?w=800",
                "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800",
                "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800",
                "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=800"
            ],
            "videos": [
                {"url": "https://www.youtube.com/embed/LXb3EKWsInQ", "title_vi": "Khu Trò Chơi Mạo Hiểm", "title_en": "Adventure Playground"},
                {"url": "https://www.youtube.com/embed/5qap5aO4i9A", "title_vi": "Zipline Xuyên Rừng", "title_en": "Forest Zipline"}
            ]
        }
    ]
    
    for exp_data in experiences_data:
        existing = Experience.query.filter_by(slug=exp_data['slug']).first()
        if existing:
            continue
            
        images = exp_data.pop('images')
        videos = exp_data.pop('videos')
        experience = Experience(**exp_data)
        db.session.add(experience)
        db.session.flush()
        
        for i, img_url in enumerate(images):
            img = ExperienceImage(experience_id=experience.id, url=img_url, sort_order=i)
            db.session.add(img)
        
        for i, video in enumerate(videos):
            vid = ExperienceVideo(experience_id=experience.id, sort_order=i, **video)
            db.session.add(vid)
    
    db.session.commit()
    print("Seeded experiences")

def seed_steam():
    steam_data = [
        {
            "slug": "intro",
            "title_vi": "Giới Thiệu Chương Trình STEAM",
            "title_en": "STEAM Program Introduction",
            "short_desc_vi": "Khám phá chương trình giáo dục STEAM độc đáo tại Lumora Resort.",
            "short_desc_en": "Discover the unique STEAM education program at Lumora Resort.",
            "content_vi": """<p>Chương trình Giáo dục STEAM tại Lumora Resort được thiết kế đặc biệt để mang đến cho trẻ em những trải nghiệm học tập thú vị.</p>

<h3>STEAM Là Gì?</h3>
<p>STEAM là phương pháp giáo dục tích hợp 5 lĩnh vực:</p>
<ul>
    <li><strong>S - Science (Khoa học):</strong> Khám phá các hiện tượng tự nhiên</li>
    <li><strong>T - Technology (Công nghệ):</strong> Ứng dụng công nghệ vào học tập</li>
    <li><strong>E - Engineering (Kỹ thuật):</strong> Thiết kế và xây dựng</li>
    <li><strong>A - Arts (Nghệ thuật):</strong> Phát triển tư duy sáng tạo</li>
    <li><strong>M - Mathematics (Toán học):</strong> Tư duy logic</li>
</ul>

<h3>Các Chương Trình Nổi Bật</h3>
<ul>
    <li><strong>STEAM Camp (3-5 ngày):</strong> Trại hè STEAM với nhiều hoạt động đa dạng</li>
    <li><strong>STEAM Weekend (2 ngày):</strong> Cuối tuần khám phá khoa học</li>
    <li><strong>STEAM Day Trip (1 ngày):</strong> Một ngày trải nghiệm STEAM</li>
</ul>

<h3>Đối Tượng Tham Gia</h3>
<ul>
    <li>Trẻ em từ 6-15 tuổi</li>
    <li>Các nhóm học sinh từ trường học</li>
    <li>Gia đình muốn trải nghiệm cùng con</li>
</ul>""",
            "content_en": """<p>The STEAM Education Program at Lumora Resort is specially designed to provide children with exciting learning experiences.</p>

<h3>What is STEAM?</h3>
<p>STEAM is an integrated educational approach covering 5 areas:</p>
<ul>
    <li><strong>S - Science:</strong> Exploring natural phenomena</li>
    <li><strong>T - Technology:</strong> Applying technology to learning</li>
    <li><strong>E - Engineering:</strong> Design and building</li>
    <li><strong>A - Arts:</strong> Developing creative thinking</li>
    <li><strong>M - Mathematics:</strong> Logical thinking</li>
</ul>

<h3>Featured Programs</h3>
<ul>
    <li><strong>STEAM Camp (3-5 days):</strong> Summer STEAM camp with diverse activities</li>
    <li><strong>STEAM Weekend (2 days):</strong> Science discovery weekend</li>
    <li><strong>STEAM Day Trip (1 day):</strong> One day STEAM experience</li>
</ul>

<h3>Participants</h3>
<ul>
    <li>Children aged 6-15</li>
    <li>Student groups from schools</li>
    <li>Families wanting to experience with their children</li>
</ul>""",
            "images": [
                "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800",
                "https://images.unsplash.com/photo-1567057419565-4349c49d8a04?w=800",
                "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=800"
            ],
            "videos": [
                {"url": "https://www.youtube.com/embed/UYqnDxvdMPg", "title_vi": "Giới Thiệu STEAM", "title_en": "STEAM Introduction"},
                {"url": "https://www.youtube.com/embed/LXb3EKWsInQ", "title_vi": "STEAM Camp Tại Lumora", "title_en": "STEAM Camp at Lumora"}
            ]
        },
        {
            "slug": "workshop",
            "title_vi": "Workshop Kỹ Năng",
            "title_en": "Skills Workshop",
            "short_desc_vi": "Các workshop kỹ năng thực hành cho trẻ em và người lớn.",
            "short_desc_en": "Practical skill workshops for children and adults.",
            "content_vi": """<p>Workshop Kỹ Năng tại Lumora Resort mang đến những buổi học thực hành bổ ích.</p>

<h3>Các Workshop Đang Tổ Chức</h3>

<h4>1. Workshop Làm Robot</h4>
<p>Học cách lắp ráp và lập trình robot đơn giản.</p>
<p><strong>Thời lượng:</strong> 3 tiếng | <strong>Độ tuổi:</strong> 8-15 tuổi | <strong>Học phí:</strong> 350.000đ</p>

<h4>2. Workshop Thí Nghiệm Khoa Học</h4>
<p>Thực hiện các thí nghiệm khoa học thú vị với nguyên liệu an toàn.</p>
<p><strong>Thời lượng:</strong> 2 tiếng | <strong>Độ tuổi:</strong> 6-12 tuổi | <strong>Học phí:</strong> 250.000đ</p>

<h4>3. Workshop Nghệ Thuật Tái Chế</h4>
<p>Sáng tạo các sản phẩm nghệ thuật từ vật liệu tái chế.</p>
<p><strong>Thời lượng:</strong> 2.5 tiếng | <strong>Độ tuổi:</strong> Mọi lứa tuổi | <strong>Học phí:</strong> 200.000đ</p>

<h3>Lịch Workshop Hàng Tuần</h3>
<ul>
    <li><strong>Thứ 7:</strong> Workshop Làm Robot (9:00-12:00), Workshop Nghệ Thuật (14:00-16:30)</li>
    <li><strong>Chủ Nhật:</strong> Workshop Khoa Học (9:00-11:00), Workshop Làm Vườn (14:00-16:00)</li>
</ul>

<h3>Ưu Đãi Nhóm</h3>
<p>Giảm 10% cho nhóm từ 5 người, giảm 20% cho nhóm từ 10 người trở lên.</p>""",
            "content_en": """<p>Skills Workshops at Lumora Resort offer practical learning sessions.</p>

<h3>Current Workshops</h3>

<h4>1. Robot Building Workshop</h4>
<p>Learn to assemble and program simple robots.</p>
<p><strong>Duration:</strong> 3 hours | <strong>Age:</strong> 8-15 years | <strong>Fee:</strong> 350,000 VND</p>

<h4>2. Science Experiment Workshop</h4>
<p>Conduct fun science experiments with safe materials.</p>
<p><strong>Duration:</strong> 2 hours | <strong>Age:</strong> 6-12 years | <strong>Fee:</strong> 250,000 VND</p>

<h4>3. Recycled Art Workshop</h4>
<p>Create art products from recycled materials.</p>
<p><strong>Duration:</strong> 2.5 hours | <strong>Age:</strong> All ages | <strong>Fee:</strong> 200,000 VND</p>

<h3>Weekly Workshop Schedule</h3>
<ul>
    <li><strong>Saturday:</strong> Robot Workshop (9:00-12:00), Art Workshop (14:00-16:30)</li>
    <li><strong>Sunday:</strong> Science Workshop (9:00-11:00), Gardening Workshop (14:00-16:00)</li>
</ul>

<h3>Group Discounts</h3>
<p>10% off for groups of 5+, 20% off for groups of 10+.</p>""",
            "images": [
                "https://images.unsplash.com/photo-1544928147-79a2dbc1f389?w=800",
                "https://images.unsplash.com/photo-1530653333484-d65f75e24f57?w=800",
                "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800"
            ],
            "videos": [
                {"url": "https://www.youtube.com/embed/UYqnDxvdMPg", "title_vi": "Workshop Làm Robot", "title_en": "Robot Workshop"},
                {"url": "https://www.youtube.com/embed/5qap5aO4i9A", "title_vi": "Workshop Kỹ Năng Sinh Tồn", "title_en": "Survival Skills Workshop"}
            ]
        },
        {
            "slug": "register",
            "title_vi": "Đăng Ký Tham Gia STEAM",
            "title_en": "Register for STEAM",
            "short_desc_vi": "Đăng ký tham gia các chương trình STEAM tại Lumora Resort.",
            "short_desc_en": "Register for STEAM programs at Lumora Resort.",
            "content_vi": "<p>Vui lòng điền form đăng ký để tham gia các chương trình STEAM.</p>",
            "content_en": "<p>Please fill out the registration form to join STEAM programs.</p>",
            "images": [],
            "videos": []
        }
    ]
    
    for steam_item in steam_data:
        existing = SteamProgram.query.filter_by(slug=steam_item['slug']).first()
        if existing:
            continue
            
        images = steam_item.pop('images')
        videos = steam_item.pop('videos')
        program = SteamProgram(**steam_item)
        db.session.add(program)
        db.session.flush()
        
        for i, img_url in enumerate(images):
            img = SteamImage(steam_id=program.id, url=img_url, sort_order=i)
            db.session.add(img)
        
        for i, video in enumerate(videos):
            vid = SteamVideo(steam_id=program.id, sort_order=i, **video)
            db.session.add(vid)
    
    db.session.commit()
    print("Seeded STEAM programs")

def seed_events():
    events_data = [
        {
            "slug": "hall",
            "title_vi": "Hội Trường",
            "title_en": "Conference Hall",
            "description_vi": "Hội trường lớn sức chứa 500 người, trang bị đầy đủ âm thanh ánh sáng cho sự kiện.",
            "description_en": "Large conference hall with 500 capacity, fully equipped with sound and lighting.",
            "capacity": 500,
            "features": "Hệ thống âm thanh chuyên nghiệp\nMàn hình LED lớn\nĐiều hòa trung tâm\nWiFi tốc độ cao",
            "images": ["https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800"]
        },
        {
            "slug": "teambuilding",
            "title_vi": "Sân Team Building",
            "title_en": "Team Building Ground",
            "description_vi": "Sân rộng cho hoạt động team building, gala dinner và các sự kiện ngoài trời.",
            "description_en": "Large ground for team building activities, gala dinner and outdoor events.",
            "capacity": 1000,
            "features": "Sân cỏ rộng 2000m²\nSân khấu di động\nKhu vực lửa trại\nTrang thiết bị team building",
            "images": ["https://images.unsplash.com/photo-1511578314322-379afb476865?w=800"]
        }
    ]
    
    for event_data in events_data:
        existing = Event.query.filter_by(slug=event_data['slug']).first()
        if existing:
            continue
            
        images = event_data.pop('images')
        event = Event(**event_data)
        db.session.add(event)
        db.session.flush()
        
        for i, img_url in enumerate(images):
            img = EventImage(event_id=event.id, url=img_url, sort_order=i)
            db.session.add(img)
    
    db.session.commit()
    print("Seeded events")

def seed_news():
    news_data = [
        {
            "slug": "summer-2024-offer",
            "title_vi": "Ưu đãi mùa hè 2024 - Giảm 30%",
            "title_en": "Summer 2024 Offer - 30% Off",
            "excerpt_vi": "Đặt phòng ngay để nhận ưu đãi giảm 30% cho kỳ nghỉ mùa hè tại Lumora Resort.",
            "excerpt_en": "Book now to get 30% off for your summer vacation at Lumora Resort.",
            "content_vi": "Chương trình ưu đãi mùa hè 2024 với mức giảm lên đến 30% cho tất cả các loại phòng. Áp dụng từ 01/06 đến 31/08/2024.",
            "content_en": "Summer 2024 promotion with up to 30% discount on all room types. Valid from June 1 to August 31, 2024.",
            "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800",
            "category": "promotion",
            "status": "published",
            "published_at": datetime(2024, 5, 15)
        },
        {
            "slug": "bbq-garden-opening",
            "title_vi": "Khai trương nhà hàng BBQ Garden",
            "title_en": "BBQ Garden Grand Opening",
            "excerpt_vi": "Lumora Resort chính thức khai trương nhà hàng BBQ Garden với thực đơn đặc biệt.",
            "excerpt_en": "Lumora Resort officially opens BBQ Garden with special menu.",
            "content_vi": "Nhà hàng BBQ Garden mới khai trương với không gian ngoài trời thoáng mát và thực đơn BBQ đa dạng.",
            "content_en": "BBQ Garden newly opened with spacious outdoor area and diverse BBQ menu.",
            "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
            "category": "news",
            "status": "published",
            "published_at": datetime(2024, 4, 20)
        },
        {
            "slug": "steam-workshop-kids",
            "title_vi": "Workshop STEAM cho trẻ em",
            "title_en": "STEAM Workshop for Kids",
            "excerpt_vi": "Tham gia workshop STEAM cuối tuần dành cho các bé từ 6-12 tuổi.",
            "excerpt_en": "Join weekend STEAM workshop for kids aged 6-12.",
            "content_vi": "Workshop STEAM với các hoạt động thú vị như lắp ráp robot, thí nghiệm khoa học và nghệ thuật sáng tạo.",
            "content_en": "STEAM workshop with fun activities like robot assembly, science experiments and creative arts.",
            "image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800",
            "category": "event",
            "status": "published",
            "published_at": datetime(2024, 4, 10)
        }
    ]
    
    for news_item in news_data:
        existing = News.query.filter_by(slug=news_item['slug']).first()
        if existing:
            continue
            
        news = News(**news_item)
        db.session.add(news)
    
    db.session.commit()
    print("Seeded news")

def seed_gallery():
    gallery_data = [
        {"type": "image", "title_vi": "Toàn cảnh Resort", "title_en": "Resort Overview", "url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800", "category": "resort", "sort_order": 1},
        {"type": "image", "title_vi": "Bể bơi", "title_en": "Swimming Pool", "url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800", "category": "resort", "sort_order": 2},
        {"type": "image", "title_vi": "Phòng nghỉ", "title_en": "Room", "url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800", "category": "room", "sort_order": 3},
        {"type": "image", "title_vi": "Nhà hàng", "title_en": "Restaurant", "url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800", "category": "dining", "sort_order": 4},
        {"type": "image", "title_vi": "Vườn cây", "title_en": "Garden", "url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800", "category": "resort", "sort_order": 5},
        {"type": "image", "title_vi": "Cảnh đẹp", "title_en": "Scenery", "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800", "category": "resort", "sort_order": 6},
        {"type": "video", "title_vi": "Giới thiệu Resort", "title_en": "Resort Introduction", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ", "category": "resort", "sort_order": 7},
        {"type": "video", "title_vi": "Tour ảo", "title_en": "Virtual Tour", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ", "category": "resort", "sort_order": 8}
    ]
    
    for item in gallery_data:
        existing = GalleryItem.query.filter_by(url=item['url'], type=item['type']).first()
        if existing:
            continue
            
        gallery_item = GalleryItem(**item)
        db.session.add(gallery_item)
    
    db.session.commit()
    print("Seeded gallery")

def seed_all():
    with app.app_context():
        db.create_all()
        seed_rooms()
        seed_restaurants()
        seed_amenities()
        seed_experiences()
        seed_steam()
        seed_events()
        seed_news()
        seed_gallery()
        print("All data seeded successfully!")

if __name__ == '__main__':
    seed_all()

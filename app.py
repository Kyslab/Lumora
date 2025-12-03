import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "lumora-resort-secret-key")

ROOMS_DATA = {
    "deluxe": {
        "id": "deluxe",
        "name": {"vi": "Phòng Tiêu Chuẩn / Deluxe", "en": "Standard / Deluxe Room"},
        "description": {
            "vi": "Phòng tiêu chuẩn với đầy đủ tiện nghi hiện đại, view đẹp ra khu vườn hoặc hồ bơi.",
            "en": "Standard room with modern amenities, beautiful garden or pool view."
        },
        "price": 1500000,
        "area": 35,
        "capacity": 2,
        "amenities": ["wifi", "ac", "tv", "minibar", "bathroom"],
        "images": [
            "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
            "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800"
        ],
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ"
    },
    "glamping": {
        "id": "glamping",
        "name": {"vi": "Glamping / Cabin / Homestay", "en": "Glamping / Cabin / Homestay"},
        "description": {
            "vi": "Trải nghiệm cắm trại sang trọng giữa thiên nhiên với đầy đủ tiện nghi.",
            "en": "Luxury camping experience in nature with full amenities."
        },
        "price": 2000000,
        "area": 40,
        "capacity": 4,
        "amenities": ["wifi", "ac", "outdoor", "bbq", "bathroom"],
        "images": [
            "https://images.unsplash.com/photo-1499696010180-025ef6e1a8f9?w=800",
            "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"
        ],
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ"
    },
    "bungalow": {
        "id": "bungalow",
        "name": {"vi": "Dorm / Bungalow", "en": "Dorm / Bungalow"},
        "description": {
            "vi": "Bungalow riêng biệt giữa khu vườn nhiệt đới, không gian yên tĩnh và riêng tư.",
            "en": "Private bungalow in tropical garden, peaceful and private space."
        },
        "price": 2500000,
        "area": 50,
        "capacity": 4,
        "amenities": ["wifi", "ac", "kitchen", "garden", "bathroom"],
        "images": [
            "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800",
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800"
        ],
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ"
    }
}

RESTAURANTS_DATA = {
    "restaurant1": {
        "id": "restaurant1",
        "name": {"vi": "Nhà Hàng Lumora", "en": "Lumora Restaurant"},
        "description": {
            "vi": "Nhà hàng chính phục vụ ẩm thực Việt Nam và quốc tế với không gian sang trọng.",
            "en": "Main restaurant serving Vietnamese and international cuisine in elegant setting."
        },
        "category": {"vi": "Nhà hàng", "en": "Restaurant"},
        "hours": "06:00 - 22:00",
        "images": [
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
            "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800"
        ],
        "menu": [
            {"name": {"vi": "Phở Bò", "en": "Beef Pho"}, "price": 85000},
            {"name": {"vi": "Bún Chả", "en": "Bun Cha"}, "price": 75000},
            {"name": {"vi": "Cơm Tấm", "en": "Broken Rice"}, "price": 70000}
        ]
    },
    "restaurant2": {
        "id": "restaurant2",
        "name": {"vi": "BBQ Garden", "en": "BBQ Garden"},
        "description": {
            "vi": "Khu BBQ ngoài trời với không gian xanh mát, thích hợp cho nhóm bạn và gia đình.",
            "en": "Outdoor BBQ area with green space, perfect for groups and families."
        },
        "category": {"vi": "BBQ", "en": "BBQ"},
        "hours": "17:00 - 23:00",
        "images": [
            "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
            "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=800"
        ],
        "menu": [
            {"name": {"vi": "Set BBQ Hải Sản", "en": "Seafood BBQ Set"}, "price": 450000},
            {"name": {"vi": "Set BBQ Bò Wagyu", "en": "Wagyu Beef BBQ Set"}, "price": 650000},
            {"name": {"vi": "Set BBQ Gia Đình", "en": "Family BBQ Set"}, "price": 850000}
        ]
    },
    "cafe": {
        "id": "cafe",
        "name": {"vi": "Café & Bar Lounge", "en": "Café & Bar Lounge"},
        "description": {
            "vi": "Quán café và bar với view đẹp, phục vụ đồ uống và cocktail đặc biệt.",
            "en": "Café and bar with beautiful view, serving drinks and special cocktails."
        },
        "category": {"vi": "Café / Bar", "en": "Café / Bar"},
        "hours": "07:00 - 24:00",
        "images": [
            "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800",
            "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800"
        ],
        "menu": [
            {"name": {"vi": "Cà Phê Sữa Đá", "en": "Vietnamese Iced Coffee"}, "price": 45000},
            {"name": {"vi": "Mojito", "en": "Mojito"}, "price": 120000},
            {"name": {"vi": "Smoothie Trái Cây", "en": "Fruit Smoothie"}, "price": 65000}
        ]
    }
}

AMENITIES_DATA = {
    "zoo": {
        "id": "zoo",
        "name": {"vi": "Vườn Thú Mini", "en": "Mini Zoo"},
        "description": {
            "vi": "Vườn thú mini với nhiều loài động vật dễ thương, thích hợp cho trẻ em khám phá.",
            "en": "Mini zoo with cute animals, perfect for children to explore."
        },
        "images": [
            "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?w=800"
        ],
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ"
    },
    "garden": {
        "id": "garden",
        "name": {"vi": "Vườn Cây Xanh", "en": "Green Garden"},
        "description": {
            "vi": "Khu vườn nhiệt đới với đa dạng cây xanh, không gian thư giãn lý tưởng.",
            "en": "Tropical garden with diverse plants, ideal relaxation space."
        },
        "images": [
            "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800"
        ],
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ"
    },
    "pool": {
        "id": "pool",
        "name": {"vi": "Bể Bơi Vô Cực", "en": "Infinity Pool"},
        "description": {
            "vi": "Bể bơi vô cực với tầm nhìn tuyệt đẹp, mở cửa từ 6h sáng đến 10h tối.",
            "en": "Infinity pool with stunning views, open from 6am to 10pm."
        },
        "images": [
            "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?w=800"
        ],
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ"
    }
}

EXPERIENCES_DATA = {
    "checkin": {
        "id": "checkin",
        "name": {"vi": "Tham Quan Check-in", "en": "Check-in Tour"},
        "short_desc": {
            "vi": "Khám phá những điểm check-in đẹp nhất tại Lumora Resort.",
            "en": "Discover the most beautiful check-in spots at Lumora Resort."
        },
        "content": {
            "vi": """
                <p>Lumora Resort tự hào sở hữu hàng chục điểm check-in tuyệt đẹp, mỗi góc nhỏ đều là một khung cảnh hoàn hảo cho những bức ảnh đáng nhớ của bạn.</p>
                
                <h3>Các Điểm Check-in Nổi Bật</h3>
                
                <h4>1. Cầu Gỗ Giữa Hồ Sen</h4>
                <p>Cây cầu gỗ uốn lượn giữa hồ sen rộng lớn, với những bông sen hồng nở rộ vào mùa hè. Đây là điểm check-in được yêu thích nhất với ánh sáng hoàng hôn tuyệt đẹp.</p>
                
                <h4>2. Vườn Hoa Bốn Mùa</h4>
                <p>Khu vườn với hàng nghìn loài hoa từ khắp nơi trên thế giới, thay đổi theo từng mùa. Mùa xuân với hoa anh đào, mùa hè với hướng dương, mùa thu với cúc vạn thọ.</p>
                
                <h4>3. Khu Rừng Tre Xanh</h4>
                <p>Con đường nhỏ xuyên qua rừng tre xanh mát, tạo nên không gian yên bình và những bức ảnh mang phong cách Nhật Bản độc đáo.</p>
                
                <h4>4. Bể Bơi Vô Cực</h4>
                <p>Bể bơi vô cực nhìn ra núi đồi xa xa, đặc biệt đẹp vào lúc bình minh và hoàng hôn với bầu trời đầy màu sắc.</p>
                
                <h4>5. Khu Nhà Sàn Truyền Thống</h4>
                <p>Những ngôi nhà sàn được thiết kế theo phong cách truyền thống Việt Nam, là nơi lý tưởng để chụp ảnh mang đậm bản sắc văn hóa.</p>
                
                <h3>Lịch Trình Tour Tham Quan</h3>
                <ul>
                    <li><strong>Tour Sáng (7:00 - 9:00):</strong> Bắt đầu từ khu vườn hoa, hồ sen, rừng tre</li>
                    <li><strong>Tour Chiều (15:00 - 17:00):</strong> Khu nhà sàn, bể bơi vô cực, đồi cỏ</li>
                    <li><strong>Tour Hoàng Hôn (17:00 - 19:00):</strong> Các điểm view hoàng hôn đẹp nhất</li>
                </ul>
                
                <h3>Dịch Vụ Chụp Ảnh Chuyên Nghiệp</h3>
                <p>Lumora Resort cung cấp dịch vụ nhiếp ảnh chuyên nghiệp với photographer có kinh nghiệm, giúp bạn lưu giữ những khoảnh khắc đẹp nhất. Liên hệ lễ tân để đặt lịch.</p>
            """,
            "en": """
                <p>Lumora Resort proudly features dozens of stunning check-in spots, where every corner is a perfect frame for your memorable photos.</p>
                
                <h3>Featured Check-in Spots</h3>
                
                <h4>1. Wooden Bridge Over Lotus Lake</h4>
                <p>A winding wooden bridge across the vast lotus lake, with pink lotus blooming in summer. This is the most beloved check-in spot with beautiful sunset lighting.</p>
                
                <h4>2. Four Seasons Flower Garden</h4>
                <p>A garden with thousands of flower species from around the world, changing with each season. Spring with cherry blossoms, summer with sunflowers, autumn with marigolds.</p>
                
                <h4>3. Green Bamboo Forest</h4>
                <p>A small path through the cool green bamboo forest, creating a peaceful atmosphere and unique Japanese-style photos.</p>
                
                <h4>4. Infinity Pool</h4>
                <p>The infinity pool overlooking distant hills, especially beautiful at sunrise and sunset with colorful skies.</p>
                
                <h4>5. Traditional Stilt Houses</h4>
                <p>Stilt houses designed in traditional Vietnamese style, an ideal place to take photos with rich cultural heritage.</p>
                
                <h3>Tour Schedule</h3>
                <ul>
                    <li><strong>Morning Tour (7:00 - 9:00):</strong> Starting from flower garden, lotus lake, bamboo forest</li>
                    <li><strong>Afternoon Tour (15:00 - 17:00):</strong> Stilt houses, infinity pool, grass hills</li>
                    <li><strong>Sunset Tour (17:00 - 19:00):</strong> Best sunset viewing spots</li>
                </ul>
                
                <h3>Professional Photography Service</h3>
                <p>Lumora Resort provides professional photography services with experienced photographers to help you capture the most beautiful moments. Contact reception to book.</p>
            """
        },
        "images": [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=800",
            "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800",
            "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800"
        ],
        "videos": [
            {"url": "https://www.youtube.com/embed/LXb3EKWsInQ", "title": {"vi": "Tour Tham Quan Resort", "en": "Resort Tour"}},
            {"url": "https://www.youtube.com/embed/5qap5aO4i9A", "title": {"vi": "Điểm Check-in Đẹp Nhất", "en": "Best Check-in Spots"}}
        ]
    },
    "adventure": {
        "id": "adventure",
        "name": {"vi": "Khu Trò Chơi Mạo Hiểm", "en": "Adventure Playground"},
        "short_desc": {
            "vi": "Thử thách bản thân với các hoạt động mạo hiểm đầy thú vị.",
            "en": "Challenge yourself with exciting adventure activities."
        },
        "content": {
            "vi": """
                <p>Khu Trò Chơi Mạo Hiểm tại Lumora Resort là điểm đến lý tưởng cho những ai yêu thích cảm giác mạnh và muốn thử thách bản thân giữa thiên nhiên hùng vĩ.</p>
                
                <h3>Các Hoạt Động Mạo Hiểm</h3>
                
                <h4>1. Zipline Xuyên Rừng</h4>
                <p>Bay lượn trên dây zipline dài 500m xuyên qua tán rừng xanh mát, với độ cao 50m so với mặt đất. Cảm giác phấn khích và tầm nhìn panorama tuyệt đẹp.</p>
                <p><strong>Độ tuổi:</strong> Từ 10 tuổi | <strong>Thời gian:</strong> 15-20 phút</p>
                
                <h4>2. Leo Vách Đá</h4>
                <p>Khu vực leo núi nhân tạo với 5 cấp độ từ dễ đến khó, phù hợp cho cả người mới bắt đầu và người có kinh nghiệm. Huấn luyện viên chuyên nghiệp hướng dẫn từng bước.</p>
                <p><strong>Độ tuổi:</strong> Từ 8 tuổi | <strong>Thời gian:</strong> 30-45 phút</p>
                
                <h4>3. Cầu Treo Vượt Thác</h4>
                <p>Đi qua cầu treo bằng gỗ dài 100m bắc qua thác nước, cảm nhận hơi nước mát lạnh và âm thanh của thiên nhiên hoang dã.</p>
                <p><strong>Độ tuổi:</strong> Từ 6 tuổi | <strong>Thời gian:</strong> 10-15 phút</p>
                
                <h4>4. Đường Trượt Lăn</h4>
                <p>Trượt xuống đồi cỏ xanh trong những quả bóng lớn trong suốt - trải nghiệm vui nhộn và an toàn cho cả gia đình.</p>
                <p><strong>Độ tuổi:</strong> Từ 5 tuổi | <strong>Thời gian:</strong> 5-10 phút/lượt</p>
                
                <h4>5. Mê Cung Xanh</h4>
                <p>Mê cung được tạo từ hàng rào cây xanh cao 2m, thử thách khả năng định hướng và làm việc nhóm của bạn.</p>
                <p><strong>Độ tuổi:</strong> Mọi lứa tuổi | <strong>Thời gian:</strong> 20-40 phút</p>
                
                <h3>Gói Trải Nghiệm</h3>
                <ul>
                    <li><strong>Gói Cơ Bản:</strong> 2 hoạt động tự chọn - 300.000đ/người</li>
                    <li><strong>Gói Tiêu Chuẩn:</strong> 4 hoạt động - 500.000đ/người</li>
                    <li><strong>Gói VIP:</strong> Tất cả hoạt động + ảnh kỷ niệm - 800.000đ/người</li>
                </ul>
                
                <h3>Lưu Ý An Toàn</h3>
                <p>Tất cả các hoạt động đều được trang bị đầy đủ thiết bị bảo hộ và có huấn luyện viên chuyên nghiệp hướng dẫn. Vui lòng tuân thủ các quy định an toàn và hướng dẫn của nhân viên.</p>
            """,
            "en": """
                <p>The Adventure Playground at Lumora Resort is the ideal destination for thrill-seekers who want to challenge themselves amid magnificent nature.</p>
                
                <h3>Adventure Activities</h3>
                
                <h4>1. Forest Zipline</h4>
                <p>Soar on a 500m zipline through the cool green canopy, 50m above ground. Experience the thrill and stunning panoramic views.</p>
                <p><strong>Age:</strong> From 10 years | <strong>Duration:</strong> 15-20 minutes</p>
                
                <h4>2. Rock Climbing</h4>
                <p>Artificial climbing area with 5 difficulty levels from easy to hard, suitable for beginners and experienced climbers. Professional instructors guide every step.</p>
                <p><strong>Age:</strong> From 8 years | <strong>Duration:</strong> 30-45 minutes</p>
                
                <h4>3. Waterfall Suspension Bridge</h4>
                <p>Cross a 100m wooden suspension bridge over a waterfall, feeling the cool mist and sounds of wild nature.</p>
                <p><strong>Age:</strong> From 6 years | <strong>Duration:</strong> 10-15 minutes</p>
                
                <h4>4. Zorbing</h4>
                <p>Roll down green grass hills in large transparent balls - a fun and safe experience for the whole family.</p>
                <p><strong>Age:</strong> From 5 years | <strong>Duration:</strong> 5-10 minutes/round</p>
                
                <h4>5. Green Maze</h4>
                <p>A maze created from 2m tall green hedges, challenging your navigation and teamwork skills.</p>
                <p><strong>Age:</strong> All ages | <strong>Duration:</strong> 20-40 minutes</p>
                
                <h3>Experience Packages</h3>
                <ul>
                    <li><strong>Basic Package:</strong> 2 activities of choice - 300,000 VND/person</li>
                    <li><strong>Standard Package:</strong> 4 activities - 500,000 VND/person</li>
                    <li><strong>VIP Package:</strong> All activities + souvenir photos - 800,000 VND/person</li>
                </ul>
                
                <h3>Safety Notes</h3>
                <p>All activities are fully equipped with safety gear and guided by professional instructors. Please follow safety regulations and staff instructions.</p>
            """
        },
        "images": [
            "https://images.unsplash.com/photo-1551632811-561732d1e306?w=800",
            "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800",
            "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=800",
            "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=800"
        ],
        "videos": [
            {"url": "https://www.youtube.com/embed/LXb3EKWsInQ", "title": {"vi": "Khu Trò Chơi Mạo Hiểm", "en": "Adventure Playground"}},
            {"url": "https://www.youtube.com/embed/5qap5aO4i9A", "title": {"vi": "Zipline Xuyên Rừng", "en": "Forest Zipline"}}
        ]
    }
}

STEAM_DATA = {
    "intro": {
        "id": "intro",
        "name": {"vi": "Giới Thiệu Chương Trình STEAM", "en": "STEAM Program Introduction"},
        "short_desc": {
            "vi": "Khám phá chương trình giáo dục STEAM độc đáo tại Lumora Resort.",
            "en": "Discover the unique STEAM education program at Lumora Resort."
        },
        "content": {
            "vi": """
                <p>Chương trình Giáo dục STEAM tại Lumora Resort được thiết kế đặc biệt để mang đến cho trẻ em và thanh thiếu niên những trải nghiệm học tập thú vị, kết hợp giữa lý thuyết và thực hành trong môi trường thiên nhiên.</p>
                
                <h3>STEAM Là Gì?</h3>
                <p>STEAM là phương pháp giáo dục tích hợp 5 lĩnh vực:</p>
                <ul>
                    <li><strong>S - Science (Khoa học):</strong> Khám phá các hiện tượng tự nhiên, thí nghiệm khoa học</li>
                    <li><strong>T - Technology (Công nghệ):</strong> Ứng dụng công nghệ vào học tập và sáng tạo</li>
                    <li><strong>E - Engineering (Kỹ thuật):</strong> Thiết kế, xây dựng và giải quyết vấn đề</li>
                    <li><strong>A - Arts (Nghệ thuật):</strong> Phát triển tư duy sáng tạo và thẩm mỹ</li>
                    <li><strong>M - Mathematics (Toán học):</strong> Tư duy logic và giải quyết vấn đề</li>
                </ul>
                
                <h3>Tại Sao Chọn STEAM Tại Lumora?</h3>
                
                <h4>Học Tập Trong Thiên Nhiên</h4>
                <p>Khác với các lớp học truyền thống, chương trình STEAM tại Lumora được tổ chức trong môi trường thiên nhiên xanh mát, giúp trẻ em vừa học vừa chơi, kết nối với thiên nhiên.</p>
                
                <h4>Đội Ngũ Giảng Viên Chuyên Nghiệp</h4>
                <p>Chương trình được giảng dạy bởi các thầy cô có kinh nghiệm trong lĩnh vực giáo dục STEAM, với phương pháp giảng dạy sinh động và thu hút.</p>
                
                <h4>Trang Thiết Bị Hiện Đại</h4>
                <p>Lumora Resort đầu tư đầy đủ các thiết bị, dụng cụ thí nghiệm và công nghệ hiện đại phục vụ cho các hoạt động STEAM.</p>
                
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
                </ul>
            """,
            "en": """
                <p>The STEAM Education Program at Lumora Resort is specially designed to provide children and teenagers with exciting learning experiences, combining theory and practice in a natural environment.</p>
                
                <h3>What is STEAM?</h3>
                <p>STEAM is an integrated educational approach covering 5 areas:</p>
                <ul>
                    <li><strong>S - Science:</strong> Exploring natural phenomena, scientific experiments</li>
                    <li><strong>T - Technology:</strong> Applying technology to learning and creation</li>
                    <li><strong>E - Engineering:</strong> Design, building and problem-solving</li>
                    <li><strong>A - Arts:</strong> Developing creative and aesthetic thinking</li>
                    <li><strong>M - Mathematics:</strong> Logical thinking and problem-solving</li>
                </ul>
                
                <h3>Why Choose STEAM at Lumora?</h3>
                
                <h4>Learning in Nature</h4>
                <p>Unlike traditional classrooms, STEAM program at Lumora is organized in a green natural environment, helping children learn while playing and connecting with nature.</p>
                
                <h4>Professional Teaching Staff</h4>
                <p>The program is taught by experienced teachers in STEAM education, with engaging and attractive teaching methods.</p>
                
                <h4>Modern Equipment</h4>
                <p>Lumora Resort has invested in full equipment, laboratory tools and modern technology for STEAM activities.</p>
                
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
                </ul>
            """
        },
        "images": [
            "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800",
            "https://images.unsplash.com/photo-1567057419565-4349c49d8a04?w=800",
            "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=800"
        ],
        "videos": [
            {"url": "https://www.youtube.com/embed/UYqnDxvdMPg", "title": {"vi": "Giới Thiệu STEAM", "en": "STEAM Introduction"}},
            {"url": "https://www.youtube.com/embed/LXb3EKWsInQ", "title": {"vi": "STEAM Camp Tại Lumora", "en": "STEAM Camp at Lumora"}}
        ]
    },
    "workshop": {
        "id": "workshop",
        "name": {"vi": "Workshop Kỹ Năng", "en": "Skills Workshop"},
        "short_desc": {
            "vi": "Các workshop kỹ năng thực hành cho trẻ em và người lớn.",
            "en": "Practical skill workshops for children and adults."
        },
        "content": {
            "vi": """
                <p>Workshop Kỹ Năng tại Lumora Resort mang đến những buổi học thực hành bổ ích, giúp người tham gia phát triển các kỹ năng sống và sáng tạo trong môi trường vui vẻ, thoải mái.</p>
                
                <h3>Các Workshop Đang Tổ Chức</h3>
                
                <h4>1. Workshop Làm Robot</h4>
                <p>Học cách lắp ráp và lập trình robot đơn giản, phát triển tư duy logic và kỹ năng giải quyết vấn đề.</p>
                <p><strong>Thời lượng:</strong> 3 tiếng | <strong>Độ tuổi:</strong> 8-15 tuổi | <strong>Học phí:</strong> 350.000đ/học viên</p>
                
                <h4>2. Workshop Thí Nghiệm Khoa Học</h4>
                <p>Thực hiện các thí nghiệm khoa học thú vị với nguyên liệu an toàn, khám phá các hiện tượng tự nhiên.</p>
                <p><strong>Thời lượng:</strong> 2 tiếng | <strong>Độ tuổi:</strong> 6-12 tuổi | <strong>Học phí:</strong> 250.000đ/học viên</p>
                
                <h4>3. Workshop Nghệ Thuật Tái Chế</h4>
                <p>Sáng tạo các sản phẩm nghệ thuật từ vật liệu tái chế, nâng cao ý thức bảo vệ môi trường.</p>
                <p><strong>Thời lượng:</strong> 2.5 tiếng | <strong>Độ tuổi:</strong> Mọi lứa tuổi | <strong>Học phí:</strong> 200.000đ/học viên</p>
                
                <h4>4. Workshop Làm Vườn</h4>
                <p>Học cách trồng và chăm sóc cây, hiểu về hệ sinh thái và tầm quan trọng của cây xanh.</p>
                <p><strong>Thời lượng:</strong> 2 tiếng | <strong>Độ tuổi:</strong> 5-12 tuổi | <strong>Học phí:</strong> 180.000đ/học viên</p>
                
                <h4>5. Workshop Kỹ Năng Sinh Tồn</h4>
                <p>Học các kỹ năng sinh tồn cơ bản như nhóm lửa, tìm nguồn nước, xây dựng nơi trú ẩn.</p>
                <p><strong>Thời lượng:</strong> 4 tiếng | <strong>Độ tuổi:</strong> 10-18 tuổi | <strong>Học phí:</strong> 400.000đ/học viên</p>
                
                <h4>6. Workshop Nấu Ăn</h4>
                <p>Học nấu các món ăn đơn giản, an toàn dưới sự hướng dẫn của đầu bếp chuyên nghiệp.</p>
                <p><strong>Thời lượng:</strong> 2 tiếng | <strong>Độ tuổi:</strong> 7-15 tuổi | <strong>Học phí:</strong> 280.000đ/học viên</p>
                
                <h3>Lịch Workshop Hàng Tuần</h3>
                <ul>
                    <li><strong>Thứ 7:</strong> Workshop Làm Robot (9:00-12:00), Workshop Nghệ Thuật (14:00-16:30)</li>
                    <li><strong>Chủ Nhật:</strong> Workshop Khoa Học (9:00-11:00), Workshop Làm Vườn (14:00-16:00)</li>
                </ul>
                
                <h3>Ưu Đãi Nhóm</h3>
                <p>Giảm 10% cho nhóm từ 5 người, giảm 20% cho nhóm từ 10 người trở lên.</p>
            """,
            "en": """
                <p>Skills Workshops at Lumora Resort offer practical learning sessions, helping participants develop life skills and creativity in a fun, comfortable environment.</p>
                
                <h3>Current Workshops</h3>
                
                <h4>1. Robot Building Workshop</h4>
                <p>Learn to assemble and program simple robots, developing logical thinking and problem-solving skills.</p>
                <p><strong>Duration:</strong> 3 hours | <strong>Age:</strong> 8-15 years | <strong>Fee:</strong> 350,000 VND/student</p>
                
                <h4>2. Science Experiment Workshop</h4>
                <p>Conduct fun science experiments with safe materials, exploring natural phenomena.</p>
                <p><strong>Duration:</strong> 2 hours | <strong>Age:</strong> 6-12 years | <strong>Fee:</strong> 250,000 VND/student</p>
                
                <h4>3. Recycled Art Workshop</h4>
                <p>Create art products from recycled materials, raising environmental awareness.</p>
                <p><strong>Duration:</strong> 2.5 hours | <strong>Age:</strong> All ages | <strong>Fee:</strong> 200,000 VND/student</p>
                
                <h4>4. Gardening Workshop</h4>
                <p>Learn to plant and care for plants, understand ecosystems and the importance of greenery.</p>
                <p><strong>Duration:</strong> 2 hours | <strong>Age:</strong> 5-12 years | <strong>Fee:</strong> 180,000 VND/student</p>
                
                <h4>5. Survival Skills Workshop</h4>
                <p>Learn basic survival skills like fire-making, water sourcing, shelter building.</p>
                <p><strong>Duration:</strong> 4 hours | <strong>Age:</strong> 10-18 years | <strong>Fee:</strong> 400,000 VND/student</p>
                
                <h4>6. Cooking Workshop</h4>
                <p>Learn to cook simple dishes safely under the guidance of professional chefs.</p>
                <p><strong>Duration:</strong> 2 hours | <strong>Age:</strong> 7-15 years | <strong>Fee:</strong> 280,000 VND/student</p>
                
                <h3>Weekly Workshop Schedule</h3>
                <ul>
                    <li><strong>Saturday:</strong> Robot Workshop (9:00-12:00), Art Workshop (14:00-16:30)</li>
                    <li><strong>Sunday:</strong> Science Workshop (9:00-11:00), Gardening Workshop (14:00-16:00)</li>
                </ul>
                
                <h3>Group Discounts</h3>
                <p>10% off for groups of 5+, 20% off for groups of 10+.</p>
            """
        },
        "images": [
            "https://images.unsplash.com/photo-1544928147-79a2dbc1f389?w=800",
            "https://images.unsplash.com/photo-1530653333484-d65f75e24f57?w=800",
            "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800"
        ],
        "videos": [
            {"url": "https://www.youtube.com/embed/UYqnDxvdMPg", "title": {"vi": "Workshop Làm Robot", "en": "Robot Workshop"}},
            {"url": "https://www.youtube.com/embed/5qap5aO4i9A", "title": {"vi": "Workshop Kỹ Năng Sinh Tồn", "en": "Survival Skills Workshop"}}
        ]
    },
    "register": {
        "id": "register",
        "name": {"vi": "Đăng Ký Tham Gia STEAM", "en": "Register for STEAM"},
        "short_desc": {
            "vi": "Đăng ký tham gia các chương trình STEAM tại Lumora Resort.",
            "en": "Register for STEAM programs at Lumora Resort."
        }
    }
}

EVENTS_DATA = {
    "hall": {
        "id": "hall",
        "name": {"vi": "Hội Trường", "en": "Conference Hall"},
        "description": {
            "vi": "Hội trường lớn sức chứa 500 người, trang bị đầy đủ âm thanh ánh sáng cho sự kiện.",
            "en": "Large conference hall with 500 capacity, fully equipped with sound and lighting."
        },
        "capacity": 500,
        "images": ["https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800"]
    },
    "teambuilding": {
        "id": "teambuilding",
        "name": {"vi": "Sân Team Building", "en": "Team Building Ground"},
        "description": {
            "vi": "Sân rộng cho hoạt động team building, gala dinner và các sự kiện ngoài trời.",
            "en": "Large ground for team building activities, gala dinner and outdoor events."
        },
        "capacity": 1000,
        "images": ["https://images.unsplash.com/photo-1511578314322-379afb476865?w=800"]
    }
}

NEWS_DATA = [
    {
        "id": 1,
        "title": {"vi": "Ưu đãi mùa hè 2024 - Giảm 30%", "en": "Summer 2024 Offer - 30% Off"},
        "excerpt": {
            "vi": "Đặt phòng ngay để nhận ưu đãi giảm 30% cho kỳ nghỉ mùa hè tại Lumora Resort.",
            "en": "Book now to get 30% off for your summer vacation at Lumora Resort."
        },
        "content": {
            "vi": "Chương trình ưu đãi mùa hè 2024 với mức giảm lên đến 30% cho tất cả các loại phòng. Áp dụng từ 01/06 đến 31/08/2024.",
            "en": "Summer 2024 promotion with up to 30% discount on all room types. Valid from June 1 to August 31, 2024."
        },
        "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800",
        "date": "2024-05-15",
        "category": {"vi": "Ưu đãi", "en": "Promotion"}
    },
    {
        "id": 2,
        "title": {"vi": "Khai trương nhà hàng BBQ Garden", "en": "BBQ Garden Grand Opening"},
        "excerpt": {
            "vi": "Lumora Resort chính thức khai trương nhà hàng BBQ Garden với thực đơn đặc biệt.",
            "en": "Lumora Resort officially opens BBQ Garden with special menu."
        },
        "content": {
            "vi": "Nhà hàng BBQ Garden mới khai trương với không gian ngoài trời thoáng mát và thực đơn BBQ đa dạng.",
            "en": "BBQ Garden newly opened with spacious outdoor area and diverse BBQ menu."
        },
        "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800",
        "date": "2024-04-20",
        "category": {"vi": "Tin tức", "en": "News"}
    },
    {
        "id": 3,
        "title": {"vi": "Workshop STEAM cho trẻ em", "en": "STEAM Workshop for Kids"},
        "excerpt": {
            "vi": "Tham gia workshop STEAM cuối tuần dành cho các bé từ 6-12 tuổi.",
            "en": "Join weekend STEAM workshop for kids aged 6-12."
        },
        "content": {
            "vi": "Workshop STEAM với các hoạt động thú vị như lắp ráp robot, thí nghiệm khoa học và nghệ thuật sáng tạo.",
            "en": "STEAM workshop with fun activities like robot assembly, science experiments and creative arts."
        },
        "image": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800",
        "date": "2024-04-10",
        "category": {"vi": "Sự kiện", "en": "Event"}
    }
]

GALLERY_DATA = {
    "images": [
        {"url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800", "title": {"vi": "Toàn cảnh Resort", "en": "Resort Overview"}},
        {"url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800", "title": {"vi": "Bể bơi", "en": "Swimming Pool"}},
        {"url": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800", "title": {"vi": "Phòng nghỉ", "en": "Room"}},
        {"url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800", "title": {"vi": "Nhà hàng", "en": "Restaurant"}},
        {"url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800", "title": {"vi": "Vườn cây", "en": "Garden"}},
        {"url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800", "title": {"vi": "Cảnh đẹp", "en": "Scenery"}}
    ],
    "videos": [
        {"url": "https://www.youtube.com/embed/dQw4w9WgXcQ", "title": {"vi": "Giới thiệu Resort", "en": "Resort Introduction"}},
        {"url": "https://www.youtube.com/embed/dQw4w9WgXcQ", "title": {"vi": "Tour ảo", "en": "Virtual Tour"}}
    ]
}

@app.route('/')
def home():
    lang = request.args.get('lang', 'vi')
    return render_template('home.html', 
                         lang=lang,
                         rooms=ROOMS_DATA,
                         amenities=AMENITIES_DATA,
                         news=NEWS_DATA[:3])

@app.route('/accommodation')
def accommodation():
    lang = request.args.get('lang', 'vi')
    room_type = request.args.get('type', None)
    return render_template('accommodation.html', 
                         lang=lang,
                         rooms=ROOMS_DATA,
                         selected_type=room_type)

@app.route('/accommodation/<room_id>')
def room_detail(room_id):
    lang = request.args.get('lang', 'vi')
    room = ROOMS_DATA.get(room_id)
    if not room:
        return render_template('404.html', lang=lang), 404
    return render_template('room_detail.html', lang=lang, room=room)

@app.route('/dining')
def dining():
    lang = request.args.get('lang', 'vi')
    return render_template('dining.html', lang=lang, restaurants=RESTAURANTS_DATA)

@app.route('/dining/<restaurant_id>')
def restaurant_detail(restaurant_id):
    lang = request.args.get('lang', 'vi')
    restaurant = RESTAURANTS_DATA.get(restaurant_id)
    if not restaurant:
        return render_template('404.html', lang=lang), 404
    return render_template('restaurant_detail.html', lang=lang, restaurant=restaurant)

@app.route('/amenities')
def amenities():
    lang = request.args.get('lang', 'vi')
    return render_template('amenities.html', lang=lang, amenities=AMENITIES_DATA)

@app.route('/experiences/checkin')
def experience_checkin():
    lang = request.args.get('lang', 'vi')
    experience = EXPERIENCES_DATA.get('checkin')
    return render_template('experience_detail.html', lang=lang, experience=experience)

@app.route('/experiences/adventure')
def experience_adventure():
    lang = request.args.get('lang', 'vi')
    experience = EXPERIENCES_DATA.get('adventure')
    return render_template('experience_detail.html', lang=lang, experience=experience)

@app.route('/steam/intro')
def steam_intro():
    lang = request.args.get('lang', 'vi')
    steam_item = STEAM_DATA.get('intro')
    return render_template('steam_detail.html', lang=lang, steam=steam_item)

@app.route('/steam/workshop')
def steam_workshop():
    lang = request.args.get('lang', 'vi')
    steam_item = STEAM_DATA.get('workshop')
    return render_template('steam_detail.html', lang=lang, steam=steam_item)

@app.route('/steam/register')
def steam_register():
    lang = request.args.get('lang', 'vi')
    return render_template('steam_register.html', lang=lang)

@app.route('/events')
def events():
    lang = request.args.get('lang', 'vi')
    return render_template('events.html', lang=lang, events=EVENTS_DATA)

@app.route('/news')
def news():
    lang = request.args.get('lang', 'vi')
    return render_template('news.html', lang=lang, news=NEWS_DATA)

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    lang = request.args.get('lang', 'vi')
    article = next((n for n in NEWS_DATA if n['id'] == news_id), None)
    if not article:
        return render_template('404.html', lang=lang), 404
    return render_template('news_detail.html', lang=lang, article=article)

@app.route('/gallery')
def gallery():
    lang = request.args.get('lang', 'vi')
    return render_template('gallery.html', lang=lang, gallery=GALLERY_DATA)

@app.route('/contact')
def contact():
    lang = request.args.get('lang', 'vi')
    return render_template('contact.html', lang=lang)

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    return jsonify({"success": True, "message": "Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất."})

@app.route('/api/booking', methods=['POST'])
def submit_booking():
    data = request.get_json()
    return jsonify({"success": True, "message": "Yêu cầu đặt phòng đã được gửi! Chúng tôi sẽ liên hệ xác nhận."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

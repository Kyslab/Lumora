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
        "description": {
            "vi": "Tour tham quan các điểm check-in đẹp nhất trong khu resort.",
            "en": "Tour of the most beautiful check-in spots in the resort."
        },
        "images": ["https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800"]
    },
    "adventure": {
        "id": "adventure",
        "name": {"vi": "Khu Trò Chơi Mạo Hiểm", "en": "Adventure Zone"},
        "description": {
            "vi": "Khu vực trò chơi mạo hiểm với nhiều hoạt động thú vị cho mọi lứa tuổi.",
            "en": "Adventure zone with exciting activities for all ages."
        },
        "images": ["https://images.unsplash.com/photo-1551632811-561732d1e306?w=800"]
    }
}

STEAM_DATA = {
    "program": {
        "id": "program",
        "name": {"vi": "Chương Trình STEAM", "en": "STEAM Program"},
        "description": {
            "vi": "Chương trình giáo dục STEAM với các hoạt động khoa học, công nghệ, kỹ thuật, nghệ thuật và toán học.",
            "en": "STEAM education program with science, technology, engineering, arts and mathematics activities."
        },
        "images": ["https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800"]
    },
    "workshop": {
        "id": "workshop",
        "name": {"vi": "Workshop Kỹ Năng", "en": "Skills Workshop"},
        "description": {
            "vi": "Các workshop kỹ năng sống, thủ công và sáng tạo cho trẻ em và người lớn.",
            "en": "Life skills, crafts and creativity workshops for children and adults."
        },
        "images": ["https://images.unsplash.com/photo-1544928147-79a2dbc1f389?w=800"]
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

@app.route('/experiences')
def experiences():
    lang = request.args.get('lang', 'vi')
    return render_template('experiences.html', lang=lang, experiences=EXPERIENCES_DATA)

@app.route('/steam')
def steam():
    lang = request.args.get('lang', 'vi')
    return render_template('steam.html', lang=lang, steam=STEAM_DATA)

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

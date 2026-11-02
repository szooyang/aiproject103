

# ==========================================
# 1. 기본 페이지 설정
# ==========================================
st.set_page_config(
    page_title="MBTI 책 & 영화 추천",
    page_icon="🎬",
    layout="wide"
)

# ==========================================
# 2. 디자인
# ==========================================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #6C63FF;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: 17px;
        color: #777777;
        margin-bottom: 25px;
    }
    .recommend-card {
        background-color: #F5F3FF;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 12px;
        border: 1px solid #E5DEFF;
    }
    .movie-card {
        background-color: #FFF4E8;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 12px;
        border: 1px solid #FFE0BD;
    }
    .card-title {
        font-size: 21px;
        font-weight: bold;
        color: #44358A;
    }
    .review {
        font-size: 15px;
        line-height: 1.7;
        color: #444444;
    }
    .section-title {
        font-size: 25px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. 한국 작가 소설 데이터
# ==========================================
books = {
    "아몬드": {
        "author": "손원평",
        "description": "감정을 잘 느끼지 못하는 소년 윤재가 다양한 사람들을 만나며 성장하는 이야기.",
        "review": "감정이란 무엇인지 생각하게 만드는 책이야. 따뜻하면서도 여운이 오래 남아서 꼭 읽어봤으면 좋겠어!"
    },
    "완득이": {
        "author": "김려령",
        "description": "평범하지 않은 환경에서 살아가는 고등학생 완득이의 성장 이야기.",
        "review": "유쾌하고 재미있어서 술술 읽혀! 웃음도 있고 감동도 있어서 부담 없이 읽기 좋아."
    },
    "불편한 편의점": {
        "author": "김호연",
        "description": "서울의 한 편의점을 배경으로 다양한 사람들의 일상과 관계를 그린 이야기.",
        "review": "읽다 보면 마음이 편안해지는 책이야. 소소한 일상 속 따뜻한 위로를 받고 싶다면 추천!"
    },
    "달러구트 꿈 백화점": {
        "author": "이미예",
        "description": "잠든 사람들이 꿈을 구매하는 신비로운 백화점을 배경으로 펼쳐지는 판타지 소설.",
        "review": "상상력이 정말 기발한 책이야! 현실에서 잠시 벗어나 특별한 세계를 여행하고 싶을 때 딱이야."
    },
    "지구 끝의 온실": {
        "author": "김초엽",
        "description": "멸망한 세계 이후 식물과 인간이 함께 살아가는 미래를 그린 SF 소설.",
        "review": "신비로운 미래 세계와 인간의 희망을 동시에 느낄 수 있어. 상상하는 걸 좋아한다면 강력 추천!"
    },
    "우리가 빛의 속도로 갈 수 없다면": {
        "author": "김초엽",
        "description": "과학기술과 인간의 삶을 연결한 다양한 이야기를 담은 SF 소설집.",
        "review": "짧은 이야기마다 생각할 거리가 가득해. 과학과 상상력, 인간적인 감동을 모두 느낄 수 있어!"
    },
    "천 개의 파랑": {
        "author": "천선란",
        "description": "로봇과 인간, 경주마의 관계를 통해 생명과 공존의 의미를 이야기하는 소설.",
        "review": "읽고 나면 세상을 바라보는 시선이 조금 달라질 거야. 따뜻한 감동을 원하는 친구에게 추천!"
    },
    "모순": {
        "author": "양귀자",
        "description": "서로 다른 삶을 살아가는 인물들을 통해 인생의 선택과 모순을 생각하게 하는 소설.",
        "review": "인생에 정답이 있는지 고민하게 만드는 책이야. 읽고 나서 친구와 이야기 나누기도 좋아!"
    },
    "두근두근 내 인생": {
        "author": "김애란",
        "description": "남들보다 빠르게 나이 들어가는 소년과 가족의 사랑을 그린 이야기.",
        "review": "웃다가 울다가 어느새 마음이 따뜻해지는 책이야. 가족과 사랑의 의미를 다시 생각하게 해!"
    },
    "바깥은 여름": {
        "author": "김애란",
        "description": "상실과 이별, 일상의 순간들을 섬세하게 그려낸 소설집.",
        "review": "잔잔하지만 깊은 울림이 있는 책이야. 사람의 마음을 이해하고 싶을 때 읽어봐!"
    },
    "파과": {
        "author": "구병모",
        "description": "오랜 세월 활동한 여성 킬러의 삶과 관계, 변화를 그린 소설.",
        "review": "독특한 설정과 강렬한 이야기가 매력적이야. 평범한 이야기가 지루하다면 추천!"
    },
    "위저드 베이커리": {
        "author": "구병모",
        "description": "신비로운 빵집을 배경으로 선택과 책임에 관한 이야기를 펼치는 판타지 소설.",
        "review": "마법 같은 분위기와 긴장감이 정말 매력적이야. 색다른 이야기를 좋아한다면 읽어봐!"
    },
    "7년의 밤": {
        "author": "정유정",
        "description": "한 사건을 둘러싼 인물들의 비밀과 갈등을 긴장감 있게 풀어낸 장편소설.",
        "review": "한 번 읽기 시작하면 다음 내용이 궁금해서 멈추기 어려워! 몰입감 있는 소설을 찾는다면 추천."
    },
    "종의 기원": {
        "author": "정유정",
        "description": "한 인물의 내면과 사건을 통해 인간의 본성과 심리를 탐구하는 소설.",
        "review": "심리 묘사가 정말 강렬한 작품이야. 긴장감 넘치는 이야기를 좋아하는 친구에게 추천!"
    },
    "소년이 온다": {
        "author": "한강",
        "description": "5·18 민주화운동을 배경으로 여러 인물의 시선에서 아픔과 기억을 그린 소설.",
        "review": "무겁지만 꼭 한 번 읽어볼 만한 작품이야. 역사와 인간의 존엄에 대해 깊이 생각하게 해."
    },
    "채식주의자": {
        "author": "한강",
        "description": "한 여성의 선택을 둘러싸고 벌어지는 가족과 사회의 갈등을 그린 소설.",
        "review": "익숙한 생각을 흔들어 놓는 독특한 작품이야. 다양한 관점에서 세상을 바라보고 싶다면 추천!"
    }
}


# ==========================================
# 4. MBTI별 책 추천
# ==========================================
mbti_books = {
    "ISTJ": ["모순", "7년의 밤"],
    "ISFJ": ["불편한 편의점", "두근두근 내 인생"],
    "INFJ": ["소년이 온다", "천 개의 파랑"],
    "INTJ": ["종의 기원", "지구 끝의 온실"],
    "ISTP": ["파과", "위저드 베이커리"],
    "ISFP": ["아몬드", "바깥은 여름"],
    "INFP": ["달러구트 꿈 백화점", "우리가 빛의 속도로 갈 수 없다면"],
    "INTP": ["지구 끝의 온실", "채식주의자"],
    "ESTP": ["완득이", "파과"],
    "ESFP": ["달러구트 꿈 백화점", "완득이"],
    "ENFP": ["천 개의 파랑", "위저드 베이커리"],
    "ENTP": ["채식주의자", "종의 기원"],
    "ESTJ": ["모순", "7년의 밤"],
    "ESFJ": ["불편한 편의점", "아몬드"],
    "ENFJ": ["두근두근 내 인생", "소년이 온다"],
    "ENTJ": ["지구 끝의 온실", "파과"]
}


# ==========================================
# 5. 현재 국내 상영 영화 데이터
# ==========================================
# 2026년 11월 2일 기준
# 상영 여부와 시간표는 영화관별로 다를 수 있음.

movies = {
    "하트 오브 비스트": {
        "genre": "모험 · 액션 · 드라마",
        "rating": "12세 이상 관람가",
        "description": "알래스카 오지에 고립된 전직 특수부대원과 은퇴한 군견이 생존을 위해 사투를 벌이는 이야기.",
        "review": "긴장감 넘치는 생존 모험을 좋아한다면 이 영화! 사람과 반려견의 특별한 유대감도 기대해 봐."
    },
    "극장판 치이카와: 인어 섬의 비밀": {
        "genre": "애니메이션 · 모험",
        "rating": "전체 관람가",
        "description": "치이카와와 친구들이 특별한 섬에 초대받아 그곳에 숨겨진 비밀을 마주하는 이야기.",
        "review": "귀여운 캐릭터와 신나는 모험을 즐기고 싶다면 추천! 친구나 가족과 함께 보기에도 좋아."
    },
    "암살자(들)": {
        "genre": "범죄 · 드라마",
        "rating": "12세 이상 관람가",
        "description": "사건과 인물들의 관계를 중심으로 펼쳐지는 범죄 드라마.",
        "review": "사건의 흐름을 따라가며 몰입하고 싶은 친구에게 추천! 영화가 끝난 뒤에도 이야기를 곱씹게 될 거야."
    },
    "실낙원": {
        "genre": "스릴러 · 드라마",
        "rating": "15세 이상 관람가",
        "description": "인물들의 갈등과 사건을 긴장감 있게 그려낸 스릴러 드라마.",
        "review": "평범한 이야기보다 긴장감과 몰입감을 원한다면 도전해 봐! 스릴러를 좋아하는 친구에게 추천."
    }
}


# ==========================================
# 6. MBTI별 영화 추천
# ==========================================
mbti_movies = {
    "ISTJ": ["암살자(들)", "하트 오브 비스트"],
    "ISFJ": ["극장판 치이카와: 인어 섬의 비밀", "하트 오브 비스트"],
    "INFJ": ["실낙원", "하트 오브 비스트"],
    "INTJ": ["실낙원", "암살자(들)"],
    "ISTP": ["하트 오브 비스트", "암살자(들)"],
    "ISFP": ["극장판 치이카와: 인어 섬의 비밀", "하트 오브 비스트"],
    "INFP": ["극장판 치이카와: 인어 섬의 비밀", "실낙원"],
    "INTP": ["암살자(들)", "실낙원"],
    "ESTP": ["하트 오브 비스트", "암살자(들)"],
    "ESFP": ["극장판 치이카와: 인어 섬의 비밀", "하트 오브 비스트"],
    "ENFP": ["극장판 치이카와: 인어 섬의 비밀", "하트 오브 비스트"],
    "ENTP": ["암살자(들)", "실낙원"],
    "ESTJ": ["하트 오브 비스트", "암살자(들)"],
    "ESFJ": ["극장판 치이카와: 인어 섬의 비밀", "하트 오브 비스트"],
    "ENFJ": ["하트 오브 비스트", "극장판 치이카와: 인어 섬의 비밀"],
    "ENTJ": ["실낙원", "암살자(들)"]
}


# ==========================================
# 7. MBTI 선택 화면
# ==========================================
st.markdown(
    '<div class="main-title">📚 나의 MBTI 취향 저격!</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">책도 영화도 내 취향대로! 오늘의 추천을 확인해 봐 🎬</div>',
    unsafe_allow_html=True
)

st.divider()

st.markdown("### 🧩 너의 MBTI는 무엇이야?")

mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

selected_mbti = st.selectbox(
    "MBTI 유형을 선택해 줘!",
    mbti_list,
    index=None,
    placeholder="나의 MBTI를 선택하세요."
)

# ==========================================
# 8. 추천 결과 화면
# ==========================================
if selected_mbti:

    st.balloons()

    st.markdown("---")

    st.markdown(
        f"<h2 style='text-align:center; color:#6C63FF;'>✨ {selected_mbti}를 위한 추천 도착!</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>너의 성향을 생각해서 책과 영화를 골라봤어. 마음에 드는 게 있는지 확인해 봐! 😎</p>",
        unsafe_allow_html=True
    )

    # --------------------------------------
    # 책 추천
    # --------------------------------------
    st.markdown(
        '<div class="section-title">📚 너에게 추천하는 책 2권</div>',
        unsafe_allow_html=True
    )

    book_col1, book_col2 = st.columns(2)

    recommended_books = mbti_books[selected_mbti]

    for i, book_name in enumerate(recommended_books):

        book = books[book_name]

        with [book_col1, book_col2][i]:

            st.markdown(
                f"""
                <div class="recommend-card">
                    <div class="card-title">📖 {book_name}</div>
                    <p><b>✍️ 작가:</b> {book['author']}</p>
                    <p><b>📌 줄거리:</b> {book['description']}</p>
                    <hr>
                    <p class="review">💬 <b>친구의 추천 평</b><br>
                    {book['review']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------
    # 영화 추천
    # --------------------------------------
    st.markdown(
        '<div class="section-title">🎬 지금 극장에서 볼 만한 영화 2편</div>',
        unsafe_allow_html=True
    )

    movie_col1, movie_col2 = st.columns(2)

    recommended_movies = mbti_movies[selected_mbti]

    for i, movie_name in enumerate(recommended_movies):

        movie = movies[movie_name]

        with [movie_col1, movie_col2][i]:

            st.markdown(
                f"""
                <div class="movie-card">
                    <div class="card-title">🎥 {movie_name}</div>
                    <p><b>🎭 장르:</b> {movie['genre']}</p>
                    <p><b>🔞 관람 등급:</b> {movie['rating']}</p>
                    <p><b>📌 줄거리:</b> {movie['description']}</p>
                    <hr>
                    <p class="review">💬 <b>친구의 추천 평</b><br>
                    {movie['review']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------
    # 마무리 메시지
    # --------------------------------------
    st.markdown("---")

    st.markdown(
        f"""
        <div style="text-align:center; padding:20px;">
            <h3>💜 오늘의 추천이 마음에 들었어?</h3>
            <p>MBTI는 취향을 알아보는 재미있는 참고 자료일 뿐이야!</p>
            <p>네가 직접 끌리는 책과 영화를 선택하는 게 가장 중요해 😊</p>
            <p><b>{selected_mbti}의 즐거운 독서와 영화 감상을 응원할게!</b> 🍀</p>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.info("👆 위에서 MBTI를 선택하면 너만의 책과 영화 추천이 시작돼!")

    st.markdown("""
    <div style="text-align:center; padding:30px;">
        <h1>📚 + 🎬 = 💜</h1>
        <h3>책 한 권, 영화 한 편으로 특별한 하루를 만들어 보자!</h3>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 9. 하단 안내
# ==========================================
st.divider()

st.caption(
    "📌 책과 영화 추천은 MBTI 유형을 활용한 재미있는 콘텐츠입니다. "
    "영화 상영 여부 및 관람 등급은 영화관과 지역에 따라 확인해 주세요."
)

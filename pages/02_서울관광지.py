
import streamlit as st
import folium
from streamlit_folium import st_folium
from html import escape

# ==========================================
# 1. 관광지 데이터
# ==========================================

PLACES = [
    {
        "rank": 1,
        "name": "명동",
        "english": "Myeong-dong",
        "lat": 37.5636,
        "lon": 126.9850,
        "category": "쇼핑·먹거리",
        "description": "화장품과 패션 매장, 길거리 음식이 모여 있는 서울 대표 쇼핑 거리예요. 다양한 한국 간식과 K-뷰티 제품을 구경하기 좋아요.",
        "tip": "저녁 시간에는 길거리 음식과 야경을 함께 즐겨 보세요."
    },
    {
        "rank": 2,
        "name": "N서울타워",
        "english": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "category": "전망·야경",
        "description": "남산 정상에 있는 서울의 상징적인 전망 명소예요. 전망대에서 서울 도심을 한눈에 볼 수 있어요.",
        "tip": "해 질 무렵 방문하면 낮과 밤의 서울 풍경을 모두 볼 수 있어요."
    },
    {
        "rank": 3,
        "name": "코엑스·별마당도서관",
        "english": "COEX & Starfield Library",
        "lat": 37.5126,
        "lon": 127.0588,
        "category": "쇼핑·문화",
        "description": "대형 쇼핑 공간과 별마당도서관이 있는 복합문화공간이에요. 독특한 서가 앞에서 사진을 찍기 좋아요.",
        "tip": "실내에서 쇼핑과 식사, 사진 촬영을 한 번에 즐겨 보세요."
    },
    {
        "rank": 4,
        "name": "강남역 일대",
        "english": "Gangnam Station Area",
        "lat": 37.4979,
        "lon": 127.0276,
        "category": "쇼핑·도심",
        "description": "세련된 상점과 식당, 카페가 모여 있는 활기찬 도심 상권이에요. 현대적인 서울의 분위기를 느끼기 좋아요.",
        "tip": "지하상가와 주변 골목의 상점도 함께 둘러보세요."
    },
    {
        "rank": 5,
        "name": "홍대 거리",
        "english": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "category": "문화·공연",
        "description": "젊은 문화와 거리 공연, 개성 있는 상점으로 유명한 곳이에요. 음악과 패션, 다양한 먹거리를 경험할 수 있어요.",
        "tip": "주말 저녁에는 거리 공연과 활기찬 분위기를 즐겨 보세요."
    },
    {
        "rank": 6,
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "category": "역사·문화",
        "description": "조선 왕조의 대표 궁궐이에요. 웅장한 건축물과 아름다운 정원을 둘러보며 한국의 역사와 전통문화를 만날 수 있어요.",
        "tip": "한복을 입고 방문하면 특별한 추억과 사진을 남길 수 있어요."
    },
    {
        "rank": 7,
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "category": "전통·문화",
        "description": "전통 한옥이 모여 있는 골목 마을이에요. 옛 서울의 주거 모습과 현대적인 카페·공방이 어우러져 있어요.",
        "tip": "실제 주민이 거주하는 곳이므로 조용히 관람하고 안내 표지와 관람 시간을 확인하세요."
    },
    {
        "rank": 8,
        "name": "동대문디자인플라자(DDP)",
        "english": "Dongdaemun Design Plaza",
        "lat": 37.5671,
        "lon": 127.0095,
        "category": "건축·전시",
        "description": "독특한 곡선형 건축물로 유명한 디자인·전시 공간이에요. 전시와 행사, 야간 조명을 즐길 수 있어요.",
        "tip": "건물 외관과 주변 조명이 돋보이는 저녁 시간도 추천해요."
    },
    {
        "rank": 9,
        "name": "광장시장",
        "english": "Gwangjang Market",
        "lat": 37.5701,
        "lon": 126.9997,
        "category": "전통시장·먹거리",
        "description": "빈대떡과 김밥 등 한국의 시장 음식을 맛볼 수 있는 전통시장이에요. 활기찬 시장 풍경도 매력적이에요.",
        "tip": "여러 음식을 조금씩 나누어 맛보면 더 다양하게 즐길 수 있어요."
    },
    {
        "rank": 10,
        "name": "낙산공원",
        "english": "Naksan Park",
        "lat": 37.5803,
        "lon": 127.0074,
        "category": "산책·야경",
        "description": "서울 성곽길과 도심 풍경을 함께 감상할 수 있는 공원이에요. 산책과 야경 감상, 사진 촬영 장소로 좋아요.",
        "tip": "성곽길은 오르막과 계단이 있으니 편한 신발을 신으세요."
    }
]

# ==========================================
# 2. 앱 제목 및 소개
# ==========================================

st.title("🇰🇷 서울 외국인 인기 관광지 TOP 10")

st.markdown(
    """
    서울 여행에서 놓치기 아까운 명소 10곳을
    지도에서 찾아보세요!

    지도에 표시된 숫자를 누르면
    관광지 설명과 여행 팁을 확인할 수 있어요.
    """
)

st.info(
    "외국인 방문 분석과 서울의 대표 명소를 참고해 구성한 "
    "안내용 관광지 목록입니다. 공식 단일 순위의 1~10위는 아닙니다."
)

# ==========================================
# 3. 관광지 종류 선택
# ==========================================

categories = ["전체"] + sorted(
    set(place["category"] for place in PLACES)
)

selected_category = st.selectbox(
    "🔎 관광지 종류로 찾아보기",
    categories
)

visible_places = [
    place for place in PLACES
    if selected_category == "전체"
    or selected_category == place["category"]
]

# ==========================================
# 4. 서울 지도 생성
# OpenStreetMap 사용
# API Key 필요 없음
# ==========================================

seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True
)

# ==========================================
# 5. 지도에 관광지 표시
# ==========================================

for place in visible_places:

    popup_html = f"""
    <div style="
        width:230px;
        font-family:sans-serif;
        line-height:1.6;
    ">

        <h4 style="margin:0 0 6px 0;">
            {place['rank']}. {escape(place['name'])}
        </h4>

        <div style="color:#666; margin-bottom:8px;">
            {escape(place['english'])}
        </div>

        <div style="margin-bottom:8px;">
            {escape(place['description'])}
        </div>

        <b>💡 여행 팁</b><br>
        {escape(place['tip'])}

    </div>
    """

    # 빨간색 숫자 아이콘 생성
    number_icon = folium.DivIcon(
        html=f"""
        <div style="
            background:#e53935;
            color:white;
            border:2px solid white;
            border-radius:50%;
            width:30px;
            height:30px;
            line-height:26px;
            text-align:center;
            font-weight:bold;
            font-size:14px;
            box-shadow:0 1px 5px rgba(0,0,0,.45);
        ">
            {place['rank']}
        </div>
        """,
        icon_size=(30, 30),
        icon_anchor=(15, 15)
    )

    folium.Marker(
        location=[
            place["lat"],
            place["lon"]
        ],
        tooltip=f"{place['rank']}. {place['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=280
        ),
        icon=number_icon
    ).add_to(seoul_map)

# ==========================================
# 6. 지도 범위 자동 조정
# ==========================================

if visible_places:

    bounds = [
        [place["lat"], place["lon"]]
        for place in visible_places
    ]

    seoul_map.fit_bounds(
        bounds,
        padding=(30, 30)
    )

# ==========================================
# 7. 지도 표시
# ==========================================

st.subheader("📍 서울 관광지 지도")

st.caption(
    "빨간색 숫자를 클릭하면 관광지의 상세 설명을 볼 수 있습니다."
)

st_folium(
    seoul_map,
    use_container_width=True,
    height=620,
    returned_objects=[]
)

# ==========================================
# 8. 관광지 설명 표시
# ==========================================

st.divider()

st.subheader("✨ 관광지 한눈에 보기")

for start in range(0, len(visible_places), 2):

    col1, col2 = st.columns(2)

    for col, place in zip(
        [col1, col2],
        visible_places[start:start + 2]
    ):

        with col:

            st.markdown(
                f"### {place['rank']}. {place['name']}"
            )

            st.caption(
                f"{place['english']} | {place['category']}"
            )

            st.write(place["description"])

            st.markdown(
                f"💡 **여행 팁:** {place['tip']}"
            )

            # 구글 지도 연결
            map_url = (
                "https://www.google.com/maps/search/?api=1&query="
                f"{place['lat']},{place['lon']}"
            )

            st.markdown(
                f"[🗺️ 구글 지도에서 위치 보기]({map_url})"
            )

            st.markdown("---")

# ==========================================
# 9. 참고 자료
# ==========================================

st.subheader("📚 참고 자료")

st.markdown(
    """
    - [서울시 공식 홈페이지](https://www.seoul.go.kr/)
    - [서울 관광 공식 홈페이지](https://english.visitseoul.net/)
    - [OpenStreetMap](https://www.openstreetmap.org/)
    """
)

st.caption(
    "※ 관광지 위치는 대표 지점의 안내용 좌표입니다. "
    "방문자 수와 선호도는 조사 기간 및 집계 방식에 따라 달라질 수 있습니다."
)

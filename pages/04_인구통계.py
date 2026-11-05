
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import re

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="서울 인구 데이터 분석",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ 서울시 연령별 인구 분석")
st.markdown(
    "📊 행정구역, 성별, 연도를 선택하여 "
    "연령대별 인구 분포를 분석해 보세요."
)

st.divider()


# ==========================================
# 2. CSV 파일 경로 설정
# ==========================================

# 현재 파일은 pages 폴더에 있으므로
# parent.parent를 사용하여 최상위 폴더로 이동

BASE_DIR = Path(__file__).resolve().parent.parent

possible_paths = [
    BASE_DIR / "population.csv",
    BASE_DIR / "population(5).csv"
]

CSV_PATH = None

for path in possible_paths:
    if path.exists():
        CSV_PATH = path
        break

if CSV_PATH is None:
    st.error(
        "❌ CSV 파일을 찾을 수 없습니다.\n\n"
        "최상위 폴더에 population.csv 파일이 있는지 "
        "확인해 주세요."
    )
    st.stop()


# ==========================================
# 3. CSV 데이터 읽기
# ==========================================

@st.cache_data
def load_data(file_path):

    # 한글 인코딩 자동 확인
    encodings = [
        "euc-kr",
        "cp949",
        "utf-8-sig",
        "utf-8"
    ]

    df = None
    encoding_used = None

    for encoding in encodings:
        try:
            df = pd.read_csv(
                file_path,
                encoding=encoding
            )
            encoding_used = encoding
            break

        except UnicodeDecodeError:
            continue

    if df is None:
        raise ValueError(
            "CSV 파일의 인코딩을 읽을 수 없습니다."
        )

    # 열 이름의 공백 제거
    df.columns = df.columns.astype(str).str.strip()

    # 행정구역 이름 정리
    df["행정구역"] = (
        df["행정구역"]
        .astype(str)
        .str.strip()
    )

    # 괄호 안의 행정구역 코드 제거
    df["지역명"] = df["행정구역"].str.replace(
        r"\s*\(\d+\)\s*$",
        "",
        regex=True
    ).str.strip()

    # 서울특별시 전체는 그대로 표시
    # 나머지는 자치구 이름만 표시
    df["선택지역"] = df["지역명"].apply(
        lambda x: (
            "서울특별시"
            if x == "서울특별시"
            else x.replace("서울특별시 ", "")
        )
    )

    # 숫자 데이터의 쉼표 제거 및 숫자 변환
    for col in df.columns:
        if col not in ["행정구역", "지역명", "선택지역"]:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(
                    ",", "", regex=False
                ),
                errors="coerce"
            )

    return df, encoding_used


try:
    df, encoding_used = load_data(str(CSV_PATH))

except Exception as e:
    st.error(f"데이터를 읽는 중 오류가 발생했습니다: {e}")
    st.stop()


# ==========================================
# 4. 선택 메뉴 만들기
# ==========================================

col1, col2, col3 = st.columns(3)

districts = df["선택지역"].tolist()

# 연도 자동 추출
years = sorted(
    set(
        re.findall(
            r"(\d{4})년_",
            " ".join(df.columns)
        )
    )
)

with col1:
    selected_district = st.selectbox(
        "📍 행정구역 선택",
        districts
    )

with col2:
    selected_gender = st.selectbox(
        "👥 성별 선택",
        ["전체", "남성", "여성"]
    )

with col3:
    selected_year = st.selectbox(
        "📅 연도 선택",
        years,
        index=len(years) - 1
    )


# ==========================================
# 5. 연령대별 데이터 추출
# ==========================================

age_columns = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]

# 실제 CSV 열 이름에 맞춘 성별 설정
gender_prefix = {
    "전체": "",
    "남성": "남_",
    "여성": "여_"
}

prefix = gender_prefix[selected_gender]

# 실제 CSV의 열 이름 구성
selected_columns = [
    f"{selected_year}년_{prefix}거주자_{age}"
    for age in age_columns
]

# 선택한 지역의 행 찾기
selected_row = df[
    df["선택지역"] == selected_district
]

if selected_row.empty:
    st.error("선택한 행정구역의 데이터가 없습니다.")
    st.stop()

# 필요한 열이 존재하는지 확인
missing_columns = [
    col for col in selected_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "필요한 데이터 열을 찾을 수 없습니다.\n\n"
        + "\n".join(missing_columns)
    )
    st.stop()

# 인구 데이터 가져오기
population_values = (
    selected_row.iloc[0][selected_columns]
    .fillna(0)
    .astype(int)
    .tolist()
)


# ==========================================
# 6. 선택 정보 표시
# ==========================================

st.subheader("📊 분석 결과")

info1, info2, info3 = st.columns(3)

with info1:
    st.metric(
        label="📍 행정구역",
        value=selected_district
    )

with info2:
    st.metric(
        label="👥 성별",
        value=selected_gender
    )

with info3:
    st.metric(
        label="📅 기준 연도",
        value=f"{selected_year}년"
    )


# ==========================================
# 7. 꺾은선 그래프 생성
# ==========================================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=age_columns,
        y=population_values,

        mode="lines+markers",

        name="인구수",

        # 핫핑크 선
        line=dict(
            color="#FF1493",
            width=4
        ),

        # 핫핑크 원형 표시
        marker=dict(
            color="#FF1493",
            size=10,
            line=dict(
                color="white",
                width=2
            )
        ),

        # 마우스를 올리면 인구수 표시
        hovertemplate=(
            "<b>%{x}</b><br>"
            "인구수: %{y:,.0f}명"
            "<extra></extra>"
        )
    )
)


# ==========================================
# 8. 그래프 전체 디자인
# ==========================================

fig.update_layout(

    title=dict(
        text=(
            f"{selected_district} "
            f"{selected_gender} 연령별 인구 분포 "
            f"({selected_year}년)"
        ),
        x=0.5,
        xanchor="center",
        font=dict(size=22)
    ),

    height=600,

    plot_bgcolor="white",
    paper_bgcolor="white",

    # 한글 표시를 위한 글꼴 설정
    font=dict(
        family="Malgun Gothic, AppleGothic, sans-serif",
        size=13,
        color="#333333"
    ),

    hovermode="x unified",

    margin=dict(
        l=80,
        r=30,
        t=100,
        b=80
    ),

    showlegend=False
)


# ==========================================
# 9. 가로축 설정
# ==========================================

fig.update_xaxes(

    title_text="나이",

    type="category",

    categoryorder="array",
    categoryarray=age_columns,

    tickmode="array",
    tickvals=age_columns,
    ticktext=age_columns,

    # 10살 단위 구분선
    showgrid=True,
    gridcolor="#E5E5E5",
    gridwidth=1,

    showline=True,
    linecolor="#AAAAAA",

    ticks="outside"
)


# ==========================================
# 10. 세로축 설정
# ==========================================

fig.update_yaxes(

    title_text="인구수 (명)",

    tickmode="linear",

    tick0=0,

    # 1,000만 명 단위
    dtick=10000000,

    tickformat=",",

    rangemode="tozero",

    showgrid=True,
    gridcolor="#DADADA",
    gridwidth=1,

    showline=True,
    linecolor="#AAAAAA",

    ticks="outside"
)


# ==========================================
# 11. 그래프 출력
# ==========================================

st.plotly_chart(
    fig,
    use_container_width=True
)


# 세로축 안내
max_population = max(population_values) if population_values else 0

if max_population < 10000000:
    st.info(
        "💡 안내: 연령대별 인구수는 1,000만 명보다 "
        "적습니다. 세로축 눈금을 1,000만 명 단위로 "
        "설정하여 그래프의 높이 차이가 작게 보일 수 있습니다."
    )


# ==========================================
# 12. 연령별 인구 데이터 표
# ==========================================

with st.expander("📋 연령대별 인구 데이터 확인하기"):

    result_df = pd.DataFrame({
        "연령대": age_columns,
        "인구수": population_values
    })

    result_df["인구수"] = result_df["인구수"].astype(int)

    st.dataframe(
        result_df.style.format({
            "인구수": "{:,}명"
        }),
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# 13. 데이터 정보
# ==========================================

st.divider()

st.caption(
    "📌 데이터 출처: 업로드된 서울시 인구 통계 CSV 파일"
)

st.caption(
    f"한글 인코딩 방식: {encoding_used.upper()}"
)

st.caption(
    "🏙️ 서울시 연령별 인구 데이터 분석 프로그램"
)

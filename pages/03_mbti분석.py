
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="국가별 MBTI 분석",
    page_icon="🌎",
    layout="wide"
)

st.title("🌎 세계 국가별 MBTI 분석")
st.write("국가를 선택하면 해당 국가의 MBTI 유형별 비율을 확인할 수 있습니다.")

# CSV 파일 불러오기
BASE_DIR = Path(__file__).parent

CSV_CANDIDATES = [
    BASE_DIR / "countriesMBTI_16types.csv",
    BASE_DIR / "countriesMBTI_16types.csv",
    BASE_DIR / "countriesMBTI.csv"
]

csv_path = next(
    (p for p in CSV_CANDIDATES if p.exists()),
    None
)

if csv_path is None:
    st.error("CSV 파일을 찾을 수 없습니다. GitHub 저장소를 확인해 주세요.")
    st.stop()

df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 데이터 확인
if "Country" not in df.columns:
    st.error("Country 열이 없습니다.")
    st.stop()

mbti_types = [col for col in df.columns if col != "Country"]

for col in mbti_types:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Country"] = df["Country"].astype(str).str.strip()
df = df.dropna(subset=["Country"])

countries = sorted(df["Country"].unique())

# 국가 선택
default_index = (
    countries.index("South Korea")
    if "South Korea" in countries else 0
)

selected_country = st.selectbox(
    "🌍 국가를 선택하세요.",
    countries,
    index=default_index
)

# 선택한 국가 데이터
country_data = df[df["Country"] == selected_country].iloc[0]

chart_data = pd.DataFrame({
    "MBTI": mbti_types,
    "비율": [country_data[x] for x in mbti_types]
})

chart_data = chart_data.dropna()
chart_data = chart_data.sort_values(
    "비율",
    ascending=False
).reset_index(drop=True)

# 색상 변환 함수
def hex_to_rgb(color):
    color = color.lstrip("#")
    return tuple(
        int(color[i:i+2], 16)
        for i in (0, 2, 4)
    )

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

# 파란색 그라데이션 생성
def make_gradient(start, end, count):
    start_rgb = hex_to_rgb(start)
    end_rgb = hex_to_rgb(end)

    colors = []

    for i in range(count):
        ratio = i / max(count - 1, 1)

        rgb = tuple(
            round(
                start_rgb[j] +
                (end_rgb[j] - start_rgb[j]) * ratio
            )
            for j in range(3)
        )

        colors.append(rgb_to_hex(rgb))

    return colors

blue_colors = make_gradient(
    "#1457C5",
    "#DCEBFF",
    max(len(chart_data) - 1, 1)
)

# 1등은 빨간색, 나머지는 파란색 그라데이션
bar_colors = ["#EF4444"] + blue_colors[:len(chart_data)-1]

# 그래프 생성
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_data["비율"],
        y=chart_data["MBTI"],
        orientation="h",
        marker_color=bar_colors,
        text=chart_data["비율"].apply(
            lambda x: f"{x:.2%}"
        ),
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "비율: %{x:.2%}"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    title=f"📊 {selected_country}의 MBTI 유형별 비율",
    xaxis_title="MBTI 비율",
    yaxis_title="MBTI 유형",
    xaxis=dict(
        tickformat=".0%",
        rangemode="tozero"
    ),
    yaxis=dict(
        categoryorder="array",
        categoryarray=chart_data["MBTI"].tolist(),
        autorange="reversed"
    ),
    height=650,
    template="plotly_white",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 1위 유형 표시
top = chart_data.iloc[0]

st.success(
    f"🏆 가장 높은 비율의 유형은 "
    f"{top['MBTI']}이며, 비율은 {top['비율']:.2%}입니다."
)

# 전체 순위표
with st.expander("📋 MBTI 비율 전체 순위 보기"):

    display_data = chart_data.copy()

    display_data.insert(
        0,
        "순위",
        range(1, len(display_data) + 1)
    )

    display_data["비율"] = display_data["비율"].map(
        lambda x: f"{x:.2%}"
    )

    st.dataframe(
        display_data.rename(
            columns={"MBTI": "MBTI 유형"}
        ),
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "※ 제공된 CSV 원본 비율을 그대로 표시합니다."
)

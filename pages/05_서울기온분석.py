
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 월별 기온분석")
st.write("원하는 월을 선택하면 전체 연도별 최고기온과 최저기온을 비교합니다.")

# CSV 파일 경로 찾기
current_dir = Path(__file__).resolve().parent

file_candidates = [
    current_dir / "temperature.csv",
    current_dir / "temperature(2).csv",
    current_dir.parent / "temperature.csv",
    current_dir.parent / "temperature(2).csv"
]

csv_path = next(
    (path for path in file_candidates if path.exists()),
    None
)

# 파일 불러오기
if csv_path is None:
    st.error("CSV 파일을 찾을 수 없습니다. 파일 위치를 확인해주세요.")
    st.stop()

try:
    df = pd.read_csv(csv_path, encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 필요한 열 확인
required_columns = ["일시", "최고기온(℃)", "최저기온(℃)"]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일의 열 이름을 확인해주세요.")
    st.stop()

# 날짜 처리
# 데이터는 1907년 10월부터 2026년 10월까지
# 월별 순서대로 기록되어 있음
month_dict = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

dates = []
start_year = 1907
start_month = 10

for i, value in enumerate(df["일시"]):
    month_name = str(value).split("-")[0]

    if month_name not in month_dict:
        st.error(f"날짜 데이터 오류: {value}")
        st.stop()

    total_month = start_month - 1 + i

    year = start_year + total_month // 12
    month = total_month % 12 + 1

    # CSV의 월 정보와 순서 확인
    if month_dict[month_name] != month:
        st.error(f"날짜 순서가 올바르지 않습니다: {value}")
        st.stop()

    dates.append(pd.Timestamp(year, month, 1))

df["날짜"] = dates

# 연도와 월 추출
df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

# 월 선택
month_names = {
    1: "1월", 2: "2월", 3: "3월", 4: "4월",
    5: "5월", 6: "6월", 7: "7월", 8: "8월",
    9: "9월", 10: "10월", 11: "11월", 12: "12월"
}

selected_month = st.selectbox(
    "분석할 월을 선택하세요.",
    options=list(month_names.keys()),
    format_func=lambda x: month_names[x],
    index=0
)

# 선택한 월 데이터 추출
filtered_df = df[df["월"] == selected_month].copy()

# 기온 데이터 숫자형 변환
filtered_df["최고기온(℃)"] = pd.to_numeric(
    filtered_df["최고기온(℃)"], errors="coerce"
)

filtered_df["최저기온(℃)"] = pd.to_numeric(
    filtered_df["최저기온(℃)"], errors="coerce"
)

# 결측치가 있는 행 제외
filtered_df = filtered_df.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"]
)

# 연도순 정렬
filtered_df = filtered_df.sort_values("연도")

# 그래프 생성
fig = go.Figure()

# 최고기온 그래프
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="hotpink",
            width=3
        ),
        marker=dict(size=6)
    )
)

# 최저기온 그래프
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="skyblue",
            width=3
        ),
        marker=dict(size=6)
    )
)

# 그래프 꾸미기
fig.update_layout(
    title={
        "text": f"{selected_month}월 기온분석",
        "x": 0.5,
        "xanchor": "center"
    },
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    legend_title="범례",
    hovermode="x unified",
    template="plotly_white",
    height=550
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 분석 데이터 출력
st.subheader("📊 연도별 기온 데이터")

display_df = filtered_df[
    ["연도", "최고기온(℃)", "최저기온(℃)"]
].copy()

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# 데이터 개수 안내
st.caption(
    f"총 {len(filtered_df)}개 연도의 {selected_month}월 기온 데이터를 분석했습니다."
)


import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures

# --------------------------------------------------
# 1. 데이터 불러오기
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_CANDIDATES = [
    BASE_DIR / "temperature.csv",
    BASE_DIR / "temperature(4).csv"
]

CSV_PATH = next(
    (p for p in FILE_CANDIDATES if p.exists()),
    None
)

st.title("🌡️ 월별 평균기온 분석 및 미래 예측")
st.write(
    "1907년부터 2025년까지의 기온 데이터를 분석하고 "
    "인공지능 예측 알고리즘 3가지로 미래 기온을 예측합니다."
)

if CSV_PATH is None:
    st.error("CSV 파일을 찾을 수 없습니다. 저장소 최상위 폴더에 temperature.csv를 업로드해 주세요.")
    st.stop()

try:
    df = pd.read_csv(CSV_PATH, encoding="cp949")
except UnicodeDecodeError:
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    except Exception as e:
        st.error(f"CSV 파일을 읽을 수 없습니다: {e}")
        st.stop()

# --------------------------------------------------
# 2. 날짜 데이터 가공
# --------------------------------------------------

month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3,
    "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9,
    "Oct": 10, "Nov": 11, "Dec": 12
}

def convert_date(value):
    try:
        month_text, year_text = str(value).strip().split("-")
        month = month_map[month_text]
        short_year = int(year_text)

        # 07~99는 1900년대, 00~06은 2000년대로 처리
        year = (
            1900 + short_year
            if short_year >= 7
            else 2000 + short_year
        )

        return year, month

    except (ValueError, KeyError, TypeError):
        return None, None


converted = df["일시"].apply(convert_date)

df["연도"] = converted.apply(lambda x: x[0])
df["월"] = converted.apply(lambda x: x[1])

df["평균기온(℃)"] = pd.to_numeric(
    df["평균기온(℃)"], errors="coerce"
)

# 1907~2025년 데이터만 분석
df = df[
    (df["연도"] >= 1907) &
    (df["연도"] <= 2025)
].copy()

df = df.dropna(subset=["연도", "월"])
df["연도"] = df["연도"].astype(int)
df["월"] = df["월"].astype(int)

if df.empty:
    st.error("분석할 데이터가 없습니다. 날짜 형식을 확인해 주세요.")
    st.stop()

# --------------------------------------------------
# 3. 월 선택
# --------------------------------------------------

st.subheader("① 분석할 월 선택")

selected_month = st.selectbox(
    "분석할 월을 선택하세요.",
    list(range(1, 13)),
    format_func=lambda x: f"{x}월"
)

# 선택한 월의 데이터
monthly = df[
    df["월"] == selected_month
][["연도", "평균기온(℃)"]].copy()

monthly = monthly.sort_values("연도")

# 결측치 제거
monthly = monthly.dropna(subset=["평균기온(℃)"])

if len(monthly) < 3:
    st.warning("예측에 필요한 데이터가 충분하지 않습니다.")
    st.stop()

st.caption(
    f"분석 데이터: {monthly['연도'].min()}년 ~ "
    f"{monthly['연도'].max()}년 / "
    f"유효 데이터 {len(monthly)}개"
)

# --------------------------------------------------
# 4. 과거 기온 그래프
# --------------------------------------------------

st.subheader("② 과거 평균기온 변화")

fig_history = go.Figure()

fig_history.add_trace(
    go.Scatter(
        x=monthly["연도"],
        y=monthly["평균기온(℃)"],
        mode="lines+markers",
        name="평균기온",
        line=dict(color="#FF1493", width=2),
        marker=dict(size=5)
    )
)

fig_history.update_layout(
    title=f"{selected_month}월 연도별 평균기온 변화 (1907~2025년)",
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    template="plotly_white",
    hovermode="x unified",
    height=430
)

st.plotly_chart(fig_history, use_container_width=True)

st.info(
    "📌 그래프 해석: 가로축은 연도, 세로축은 평균기온입니다. "
    "그래프의 전체적인 흐름을 살펴보며 기온이 어떻게 변화했는지 확인해 보세요."
)

# --------------------------------------------------
# 5. 미래 예측연도 입력
# --------------------------------------------------

st.subheader("③ 미래 평균기온 예측")

predict_year = st.number_input(
    "몇 년의 평균기온을 예측할까요?",
    min_value=2026,
    max_value=2100,
    value=2035,
    step=1
)

st.caption(
    "1907~2025년의 선택한 월별 평균기온을 학습하여 "
    "입력한 연도의 기온을 예측합니다."
)

# --------------------------------------------------
# 6. 예측 알고리즘 학습
# --------------------------------------------------

X = monthly[["연도"]].values
y = monthly["평균기온(℃)"].values

# 미래 예측용 연도
future_years = np.arange(
    monthly["연도"].min(),
    predict_year + 1
).reshape(-1, 1)

# ① 선형 회귀
linear_model = LinearRegression()
linear_model.fit(X, y)

linear_predictions = linear_model.predict(future_years)

# ② 랜덤 포레스트
rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=5,
    min_samples_leaf=3,
    random_state=42
)

rf_model.fit(X, y)

rf_predictions = rf_model.predict(future_years)

# ③ 다항 회귀 (2차식)
poly = PolynomialFeatures(degree=2)

X_poly = poly.fit_transform(X)
future_poly = poly.transform(future_years)

poly_model = LinearRegression()
poly_model.fit(X_poly, y)

poly_predictions = poly_model.predict(future_poly)

# --------------------------------------------------
# 7. 예측 결과 비교 그래프
# --------------------------------------------------

st.subheader("④ 예측 알고리즘 3가지 비교")

fig = go.Figure()

# 실제 과거 기온
fig.add_trace(
    go.Scatter(
        x=monthly["연도"],
        y=monthly["평균기온(℃)"],
        mode="lines+markers",
        name="실제 평균기온",
        line=dict(color="black", width=2),
        marker=dict(size=4)
    )
)

# 예측 알고리즘 3개
model_data = [
    (
        "선형 회귀",
        linear_predictions,
        "#FF1493"
    ),
    (
        "랜덤 포레스트",
        rf_predictions,
        "#1E90FF"
    ),
    (
        "다항 회귀",
        poly_predictions,
        "#2E8B57"
    )
]

# 과거 학습 구간의 모델 결과
for name, predictions, color in model_data:

    fig.add_trace(
        go.Scatter(
            x=future_years.flatten(),
            y=predictions,
            mode="lines",
            name=f"{name} 학습 및 예측",
            line=dict(
                color=color,
                width=2,
                dash="dash"
            )
        )
    )

# 2025년 이후 예측 구간 표시
fig.add_vline(
    x=2025,
    line_dash="dot",
    line_color="gray",
    annotation_text="미래 예측 시작",
    annotation_position="top"
)

fig.update_layout(
    title=f"{selected_month}월 평균기온 미래 예측 비교",
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    template="plotly_white",
    hovermode="x unified",
    height=550,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    )
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "📌 검은색 선은 실제 관측 기온이며, "
    "점선 3개는 각각 다른 알고리즘이 계산한 기온입니다. "
    "2025년 이후의 점선 모양을 비교해 보세요."
)

# --------------------------------------------------
# 8. 최종 예측값 비교
# --------------------------------------------------

st.subheader(f"⑤ {predict_year}년 {selected_month}월 예측 결과")

# 마지막 연도의 예측값
linear_result = float(
    linear_model.predict([[predict_year]])[0]
)

rf_result = float(
    rf_model.predict([[predict_year]])[0]
)

poly_result = float(
    poly_model.predict(
        poly.transform([[predict_year]])
    )[0]
)

result_df = pd.DataFrame({
    "알고리즘": [
        "선형 회귀",
        "랜덤 포레스트",
        "다항 회귀"
    ],
    "예측 평균기온(℃)": [
        round(linear_result, 2),
        round(rf_result, 2),
        round(poly_result, 2)
    ]
})

st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# 9. 알고리즘별 설명
# --------------------------------------------------

st.subheader("⑥ 알고리즘별 작동 원리 알아보기")

with st.expander("🌸 1. 선형 회귀 (Linear Regression)"):

    st.markdown("""
    **핵심 원리: 데이터를 가장 잘 설명하는 직선을 찾습니다.**

    - 과거 기온이 전체적으로 상승하는지 하락하는지 분석합니다.
    - 연도와 평균기온 사이의 관계를 직선으로 표현합니다.
    - 미래에도 지금까지의 상승·하락 추세가 이어진다고 가정합니다.

    **그래프에서 관찰할 점**

    - 직선 형태로 일정하게 증가하거나 감소합니다.
    - 장기적인 기온 변화 방향을 쉽게 파악할 수 있습니다.

    **한계점**

    - 기온이 실제로 곡선 형태로 변화하더라도 직선으로만 예측합니다.
    """)

with st.expander("🔵 2. 랜덤 포레스트 (Random Forest)"):

    st.markdown("""
    **핵심 원리: 여러 개의 의사결정나무가 예측한 결과를 평균 냅니다.**

    - 과거 데이터를 여러 부분으로 나누어 학습합니다.
    - 여러 의사결정나무가 각각 기온을 예측합니다.
    - 각 나무의 예측 결과를 종합하여 최종값을 계산합니다.

    **그래프에서 관찰할 점**

    - 직선보다는 계단 모양의 변화가 나타날 수 있습니다.
    - 과거 데이터의 특정 구간에서 학습한 기온 범위를 활용합니다.
    - 학습 데이터의 최대 연도보다 먼 미래에서는 예측값이 일정해지는 특징이 있습니다.

    **한계점**

    - 과거에 없었던 새로운 추세가 미래에도 계속되는 상황을 잘 예측하지 못할 수 있습니다.
    """)

with st.expander("🟢 3. 다항 회귀 (Polynomial Regression)"):

    st.markdown("""
    **핵심 원리: 직선이 아닌 곡선으로 데이터의 변화 추세를 찾습니다.**

    - 선형 회귀에 제곱 항을 추가합니다.
    - 기온이 일정한 직선 형태가 아니라 휘어진 형태로 변화하는 경우를 표현할 수 있습니다.
    - 이번 프로그램에서는 2차 함수를 사용합니다.

    **그래프에서 관찰할 점**

    - 직선이 아니라 곡선 형태로 나타납니다.
    - 기온의 상승 속도가 빨라지거나 느려지는 모습을 표현할 수 있습니다.

    **한계점**

    - 먼 미래로 예측할수록 곡선이 급격하게 변할 수 있습니다.
    - 실제 기온 변화가 반드시 이 곡선을 따라간다는 의미는 아닙니다.
    """)

# --------------------------------------------------
# 10. 수업 활동 및 주의사항
# --------------------------------------------------

st.subheader("⑦ 생각해 보기")

st.markdown("""
다음 질문에 답해 보세요.

1. 세 가지 알고리즘 중 미래 기온이 가장 높게 예측된 알고리즘은 무엇인가요?
2. 랜덤 포레스트의 미래 예측값이 일정해지는 이유는 무엇일까요?
3. 다항 회귀의 곡선이 미래에 급격하게 상승하거나 하락한다면 그 예측을 신뢰할 수 있을까요?
4. 실제 미래 기온을 가장 정확하게 예측하는 알고리즘은 무엇일까요?
""")

st.warning(
    "주의: 이 프로그램은 교육용 데이터 분석 및 예측 실습입니다. "
    "실제 기후예측 모델은 온실가스 배출량, 해양, 대기 순환 등 "
    "다양한 변수를 활용합니다. 이 프로그램의 결과를 실제 기후예측값으로 "
    "해석해서는 안 됩니다."
)

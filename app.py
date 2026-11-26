import streamlit as st
import pandas as pd
import altair as alt

st.title("🌍 지구 온도 상승, 정말 이산화탄소 때문일까?")

# --- 1. 데이터 불러오기 및 전처리 ---
st.header("1. 데이터 전처리 및 개요")

df = pd.read_csv("climate_data.csv")

# 2003년 이상 데이터만 남기고 결측치 제거 (1999~2002년 이상치 4개 행 제거)
original_row_count = len(df)
df_clean = df[df['연도'] >= 2003].dropna()
cleaned_row_count = len(df_clean)

st.subheader("결측치·이상치 처리 기준 및 편향 점검")
st.markdown("""
* **결측치 처리 기준:** 원본 데이터(27행) 내 빈 값(결측치)은 `0개`입니다.
* **이상치 처리 기준:** 1999~2002년 평균 온도가 `8.16~8.78°C`로 2003년 이후(`13.79~15.84°C`)에 비해 비정상적으로 낮게 측정되었고, 원본 대기질 표에서도 해당 기간의 다른 기상 관측값(풍향·풍속 등)이 누락되어 있어 초기 측정 불완전 구간(이상치)으로 판단해 **4개 행(1999~2002년)을 제거**했습니다.
* **처리로 생길 수 있는 치우침(편향):** 초기 4개년 데이터를 제거하면서 표본 수가 27개에서 23개로 줄어들어, 2000년대 초반을 포함한 더 장기적인 기온 상승 추세가 축소되어 보이는 치우침(편향)이 생길 수 있습니다.
""")

st.write(f"전처리 전 데이터: **{original_row_count}행** ➔ 전처리 후 데이터: **{cleaned_row_count}행** (이상치 4행 제거)")

st.subheader("데이터 개요 (전처리 후)")
st.write(f"데이터 크기: **{df_clean.shape[0]}행, {df_clean.shape[1]}열**")

col1, col2 = st.columns(2)
with col1:
    st.write("✔️ 각 열의 자료형")
    st.dataframe(df_clean.dtypes.astype(str))
with col2:
    st.write("✔️ 열별 빈 값(결측치) 개수")
    st.dataframe(df_clean.isnull().sum())


# --- 2. 탐색적 데이터 분석 (가독성 개선 그래프 2종) ---
st.header("2. 탐색적 데이터 분석 (시각화)")

# [그래프 1] 연도별 CO2 농도와 평균 온도 추이 (상하 2단 비교로 겹침 제거)
st.subheader("그래프 1. 연도별 CO2 농도 vs 평균 온도 변화 추이 (2003~2025)")
st.caption("🔴 위쪽: 이산화탄소(CO2) 농도 추이 / 🔵 아래쪽: 평균 온도 추이 (같은 연도별로 위아래 비교)")

chart_co2 = alt.Chart(df_clean).mark_line(color='#E63946', strokeWidth=3, point=alt.OverlayMarkDef(size=70, color='#E63946')).encode(
    x=alt.X('연도:O', title=None, axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('CO2농도:Q', title='CO2 농도 (ppm)', scale=alt.Scale(zero=False)),
    tooltip=['연도', 'CO2농도', '평균온도']
).properties(
    title='① 연도별 이산화탄소(CO2) 농도 변화 (ppm)',
    height=230
)

chart_temp = alt.Chart(df_clean).mark_line(color='#1D3557', strokeWidth=3, point=alt.OverlayMarkDef(size=70, color='#1D3557')).encode(
    x=alt.X('연도:O', title='연도 (Year)', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('평균온도:Q', title='평균 온도 (°C)', scale=alt.Scale(zero=False)),
    tooltip=['연도', 'CO2농도', '평균온도']
).properties(
    title='② 연도별 평균 온도 변화 (°C)',
    height=230
)

st.altair_chart(chart_co2, use_container_width=True)
st.altair_chart(chart_temp, use_container_width=True)


# [그래프 2] CO2 농도와 평균 온도의 상관관계 (산점도 + 추세선)
st.subheader("그래프 2. CO2 농도와 평균 온도의 상관관계 (산점도)")
corr_value = df_clean['CO2농도'].corr(df_clean['평균온도'])

points = alt.Chart(df_clean).mark_circle(size=90, color='#6A4C93', opacity=0.85).encode(
    x=alt.X('CO2농도:Q', title='이산화탄소(CO2) 농도 (ppm)', scale=alt.Scale(zero=False)),
    y=alt.Y('평균온도:Q', title='평균 온도 (°C)', scale=alt.Scale(zero=False)),
    tooltip=['연도', 'CO2농도', '평균온도']
)

trend_line = points.transform_regression('CO2농도', '평균온도').mark_line(color='#E63946', strokeDash=[6, 4], strokeWidth=2.5)

chart2 = (points + trend_line).properties(
    title=f'CO2 농도와 평균 온도의 상관관계 및 추세선 (상관계수 r = {corr_value:.2f})',
    height=320
)
st.altair_chart(chart2, use_container_width=True)


# --- 3. 분석 결과 및 인사이트 ---
st.header("3. 분석 결과 및 인사이트")

st.subheader("🔍 그래프에서 찾아낸 점 (근거 수치)")
st.info(f"""
* **CO2의 지속적 증가:** 2003년 `379.9ppm`이던 CO2 농도는 2025년 `434.0ppm`으로 23년간 한 해도 빠짐없이 `54.1ppm(약 14.2%)` 꾸준히 증가했습니다.
* **평균 온도의 변동성:** 같은 기간 평균 온도는 2011년 최저 `13.79°C`에서 2024년 최고 `15.84°C`까지 `2.05°C` 폭으로 오르내림을 반복했으며, 두 변수의 상관계수는 **`{corr_value:.2f}`**로 나타났습니다.
""")

st.subheader("💡 예상과 달랐던 점 및 다음 분석 과제")
st.success("""
* **예상과 다른 점:** 처음에는 CO2가 오르면 지역 평균 온도도 직선으로 함께 오를 것이라 예상했으나, 초기 이상치(1999~2002년)를 제거하고 보니 CO2는 매년 직선으로 상승하는 반면 경상남도 평균 온도는 2004년(`15.61°C`)에도 높았다가 2011년(`13.79°C`)에 낮아지는 등 단기 등락이 컸습니다.
* **다음 분석에서 확인할 점:** 지역 단위(경상남도) 기온은 전 지구 평균과 달리 해류(엘니뇨·라니냐)나 국지적 기상 변동의 영향을 크게 받으므로, 다음 분석에서는 전 지구 평균 기온 데이터와 비교하거나 다른 온실가스(메탄 등) 변수를 추가해 검증해보고 싶습니다.
""")

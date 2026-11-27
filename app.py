import streamlit as st
import pandas as pd
import altair as alt

st.title("🌍 지구 온도 상승, 정말 이산화탄소 때문일까?")

# --- 1. 데이터 전처리 및 개요 ---
st.header("1. 데이터 개요 및 전처리")

df = pd.read_csv("climate_data.csv")
original_row_count = len(df)
df_clean = df[df['연도'] >= 2003].dropna()
cleaned_row_count = len(df_clean)

st.write(f"**데이터 크기:** 전처리 전 `{original_row_count}행` ➔ 전처리 후 `{cleaned_row_count}행, {df_clean.shape[1]}열`")

st.markdown("""
* **결측치 기준:** 빈 값 `0개`로 삭제된 결측 행 없음
* **이상치 기준:** 1999~2002년(`8.16~8.78°C`)은 초기 관측 누락이 동반된 비정상 저온 구간으로 판단해 **4개 행 제거**
* **치우침(편향) 점검:** 초기 4개년 제거로 표본이 축소되어 2000년대 초반을 포함한 장기 상승 폭이 다소 완만하게 보일 수 있음
""")

col1, col2 = st.columns(2)
with col1:
    st.write("✔️ 열별 자료형")
    st.dataframe(df_clean.dtypes.astype(str), use_container_width=True)
with col2:
    st.write("✔️ 열별 빈 값 개수")
    st.dataframe(df_clean.isnull().sum(), use_container_width=True)


# --- 2. 데이터 시각화 ---
st.header("2. 탐색적 데이터 분석 (시각화)")

# 그래프 1: 연도별 CO2 농도 및 평균 온도 변화 추이
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

# 그래프 2: CO2 농도와 평균 온도의 상관관계 (산점도 + 추세선)
corr_value = df_clean['CO2농도'].corr(df_clean['평균온도'])

points = alt.Chart(df_clean).mark_circle(size=90, color='#6A4C93', opacity=0.85).encode(
    x=alt.X('CO2농도:Q', title='이산화탄소(CO2) 농도 (ppm)', scale=alt.Scale(zero=False)),
    y=alt.Y('평균온도:Q', title='평균 온도 (°C)', scale=alt.Scale(zero=False)),
    tooltip=['연도', 'CO2농도', '평균온도']
)

trend_line = points.transform_regression('CO2농도', '평균온도').mark_line(color='#E63946', strokeDash=[6, 4], strokeWidth=2.5)

chart2 = (points + trend_line).properties(
    title=f'③ CO2 농도와 평균 온도의 상관관계 (상관계수 r = {corr_value:.2f})',
    height=320
)
st.altair_chart(chart2, use_container_width=True)


# --- 3. 핵심 분석 결과 ---
st.header("3. 핵심 분석 결과")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.subheader("🔍 주요 발견 (근거 수치)")
    st.info(f"""
    * **CO2 지속 상승:** 2003년 `379.9ppm` ➔ 2025년 `434.0ppm` (`+54.1ppm`, 약 `14.2%` 증가)
    * **온도 변동 폭:** 2011년 최저 `13.79°C` ~ 2024년 최고 `15.84°C` (`2.05°C` 차이)
    * **양의 상관관계:** 상관계수 **`r = {corr_value:.2f}`**
    """)

with res_col2:
    st.subheader("💡 예상과 다른 점 & 다음 계획")
    st.success("""
    * **예상과 다른 점:** CO2는 매년 직선으로 오르지만, 지역 평균 온도는 해마다 오르내림(단기 등락)이 큼
    * **다음 분석 과제:** 전 지구 평균 기온 데이터와 비교하고, 메탄·엘니뇨 등 다른 기후 변수를 추가해 회귀 모델로 검증 예정
    """)

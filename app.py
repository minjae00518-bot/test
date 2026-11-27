import streamlit as st
import pandas as pd
import altair as alt

st.title("🌍 지구 온도 상승, 정말 이산화탄소 때문일까?")

df = pd.read_csv("climate_data.csv")
df_clean = df[df['연도'] >= 2003].dropna()

# --- 데이터 시각화 ---
st.header("탐색적 데이터 분석 (시각화)")

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

# --- 핵심 분석 결과 ---
st.header("핵심 분석 결과")

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

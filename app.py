import streamlit as st
import pandas as pd
import altair as alt

st.title("🌍 지구 온도 상승, 정말 이산화탄소 때문일까?")

# 데이터 불러오기 및 2003년 이후 데이터 필터링
df = pd.read_csv("climate_data.csv")
df_clean = df[df['연도'] >= 2003].dropna()

# --- 데이터 시각화 ---
st.header("탐색적 데이터 분석 (시각화)")

# 그래프 1: 연도별 CO2 농도 추이
chart_co2 = alt.Chart(df_clean).mark_line(color='#E63946', strokeWidth=3, point=alt.OverlayMarkDef(size=70, color='#E63946')).encode(
    x=alt.X('연도:O', title=None, axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('CO2농도:Q', title='CO2 농도 (ppm)', scale=alt.Scale(zero=False)),
    tooltip=['연도', 'CO2농도', '평균온도']
).properties(
    title='① 연도별 이산화탄소(CO2) 농도 변화 (ppm)',
    height=230
)

# 그래프 2: 연도별 평균 온도 추이
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

# 그래프 3: 산점도 및 추세선
corr_value = df_clean['CO2농도'].corr(df_clean['평균온도'])

points = alt.Chart(df_clean).mark_circle(size=90, color='#6A4C93', opacity=0.85).encode(
    x=alt.X('CO2농도:Q', title='이산화탄소(CO2) 농도 (ppm)', scale=alt.Scale(zero=False)),
    y=alt.Y('평균온도:Q', title='평균 온도 (°C)', scale=alt.Scale(zero=False)),
    tooltip=['연도', 'CO2농도', '평균온도']
)

trend_line = points.transform_regression('CO2농도', '평균온도').mark_line(color='#E63946', strokeDash=[6, 4], strokeWidth=2.5)

chart2 = (points + trend_
          

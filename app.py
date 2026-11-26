import streamlit as st
import pandas as pd
import altair as alt

st.title("🌍 지구 온도 상승, 정말 이산화탄소 때문일까?")

# --- 1. 데이터 불러오기 및 전처리 ---
st.header("1. 데이터 전처리 및 개요")

df = pd.read_csv("climate_data.csv")

st.subheader("결측치·이상치 처리 기준 및 편향 점검")
st.markdown("""
* **결측치 처리 기준:** 1999~2025년 데이터 내 빈 값(결측치)이 `0개`이므로 삭제하거나 대체한 행이 없습니다.
* **이상치 처리 기준:** 1999~2002년 평균 온도가 `8.16~8.78°C`로, 2003년 이후(`13.79~15.84°C`)에 비해 유독 낮게 기록된 이상치 구간이 존재합니다. 장기 추세 보존을 위해 임의로 삭제하지 않고 분석에 포함했습니다.
* **처리로 생길 수 있는 치우침(편향):** 초기(1999~2002년)의 낮은 온도 이상치를 삭제하지 않고 유지했기 때문에, 전체 기간의 기온 상승 폭이 실제보다 가파르게 과대평가되는 치우침(편향)이 발생할 수 있습니다.
""")

original_row_count = len(df)
df_clean = df.dropna()
cleaned_row_count = len(df_clean)

st.write(f"전처리 전 데이터: **{original_row_count}행** ➔ 전처리 후 데이터: **{cleaned_row_count}행**")

st.subheader("데이터 개요")
st.write(f"데이터 크기: **{df_clean.shape[0]}행, {df_clean.shape[1]}열**")

col1, col2 = st.columns(2)
with col1:
    st.write("✔️ 각 열의 자료형")
    st.dataframe(df_clean.dtypes.astype(str))
with col2:
    st.write("✔️ 열별 빈 값(결측치) 개수")
    st.dataframe(df_clean.isnull().sum())


# --- 2. 탐색적 데이터 분석 (그래프 2개) ---
st.header("2. 탐색적 데이터 분석 (시각화)")

# [그래프 1] 연도별 CO2 농도와 평균 온도 추이 (이중 축 선 그래프)
st.subheader("그래프 1. 연도별 CO2 농도와 평균 온도 변화 추이")

base = alt.Chart(df_clean).encode(
    x=alt.X('연도:O', title='연도 (Year)')
)
line_co2 = base.mark_line(color='red', point=True).encode(
    y=alt.Y('CO2농도:Q', title='이산화탄소(CO2) 농도 (ppm)', scale=alt.Scale(zero=False)),
    tooltip=['연도', 'CO2농도', '평균온도']
)
line_temp = base.mark_line(color='blue', strokeDash=[5, 5], point=True).encode(
    y=alt.Y('평균온도:Q', title='평균 온도 (°C)', scale=alt.Scale(zero=False)),
    tooltip=['연도', 'CO2농도', '평균온도']
)
chart1 = alt.layer(line_co2, line_temp).resolve_scale(
    y='independent'
).properties(
    title='연도별 이산화탄소(CO2) 농도와 평균 온도의 변화'
)
st.altair_chart(chart1, use_container_width=True)

# [그래프 2] CO2 농도와 평균 온도의 상관관계 (산점도)
st.subheader("그래프 2. CO2 농도와 평균 온도의 상관관계 (산점도)")
corr_value = df_clean['CO2농도'].corr(df_clean['평균온도'])

chart2 = alt.Chart(df_clean).mark_circle(size=80, color='purple').encode(
    x=alt.X('CO2농도:Q', title='이산화탄소(CO2) 농도 (ppm)', scale=alt.Scale(zero=False)),
    y=alt.Y('평균온도:Q', title='평균 온도 (°C)', scale=alt.Scale(zero=False)),
    tooltip=['연도', 'CO2농도', '평균온도']
).properties(
    title=f'CO2 농도와 평균 온도의 상관관계 (상관계수 r = {corr_value:.2f})'
)
st.altair_chart(chart2, use_container_width=True)


# --- 3. 분석 결과 및 인사이트 ---
st.header("3. 분석 결과 및 인사이트")

st.subheader("🔍 그래프에서 찾아낸 점 (근거 수치)")
st.info(f"""
* **장기적 비례 추세:** 1999년 `371.2ppm`이던 CO2 농도는 2025년 `434.0ppm`으로 27년간 매년 빠짐없이 `62.8ppm(약 16.9%)` 증가했고, 평균 온도 역시 1999년 `8.64°C`에서 2024년 `15.84°C`까지 전반적으로 상승했습니다.
* **양의 상관관계:** 두 변수의 피어슨 상관계수는 **`{corr_value:.2f}`**로, 이산화탄소 농도가 높을수록 평균 온도도 높아지는 양의 상관관계를 확인했습니다.
""")

st.subheader("💡 예상과 달랐던 점 및 다음 분석 과제")
st.success("""
* **예상과 다른 점:** CO2 농도는 27년간 일직선으로 꾸준히 상승했지만, 평균 온도는 2003년(`14.62°C`) 이후 2025년(`15.08°C`)까지 `13.79°C~15.84°C` 사이에서 오르내림을 반복하며 단기적으로는 CO2 증가율만큼 가파르게 오르지 않았습니다.
* **다음 분석에서 확인할 점:** 이산화탄소 외에 단기적인 기온 등락에 영향을 주는 다른 온실가스(메탄 등)나 기후 요인(엘니뇨·라니냐 등)을 추가하고, 회귀 모델을 적용해 CO2만으로 온도를 얼마나 정확히 예측할 수 있는지 검증할 계획입니다.
""")

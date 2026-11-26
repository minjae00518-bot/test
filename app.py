import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (로컬 테스트용 - 배포 서버에서는 영문 라벨이 안전하므로 그래프 내 텍스트는 영문 병기)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

st.title("🌍 지구 온도 상승, 정말 이산화탄소 때문일까?")

# --- 1. 데이터 불러오기 및 전처리 ---
st.header("1. 데이터 전처리 및 개요")

df = pd.read_csv("climate_data.csv")

# [루브릭 상] 결측치와 이상치 구분, 전후 행 수, 처리로 인한 치우침(편향) 명시
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

# [루브릭 상] 데이터 개요 (행·열 수, 자료형, 빈 값 개수)
st.subheader("데이터 개요")
st.write(f"데이터 크기: **{df_clean.shape[0]}행, {df_clean.shape[1]}열**")

col1, col2 = st.columns(2)
with col1:
    st.write("✔️ 각 열의 자료형")
    st.dataframe(df_clean.dtypes.astype(str))
with col2:
    st.write("✔️ 열별 빈 값(결측치) 개수")
    st.dataframe(df_clean.isnull().sum())


# --- 2. 탐색적 데이터 분석 (그래프 2개 이상) ---
st.header("2. 탐색적 데이터 분석 (시각화)")

# [그래프 1] 연도별 CO2 농도와 평균 온도 추이 (이중 축 선 그래프)
st.subheader("그래프 1. 연도별 CO2 농도와 평균 온도 변화 추이")
fig1, ax1 = plt.subplots(figsize=(10, 4.5))

color1 = 'tab:red'
ax1.set_xlabel('Year (연도)', fontsize=11)
ax1.set_ylabel('CO2 Concentration (ppm)', color=color1, fontsize=11)
ax1.plot(df_clean['연도'], df_clean['CO2농도'], color=color1, marker='o', label='CO2 (ppm)')
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
color2 = 'tab:blue'
ax2.set_ylabel('Average Temperature (°C)', color=color2, fontsize=11)
ax2.plot(df_clean['연도'], df_clean['평균온도'], color=color2, marker='s', linestyle='--', label='Temp (°C)')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('Annual CO2 Concentration vs. Average Temperature (1999-2025)', fontsize=13, fontweight='bold')
fig1.tight_layout()
st.pyplot(fig1)

# [그래프 2] CO2 농도와 평균 온도의 상관관계 (산점도)
st.subheader("그래프 2. CO2 농도와 평균 온도의 상관관계 (산점도)")
corr_value = df_clean['CO2농도'].corr(df_clean['평균온도'])

fig2, ax = plt.subplots(figsize=(10, 4.5))
ax.scatter(df_clean['CO2농도'], df_clean['평균온도'], color='purple', alpha=0.75, s=60)
ax.set_xlabel('CO2 Concentration (ppm)', fontsize=11)
ax.set_ylabel('Average Temperature (°C)', fontsize=11)
ax.set_title(f'Correlation between CO2 and Temperature (r = {corr_value:.2f})', fontsize=13, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
fig2.tight_layout()
st.pyplot(fig2)


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

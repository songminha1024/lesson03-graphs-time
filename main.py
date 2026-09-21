
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 페이지 설정
# ==========================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("일별 박스오피스 데이터를 통해 영화의 시간에 따른 변화를 살펴봅니다.")

# ==========================================
# 데이터 불러오기 및 전처리
# ==========================================
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/"
    "modudata/main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 열 이름 앞뒤 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 열을 문자열로 변환한 뒤 실제 날짜 자료형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.strip(),
        format="%Y%m%d",
        errors="coerce"
    )

    # 날짜 변환에 실패한 행 제거
    df = df.dropna(subset=["날짜"]).copy()

    # 관객수와 순위 등 숫자 열 변환
    numeric_cols = [
        "순위", "일관객", "누적관객", "스크린수", "상영횟수"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 영화명 결측치 제거
    df = df.dropna(subset=["영화명"])

    return df


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# ==========================================
# 데이터 요약
# ==========================================
st.info(
    f"총 {len(df):,}개의 기록 | "
    f"{df['날짜'].min():%Y-%m-%d} ~ {df['날짜'].max():%Y-%m-%d}"
)

# ==========================================
# 그래프 1. 영화별 일관객 변화
# ==========================================
st.header("그래프 1. 영화별 일관객 변화")

st.markdown(
    "영화를 선택하여 날짜에 따른 일관객 수의 변화를 확인해 보세요."
)

# 드롭다운으로 영화 선택
movie_list = sorted(df["영화명"].unique().tolist())

selected_movie = st.selectbox(
    "영화 선택",
    movie_list,
    key="movie_select"
)

# 선택한 영화의 데이터 추출
movie_df = df[df["영화명"] == selected_movie].copy()

# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")

# Plotly 선 그래프 생성
fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수 (명)"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
    }
)

fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>"
                  "일관객: %{y:,.0f}명<extra></extra>"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)"
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 문구
st.markdown("**이 그래프로 알 수 있는 것**")
st.write(
    "선택한 영화의 날짜별 일관객 변화를 비교하여 "
    "관객 수가 증가하거나 감소하는 시점을 파악할 수 있다."
)

# ==========================================
# 그래프 2. 추가 예정
# ==========================================
st.divider()
st.header("그래프 2. 추가 예정")
st.caption("앞으로 새로운 시간 관련 그래프를 추가할 공간입니다.")

# ==========================================
# 그래프 3. 추가 예정
# ==========================================
st.divider()
st.header("그래프 3. 추가 예정")
st.caption("앞으로 새로운 시간 관련 그래프를 추가할 공간입니다.")

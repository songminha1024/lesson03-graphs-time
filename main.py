
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
    df.columns = df.columns.str.strip()

    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.strip(),
        format="%Y%m%d",
        errors="coerce"
    )

    df = df.dropna(subset=["날짜"]).copy()

    numeric_cols = [
        "순위", "일관객", "누적관객", "스크린수", "상영횟수"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["영화명", "일관객"])

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
    f"{df['날짜'].min():%Y-%m-%d} ~ "
    f"{df['날짜'].max():%Y-%m-%d}"
)


# ==========================================
# 그래프 1. 영화별 일관객 변화
# ==========================================
st.header("그래프 1. 영화별 일관객 변화")

st.markdown(
    "영화를 선택하여 날짜에 따른 일관객 수의 변화를 확인해 보세요."
)

movie_list = sorted(df["영화명"].unique().tolist())

selected_movie = st.selectbox(
    "영화 선택",
    movie_list,
    key="movie_select"
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수 (명)"
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

st.markdown("**이 그래프로 알 수 있는 것**")
st.write(
    "선택한 영화의 날짜별 일관객 변화를 비교하여 "
    "관객 수가 증가하거나 감소하는 시점을 파악할 수 있다."
)


# ==========================================
# 그래프 2. 일관객 합계 상위 5편 비교
# ==========================================
st.divider()
st.header("그래프 2. 일관객 합계 상위 5편의 날짜별 변화")

st.markdown(
    "전체 데이터 기간 동안 일관객 합계가 가장 큰 영화 5편의 "
    "날짜별 관객 수를 비교합니다."
)

movie_totals = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .rename(columns={"일관객": "기간 내 일관객 합계"})
)

top5_movies = (
    movie_totals
    .nlargest(5, "기간 내 일관객 합계")["영화명"]
    .tolist()
)

top5_df = df[df["영화명"].isin(top5_movies)].copy()
top5_df = top5_df.sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="기간 내 일관객 합계 상위 5편",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수 (명)",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>"
                  "날짜: %{x|%Y-%m-%d}<br>"
                  "일관객: %{y:,.0f}명<extra></extra>"
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",
    legend_title="영화 (클릭하여 표시/숨기기)"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.write(
    "기간 내 일관객 합계가 큰 5편의 날짜별 관객 변화를 비교하여 "
    "영화별 흥행 추세와 관객 수 변동 시점의 차이를 파악할 수 있다."
)


# ==========================================
# 그래프 3. 날짜별 박스오피스 10위권 총 일관객
# ==========================================
st.divider()
st.header("그래프 3. 날짜별 박스오피스 10위권 총 일관객")

st.markdown(
    "매일 박스오피스 10위권에 오른 영화들의 일관객을 합산하여 "
    "전체 관객 규모의 시간에 따른 변화를 살펴봅니다."
)

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .rename(columns={"일관객": "총 일관객"})
    .sort_values("날짜")
)

top3_days = daily_total.nlargest(3, "총 일관객").copy()
top3_days["날짜 라벨"] = top3_days["날짜"].dt.strftime("%Y-%m-%d")

fig3 = px.area(
    daily_total,
    x="날짜",
    y="총 일관객",
    title="날짜별 박스오피스 10위권 총 일관객",
    labels={
        "날짜": "날짜",
        "총 일관객": "총 일관객 수 (명)"
    }
)

fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["총 일관객"],
    mode="markers+text",
    text=top3_days["날짜 라벨"],
    textposition="top center",
    marker=dict(size=10, color="red"),
    name="관객 합계 상위 3일",
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "총 일관객: %{y:,.0f}명<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="총 일관객 수 (명)",
    hovermode="x unified"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.write(
    "날짜별 박스오피스 10위권의 총 일관객 변화를 통해 "
    "전체 영화 관람 규모의 추세와 관객이 집중된 날짜를 파악할 수 있다."
)


# ==========================================
# 그래프 4. 기간 내 일관객 합계 TOP 10
# ==========================================
st.divider()
st.header("그래프 4. 기간 내 일관객 합계 TOP 10")

st.markdown(
    "전체 데이터 기간 동안 영화별 일관객 합계를 계산하여 "
    "관객 수가 가장 많았던 영화 10편을 비교합니다."
)

# 영화별 일관객 합계와 10위권에 든 날짜 수 계산
movie_summary = (
    df.groupby("영화명")
    .agg(
        기간_일관객_합계=("일관객", "sum"),
        **{"10위권_날짜수": ("날짜", "nunique")}
    )
    .reset_index()
)

# 일관객 합계 기준 TOP 10 선정
top10_df = (
    movie_summary
    .nlargest(10, "기간_일관객_합계")
    .sort_values("기간_일관객_합계", ascending=False)
    .copy()
)

# 가로 막대그래프 생성
fig4 = px.bar(
    top10_df,
    x="기간_일관객_합계",
    y="영화명",
    orientation="h",
    title="영화별 기간 내 일관객 합계 TOP 10",
    labels={
        "영화명": "영화",
        "기간_일관객_합계": "기간 내 일관객 합계 (명)"
    },
    custom_data=["10위권_날짜수"],
    text="기간_일관객_합계"
)

# 관객이 많은 영화가 위에 오도록 정렬
fig4.update_yaxes(autorange="reversed")

# 막대 위에 관객 합계 표시 및 마우스 오버 정보 설정
fig4.update_traces(
    texttemplate="%{x:,.0f}명",
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "영화: %{y}<br>"
        "기간 내 일관객 합계: %{x:,.0f}명<br>"
        "10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="기간 내 일관객 합계 (명)",
    yaxis_title="영화",
    showlegend=False
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.write(
    "영화별 기간 내 일관객 합계와 10위권에 든 날수를 비교하여 "
    "전체 흥행 규모와 박스오피스 상위권 유지 기간의 차이를 파악할 수 있다."
)


# ==========================================
# 그래프 5. 추가 예정
# ==========================================
st.divider()
st.header("그래프 5. 추가 예정")
st.caption("앞으로 새로운 시간 관련 그래프를 추가할 공간입니다.")

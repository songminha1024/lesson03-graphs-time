
# ==========================================
# 그래프 5. 월 × 요일별 일관객 히트맵
# ==========================================
st.divider()
st.header("그래프 5. 월 × 요일별 일관객 히트맵")

st.markdown(
    "월과 요일에 따라 박스오피스 10위권의 일관객 합계가 "
    "어떻게 달라지는지 히트맵으로 살펴봅니다."
)

# 월요일부터 일요일까지 요일 순서 지정
weekday_order = [
    "월요일", "화요일", "수요일", "목요일",
    "금요일", "토요일", "일요일"
]

# 날짜에서 월과 요일 추출
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month
heatmap_df["요일번호"] = heatmap_df["날짜"].dt.dayofweek
heatmap_df["요일"] = heatmap_df["요일번호"].map(
    dict(enumerate(weekday_order))
)

# 월 × 요일별 일관객 합계 계산
heatmap_data = (
    heatmap_df
    .pivot_table(
        index="월",
        columns="요일",
        values="일관객",
        aggfunc="sum",
        fill_value=0
    )
    .reindex(
        index=range(1, 13),
        columns=weekday_order,
        fill_value=0
    )
)

# 히트맵 생성
fig5 = px.imshow(
    heatmap_data,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계 (명)"
    },
    x=weekday_order,
    y=[f"{m}월" for m in range(1, 13)],
    color_continuous_scale="YlOrRd",
    aspect="auto",
    title="월 × 요일별 박스오피스 10위권 일관객 합계",
    text_auto=",.0f"
)

fig5.update_traces(
    hovertemplate=(
        "월: %{y}<br>"
        "요일: %{x}<br>"
        "일관객 합계: %{z:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar_title="일관객 합계 (명)"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.write(
    "월과 요일에 따른 박스오피스 10위권의 일관객 합계를 비교하여 "
    "관객이 집중되는 시기의 계절적·요일별 경향을 파악할 수 있다."
)


# ==========================================
# 그래프 6. 추가 예정
# ==========================================
st.divider()
st.header("그래프 6. 추가 예정")
st.caption("앞으로 새로운 시간 관련 그래프를 추가할 공간입니다.")

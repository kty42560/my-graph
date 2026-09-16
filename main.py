# ========================================
# 그래프 5 - 월 × 요일별 일관객 합계 히트맵
# ========================================
st.divider()

st.header("그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "날짜에서 월과 요일을 뽑아 월요일부터 일요일까지의 "
    "요일별 일관객 합계를 비교합니다."
)

# 날짜에서 월과 요일 추출
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

# 요일 이름 지정
weekday_names = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일"
}

heatmap_df["요일"] = heatmap_df["날짜"].dt.dayofweek.map(weekday_names)

# 월 × 요일별 일관객 합계
heatmap_data = (
    heatmap_df
    .groupby(["월", "요일"])["일관객"]
    .sum()
    .reset_index()
)

# 요일 순서 지정
weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_data["요일"] = pd.Categorical(
    heatmap_data["요일"],
    categories=weekday_order,
    ordered=True
)

heatmap_data = heatmap_data.sort_values(["월", "요일"])

# 히트맵
fig5 = px.density_heatmap(
    heatmap_data,
    x="요일",
    y="월",
    z="일관객",
    category_orders={
        "요일": weekday_order,
        "월": list(range(1, 13))
    },
    color_continuous_scale="Blues",
    text_auto=".3s",
    title="월 × 요일별 10위권 일관객 합계",
    labels={
        "요일": "요일",
        "월": "월",
        "일관객": "일관객 합계"
    }
)

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>일관객 합계: %{z:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar_title="일관객"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 직접 작성하세요.")


# ========================================
# 그래프 6 - 다음 그래프를 위한 구역
# ========================================
st.divider()

st.header("그래프 6")
st.write("다음 그래프를 추가할 공간입니다.")

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 내용을 작성하세요.")

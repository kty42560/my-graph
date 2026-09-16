import streamlit as st
import pandas as pd
import plotly.express as px


# ----------------------------------------
# 페이지 설정
# ----------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")
st.write("영화 데이터를 시간의 흐름에 따라 살펴봅니다.")


# ----------------------------------------
# 데이터 불러오기
# ----------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자 열을 숫자형으로 변환
    for col in ["일관객", "누적관객", "스크린수", "상영횟수"]:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df


df = load_data()


# ========================================
# 그래프 1
# 영화별 날짜별 일관객 변화
# ========================================
st.header("그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화의 날짜별 일관객 수 변화를 볼 수 있습니다."
)

movie_list = sorted(
    df["영화명"].dropna().unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
)

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie} - 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info(
    "여기에 이 그래프로 알 수 있는 내용을 직접 작성하세요."
)


# ========================================
# 그래프 2
# 일관객 합계가 가장 큰 영화 5편
# ========================================
st.divider()

st.header("그래프 2. 일관객 합계가 가장 큰 영화 5편")

st.write(
    "전체 기간의 일관객 합계를 기준으로 상위 5편을 골라 "
    "날짜별 일관객 변화를 비교합니다."
)

# 영화별 일관객 합계
movie_totals = (
    df.groupby(
        "영화명",
        as_index=False
    )["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
)

# 상위 5편
top5_movies = (
    movie_totals
    .head(5)["영화명"]
    .tolist()
)

# 상위 5편의 날짜별 데이터
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = (
    top5_df
    .groupby(
        ["날짜", "영화명"],
        as_index=False
    )["일관객"]
    .sum()
    .sort_values("날짜")
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info(
    "여기에 이 그래프로 알 수 있는 내용을 직접 작성하세요."
)


# ========================================
# 그래프 3
# 날짜별 10위권 일관객 합계
# ========================================
st.divider()

st.header("그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜의 10위권 영화 일관객을 모두 더해 "
    "날짜별 전체 관객 규모의 변화를 살펴봅니다."
)

# 날짜별 10위권 일관객 합계
daily_total = (
    df.groupby(
        "날짜",
        as_index=False
    )["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 3일
top3_days = daily_total.nlargest(
    3,
    "일관객"
)

# 영역 그래프
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)

fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)

# 합계가 가장 큰 3일 표시
for _, row in top3_days.iterrows():

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"{row['날짜'].strftime('%Y-%m-%d')}"
            f"<br>{row['일관객']:,}명"
        ),
        showarrow=True,
        arrowhead=2,
        yshift=10
    )

fig3.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계 (명)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info(
    "여기에 이 그래프를 보고 알 수 있는 내용을 직접 작성하세요."
)


# ========================================
# 그래프 4
# 영화별 기간 일관객 TOP 10
# ========================================
st.divider()

st.header("그래프 4. 영화별 기간 일관객 TOP 10")

st.write(
    "이 기간 동안 영화별 일관객을 모두 더해 "
    "관객이 가장 많았던 영화 10편을 비교합니다."
)

# ----------------------------------------
# 영화별 일관객 합계와 10위권에 든 날수
# ----------------------------------------
movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        top10_days=("날짜", "nunique"),
    )
    .reset_index()
)

# 일관객 합계가 많은 순서로 TOP 10
top10_movies = (
    movie_summary
    .sort_values(
        "일관객합계",
        ascending=False
    )
    .head(10)
    .sort_values(
        "일관객합계",
        ascending=True
    )
)

# 가로 막대그래프
fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="영화별 기간 일관객 TOP 10",
    labels={
        "일관객합계": "기간 일관객 합계",
        "영화명": "영화"
    },
    custom_data=["top10_days"]
)

# 마우스를 올렸을 때 표시되는 정보
fig4.update_traces(
    hovertemplate=(
        "영화: %{y}"
        "<br>기간 일관객 합계: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="기간 일관객 합계 (명)",
    yaxis_title="영화"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info(
    "여기에 이 그래프를 보고 알 수 있는 내용을 직접 작성하세요."
)


# ========================================
# 그래프 5
# 월 × 요일별 일관객 합계 히트맵
# ========================================
st.divider()

st.header("그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "날짜에서 월과 요일을 뽑아 "
    "월별·요일별 10위권 일관객 합계를 비교합니다."
)

# 날짜에서 월 추출
heatmap_df = df.copy()

heatmap_df["월"] = (
    heatmap_df["날짜"].dt.month
)

# 요일 이름
weekday_names = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일"
}

heatmap_df["요일"] = (
    heatmap_df["날짜"]
    .dt.dayofweek
    .map(weekday_names)
)

# 월 × 요일별 일관객 합계
heatmap_data = (
    heatmap_df
    .groupby(
        ["월", "요일"]
    )["일관객"]
    .sum()
    .reset_index()
)

# 요일 순서
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

heatmap_data = heatmap_data.sort_values(
    ["월", "요일"]
)

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

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info(
    "여기에 이 그래프를 보고 알 수 있는 내용을 직접 작성하세요."
)


# ========================================
# 그래프 6
# 다음 그래프를 위한 공간
# ========================================
st.divider()

st.header("그래프 6")

st.write(
    "다음 그래프를 추가할 공간입니다."
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info(
    "여기에 내용을 작성하세요."
)

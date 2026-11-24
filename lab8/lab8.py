
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS

st.set_page_config(
    page_title="Lab 8 | Feedback",
    layout="wide"
)

# ==========================================
# 1. SAMPLE DATA
# ==========================================

reviews = [
    "The bottle keeps my water cold all day.",
    "Great size and easy to carry to class.",
    "I love the simple design and sturdy lid.",
    "It leaks in my bag. Very disappointing.",
    "The cap is hard to open and the bottle feels heavy.",
    "Good value, but cleaning the narrow opening is difficult.",
    "Keeps drinks cold, though the paint scratches easily.",
    "The bottle is fine. Nothing special either way.",
    "I expected better insulation for this price.",
    "Lightweight, useful, and easy to wash.",
    "Not bad, but I would prefer a larger capacity.",
    "Excellent bottle. I use it every day.",
    "The lid broke after one week. Poor quality.",
    "It works as described and arrived on time.",
    "Nice color, but it does not keep drinks cold.",
    "Affordable and practical for carrying water.",
    "The bottle is okay; the handle is uncomfortable.",
    "Very happy with the purchase and the quality."
]

topics = [
    "Insulation",
    "Portability",
    "Lid",
    "Leakage",
    "Lid",
    "Cleaning",
    "Durability",
    "General",
    "Insulation",
    "Cleaning",
    "Capacity",
    "General",
    "Lid",
    "Delivery",
    "Insulation",
    "Price",
    "Portability",
    "Quality"
]

df = pd.DataFrame({
    "id": [f"R{i:02}" for i in range(1, 19)],
    "text": reviews,
    "topic": topics
})

# ==========================================
# 2. SENTIMENT CLASSIFICATION
# ==========================================

analyzer = SentimentIntensityAnalyzer()

def label_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "Positive", score

    if score <= -0.05:
        return "Negative", score

    return "Neutral", score


df[["sentiment", "compound"]] = df["text"].apply(
    lambda text: pd.Series(label_sentiment(text))
)

# ==========================================
# 3. DASHBOARD HEADER
# ==========================================

st.title("Product Feedback: A Text Summary")

st.caption(
    "Fictional practice data. Automated sentiment labels "
    "require human review."
)

positive = len(df[df["sentiment"] == "Positive"])
neutral = len(df[df["sentiment"] == "Neutral"])
negative = len(df[df["sentiment"] == "Negative"])

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Reviews", len(df))
c2.metric("Positive", positive)
c3.metric("Neutral", neutral)
c4.metric("Negative", negative)

# ==========================================
# 4. SENTIMENT COUNT CHART
# ==========================================

left, right = st.columns(2)

with left:

    st.subheader("Comment Counts by Sentiment")

    order = ["Positive", "Neutral", "Negative"]

    counts = df["sentiment"].value_counts().reindex(
        order, fill_value=0
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))

    bars = ax.barh(
        counts.index,
        counts.values,
        color=["#4CAF50", "#9E9E9E", "#F44336"]
    )

    ax.bar_label(bars, padding=3)
    ax.set_xlabel("Number of Comments")
    ax.set_xlim(0, max(counts.values) + 2)
    ax.invert_yaxis()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# ==========================================
# 5. WORD CLOUD
# ==========================================

with right:

    st.subheader("Words Used in the Comments")

    stop_words = set(STOPWORDS) | {
        "bottle", "drinks", "drink", "water"
    }

    # Retain a useful product-related term
    stop_words.discard("cold")

    cloud = WordCloud(
        width=900,
        height=500,
        background_color="white",
        colormap="viridis",
        stopwords=stop_words,
        collocations=False,
        random_state=42
    ).generate(" ".join(df["text"]))

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.imshow(cloud, interpolation="bilinear")
    ax.axis("off")

    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Larger words appear more frequently. "
        "Word size, color and position do not indicate sentiment."
    )

# ==========================================
# 6. ORIGINAL COMMENTS
# ==========================================

st.subheader("Review the Original Comments")

selected_sentiment = st.selectbox(
    "Filter by Sentiment",
    ["All", "Positive", "Neutral", "Negative"]
)

if selected_sentiment == "All":
    filtered_df = df
else:
    filtered_df = df[
        df["sentiment"] == selected_sentiment
    ]

st.dataframe(
    filtered_df[
        ["id", "text", "topic", "sentiment", "compound"]
    ],
    use_container_width=True,
    hide_index=True
)

st.caption(
    "A compound score is a model output, "
    "not a confidence rating."
)

# ==========================================
# 7. SENTIMENT COMPARISON BY TOPIC
# ==========================================

st.subheader("Sentiment Comparison by Topic")

topic_counts = pd.crosstab(
    df["topic"],
    df["sentiment"]
).reindex(
    columns=["Positive", "Neutral", "Negative"],
    fill_value=0
)

fig, ax = plt.subplots(figsize=(10, 5))

topic_counts.plot(
    kind="barh",
    stacked=True,
    color=["#4CAF50", "#9E9E9E", "#F44336"],
    ax=ax
)

ax.set_xlabel("Number of Comments")
ax.set_ylabel("Product Topic")
ax.legend(title="Sentiment")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

st.caption(
    "The sample contains only 18 comments. "
    "Some topics have very few reviews, so comparisons "
    "should not be generalized."
)

# ==========================================
# 8. MANUAL SENTIMENT AUDIT
# ==========================================

st.subheader("Manual Sentiment Audit")

st.write(
    "Review two comments from each sentiment category "
    "where available."
)

audit_frames = []

for sentiment in ["Positive", "Neutral", "Negative"]:

    subset = df[df["sentiment"] == sentiment]

    audit_frames.append(subset.head(2))

    if len(subset) < 2:
        st.info(
            f"Only {len(subset)} {sentiment.lower()} "
            "comment(s) are available for review."
        )

audit_df = pd.concat(audit_frames)[
    ["id", "text", "sentiment", "compound"]
].copy()

audit_df["Manual Assessment"] = "Not reviewed"

edited_audit = st.data_editor(
    audit_df,
    hide_index=True,
    use_container_width=True,
    disabled=["id", "text", "sentiment", "compound"],
    column_config={
        "Manual Assessment": st.column_config.SelectboxColumn(
            "Manual Assessment",
            options=[
                "Not reviewed",
                "Reasonable",
                "Borderline",
                "Incorrect"
            ],
            required=True
        )
    }
)

# ==========================================
# 9. NEGATION TEST
# ==========================================

st.subheader("Negation Test")

original_text = "The bottle is easy to clean."
modified_text = "The bottle is not easy to clean."

original_label, original_score = label_sentiment(
    original_text
)

modified_label, modified_score = label_sentiment(
    modified_text
)

negation_df = pd.DataFrame({
    "Comment": [original_text, modified_text],
    "Sentiment": [original_label, modified_label],
    "Compound Score": [original_score, modified_score]
})

st.dataframe(
    negation_df,
    use_container_width=True,
    hide_index=True
)

st.write(
    "This comparison demonstrates how negation can "
    "affect automated sentiment classification."
)

# ==========================================
# 10. INTERACTIVE SENTIMENT TEST
# ==========================================

st.subheader("Test Your Own Comment")

user_text = st.text_area(
    "Enter a product review:"
)

if st.button("Analyze Sentiment"):

    if user_text.strip():

        label, score = label_sentiment(user_text)

        st.write(f"Sentiment: **{label}**")
        st.write(f"Compound Score: **{score:.4f}**")

    else:
        st.warning("Please enter a comment.")

st.caption(
    "Data source: Lab 8 fictional product reviews (2026)."
)

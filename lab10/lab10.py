
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Lab 10 | Data Story",
    layout="wide"
)

# ==========================================
# 2. ORIGINAL DATASET
# ==========================================

skills = [
    "Data storytelling",
    "Python",
    "Chart selection",
    "Color and labels",
    "Data cleaning"
]

original_ratings = [2.4, 3.0, 3.2, 3.7, 4.1]

# ==========================================
# 3. SIDEBAR SETTINGS
# ==========================================

st.sidebar.header("Customize the Data Story")

audience = st.sidebar.selectbox(
    "Select Target Audience",
    [
        "Students",
        "Workshop Instructor",
        "Department Manager"
    ]
)

highlight_method = st.sidebar.radio(
    "Highlighting Method",
    [
        "Contrasting Color",
        "Text Annotation",
        "Position"
    ]
)

st.sidebar.subheader("Modify Skill Ratings")

ratings = []

for skill, rating in zip(skills, original_ratings):

    new_rating = st.sidebar.slider(
        skill,
        min_value=1.0,
        max_value=5.0,
        value=rating,
        step=0.1
    )

    ratings.append(new_rating)

# ==========================================
# 4. PREPARE DATA
# ==========================================

df = pd.DataFrame({
    "Skill": skills,
    "Average rating": ratings
})

lowest_rating = df["Average rating"].min()

lowest_skills = df.loc[
    df["Average rating"] == lowest_rating,
    "Skill"
].tolist()

lowest_skill = lowest_skills[0]

# ==========================================
# 5. AUDIENCE AND PURPOSE
# ==========================================

if audience == "Students":

    title = "Plan a Workshop Around Students' Needs"

    purpose = (
        "Help students identify which data visualization "
        "skill needs the most improvement."
    )

    takeaway = (
        f"Focus on improving {lowest_skill.lower()} "
        "in the next workshop."
    )

elif audience == "Workshop Instructor":

    title = "Identify the Priority Topic for the Next Workshop"

    purpose = (
        "Help the instructor prioritize workshop content "
        "based on students' self-rated skills."
    )

    takeaway = (
        f"Prioritize {lowest_skill.lower()} "
        "when planning the next workshop."
    )

else:

    title = "Identify Student Training Priorities"

    purpose = (
        "Support department decisions about training "
        "and learning resources."
    )

    takeaway = (
        f"Prioritize training resources for "
        f"{lowest_skill.lower()}."
    )

if len(lowest_skills) > 1:
    takeaway = (
        "The following skills share the lowest rating: "
        + ", ".join(lowest_skills)
        + ". Consider all of them when planning training."
    )

# ==========================================
# 6. DASHBOARD HEADER
# ==========================================

st.title(title)

st.write(f"**Audience:** {audience}")
st.write(f"**Purpose:** {purpose}")

st.info(f"Key Takeaway: {takeaway}")

# ==========================================
# 7. CHART PREPARATION
# ==========================================

chart_data = df.copy()

if highlight_method == "Position":

    chart_data = chart_data.sort_values(
        "Average rating",
        ascending=True
    )

fig, ax = plt.subplots(figsize=(10, 5))

# ==========================================
# 8. HIGHLIGHTING METHODS
# ==========================================

if highlight_method == "Contrasting Color":

    colors = [
        "#E07A3F" if skill == lowest_skill
        else "#4C78A8"
        for skill in chart_data["Skill"]
    ]

else:

    colors = ["#4C78A8"] * len(chart_data)

bars = ax.barh(
    chart_data["Skill"],
    chart_data["Average rating"],
    color=colors
)

# ==========================================
# 9. CHART DESIGN
# ==========================================

ax.set_xlim(0, 5.6)

ax.set_xticks(range(0, 6))

ax.set_xlabel(
    "Average self-rating "
    "(1 = beginner, 5 = confident)"
)

if len(lowest_skills) == 1:

    ax.set_title(
        f"{lowest_skill} received the lowest average rating",
        fontsize=14,
        fontweight="bold"
    )

else:

    ax.set_title(
        "Multiple skills share the lowest average rating",
        fontsize=14,
        fontweight="bold"
    )

ax.invert_yaxis()

# Remove unnecessary borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Light horizontal comparison grid
ax.grid(
    axis="x",
    color="#DDDDDD",
    linewidth=0.7
)

ax.set_axisbelow(True)
ax.tick_params(axis="both", length=0)

# ==========================================
# 10. VALUE LABELS AND ANNOTATION
# ==========================================

for bar, skill, value in zip(
    bars,
    chart_data["Skill"],
    chart_data["Average rating"]
):

    label = f"{value:.1f}"

    if (
        highlight_method == "Text Annotation"
        and skill == lowest_skill
    ):

        label += " (Lowest)"

    ax.text(
        value + 0.05,
        bar.get_y() + bar.get_height() / 2,
        label,
        va="center",
        fontsize=10
    )

fig.tight_layout()

st.pyplot(fig, clear_figure=True)

plt.close(fig)

st.caption(
    "Source: Fictional practice values (2026). "
    "Ratings represent averages on a 1–5 scale."
)

# ==========================================
# 11. EXPLAIN THE GRAPHIC
# ==========================================

st.subheader("Understanding the Graphic")

with st.expander("Five Questions About the Graphic"):

    st.markdown(f"""
    **1. What do the axes mean?**

    The vertical axis represents data visualization
    skills, while the horizontal axis represents
    average self-ratings.

    **2. What do the encodings mean?**

    Bar length represents the average rating.
    The selected highlighting method directs
    attention to the lowest-rated skill.

    **3. What level of detail is shown?**

    The values represent average ratings,
    not individual student responses.

    **4. Which data points should the audience notice?**

    The lowest-rated skill is {lowest_skill},
    with an average rating of {lowest_rating:.1f}.

    **5. What is the key takeaway?**

    {takeaway}
    """)

# ==========================================
# 12. ORIGINAL AND MODIFIED DATA
# ==========================================

with st.expander("View Original and Modified Ratings"):

    comparison = pd.DataFrame({
        "Skill": skills,
        "Original Rating": original_ratings,
        "Modified Rating": ratings
    })

    st.dataframe(
        comparison,
        hide_index=True,
        use_container_width=True
    )

# ==========================================
# 13. AUDIENCE FEEDBACK
# ==========================================

st.subheader("Evaluate Audience Understanding")

st.write(
    "Ask a classmate to interpret the chart "
    "without reading the takeaway aloud."
)

with st.form("audience_feedback"):

    axes_response = st.text_area(
        "What do the axes and bar lengths represent?"
    )

    highlight_response = st.text_area(
        "What does the highlighted value mean?"
    )

    takeaway_response = st.text_area(
        "What is the main message of the chart?"
    )

    understood = st.text_area(
        "One point the audience understood"
    )

    unclear = st.text_area(
        "One point that was unclear"
    )

    revision = st.text_area(
        "Change made after receiving feedback"
    )

    submitted = st.form_submit_button(
        "Record Feedback"
    )

if submitted:

    st.success("Feedback recorded for this session.")

    feedback = pd.DataFrame({
        "Evaluation": [
            "Understanding of axes",
            "Understanding of highlight",
            "Main takeaway",
            "Point understood",
            "Unclear point",
            "Revision"
        ],
        "Response": [
            axes_response,
            highlight_response,
            takeaway_response,
            understood,
            unclear,
            revision
        ]
    })

    st.dataframe(
        feedback,
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "Download Audience Feedback",
        feedback.to_csv(index=False),
        file_name="lab10_feedback.csv",
        mime="text/csv"
    )

st.caption(
    "Educational exercise: Framing the Data Story."
)

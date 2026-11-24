
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Lab 9 | Chart Design",
    layout="wide"
)

# ==========================================
# 2. DATASET
# ==========================================

data = pd.DataFrame({
    "Branch": [
        "North", "South", "East",
        "West", "Central", "Northeast"
    ],
    "Sales": [96, 99, 98, 100, 97, 98]
})

# Replace with your name
author = "Your Name"

# ==========================================
# 3. STREAMLIT INTERFACE
# ==========================================

st.title("Designing a Clearer Bar Chart")

st.caption(
    "Comparing cluttered and improved visualizations "
    "using the same sales data."
)

version = st.radio(
    "Choose a chart",
    ["Cluttered", "Improved"],
    horizontal=True
)

show_all = st.checkbox(
    "Include two additional branches",
    value=True
)

if show_all:
    chart_data = data.copy()
else:
    chart_data = data.iloc[:4].copy()

fig, ax = plt.subplots(figsize=(10, 5))

# ==========================================
# 4. CLUTTERED CHART
# ==========================================

if version == "Cluttered":

    colors = [
        "#8FB9A8",
        "#D8B365",
        "#B2ABD2",
        "#5E3C99",
        "#FF6961",
        "#77DD77"
    ]

    bars = ax.bar(
        chart_data["Branch"],
        chart_data["Sales"],
        color=colors[:len(chart_data)],
        edgecolor="black",
        linewidth=2
    )

    # Truncated axis exaggerates differences
    ax.set_ylim(95, 101)

    # Unnecessary background decoration
    ax.set_facecolor("#E8E8E8")

    # Excessive gridlines
    ax.grid(
        True,
        which="both",
        color="white",
        linewidth=2
    )

    ax.set_title(
        "SALES PERFORMANCE!!!",
        fontsize=18,
        fontweight="bold"
    )

# ==========================================
# 5. IMPROVED CHART
# ==========================================

else:

    highest_branch = chart_data.loc[
        chart_data["Sales"].idxmax(),
        "Branch"
    ]

    # Highlight only the highest-performing branch
    colors = [
        "#E07A3F" if branch == highest_branch
        else "#4C78A8"
        for branch in chart_data["Branch"]
    ]

    bars = ax.bar(
        chart_data["Branch"],
        chart_data["Sales"],
        color=colors
    )

    # Accurate zero baseline
    ax.set_ylim(0, 110)

    # Natural axis increments
    ax.set_yticks(range(0, 101, 20))

    # Display exact sales values
    ax.bar_label(
        bars,
        fmt="%.0f",
        padding=3
    )

    # Descriptive title
    ax.set_title(
        f"{highest_branch} branch recorded the highest sales",
        fontsize=15,
        fontweight="bold"
    )

    # Subtle horizontal gridlines
    ax.grid(
        axis="y",
        color="#DDDDDD",
        linewidth=0.7
    )

    ax.set_axisbelow(True)

    # Remove unnecessary borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Remove unnecessary tick marks
    ax.tick_params(axis="both", length=0)

# ==========================================
# 6. CHART LABELS AND ATTRIBUTION
# ==========================================

ax.set_ylabel("Sales (units)")

fig.text(
    0.5,
    0.02,
    f"Data: fictional practice values (2026) | Chart: {author}",
    ha="center",
    fontsize=9,
    color="gray"
)

fig.tight_layout(rect=[0, 0.06, 1, 1])

st.pyplot(fig, clear_figure=True)

plt.close(fig)

# ==========================================
# 7. CHART EXPLANATION
# ==========================================

if version == "Cluttered":

    st.warning(
        "The shortened vertical axis exaggerates "
        "small differences between branches."
    )

    st.write("""
    **Problems with this chart:**

    - Truncated vertical axis.
    - Unnecessary background decoration.
    - Excessive gridlines.
    - Inconsistent use of colors.
    - Non-descriptive chart title.
    """)

else:

    st.success(
        "The improved chart uses a zero baseline "
        "and highlights the highest sales value."
    )

    st.write("""
    **Improvements made:**

    - Vertical axis starts at zero.
    - Consistent colors with one accent color.
    - Clear and descriptive title.
    - Exact values displayed above bars.
    - Reduced chartjunk and unnecessary borders.
    - Natural axis increments.
    - Clear source and author attribution.
    """)

# ==========================================
# 8. ORIGINAL DATA
# ==========================================

st.subheader("Original Sales Data")

st.dataframe(
    chart_data,
    hide_index=True,
    use_container_width=True
)

highest = chart_data["Sales"].max()
lowest = chart_data["Sales"].min()

c1, c2, c3 = st.columns(3)

c1.metric("Highest Sales", highest)
c2.metric("Lowest Sales", lowest)
c3.metric("Difference", highest - lowest)

# ==========================================
# 9. DATA INTEGRITY
# ==========================================

st.subheader("Data Integrity")

percentage_difference = (
    (highest - lowest) / lowest
) * 100

st.write(
    f"The highest sales value is only "
    f"{percentage_difference:.2f}% higher "
    f"than the lowest sales value."
)

st.write(
    "Both charts represent the same data, "
    "but their design affects how readers "
    "perceive the differences."
)

st.caption(
    "All sales figures are fictional and "
    "used for educational purposes."
)

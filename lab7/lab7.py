
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Streamlit page configuration
st.set_page_config(
    page_title="Lab 7 - Interactive Map Visualization",
    layout="wide"
)

# Load the Natural Earth dataset
@st.cache_data
def load_data():
    file_path = (
        Path(__file__).parent
        / "ne_110m_admin_0_countries"
        / "ne_110m_admin_0_countries.shp"
    )

    gdf = gpd.read_file(file_path)

    # Standardize column names to lowercase
    gdf.columns = gdf.columns.str.lower()

    if 'pop_est' not in gdf.columns:
        np.random.seed(0)
        gdf['pop_est'] = np.random.randint(
            1000000, 1000000000, size=len(gdf)
        )
        gdf['synthetic_population'] = True
    else:
        gdf['synthetic_population'] = False

    return gdf


gdf = load_data()

# Calculate population density per square kilometre
area_km2 = gdf.to_crs("EPSG:6933").geometry.area / 1e6
gdf['pop_density'] = gdf['pop_est'] / area_km2.replace(0, np.nan)

# Available geographical projections
projection_options = {
    "Plate Carree": "EPSG:4326",
    "Mercator": "EPSG:3395",
    "Robinson": "ESRI:54030",
    "Mollweide": "ESRI:54009",
    "Equal Earth": "EPSG:8857"
}

# Streamlit interface
st.title("Interactive Map Visualization Examples")

st.sidebar.header("Choose a Map Type")

map_type = st.sidebar.radio(
    "Select Map Type",
    [
        "Map Cosmetics",
        "Map Visual Hierarchy",
        "Choropleth Map",
        "Geo Projection"
    ]
)

if gdf['synthetic_population'].any():
    st.warning("Population values are synthetic practice data.")


# ==========================================
# 1. MAP COSMETICS
# ==========================================

if map_type == "Map Cosmetics":

    st.subheader("Map Cosmetics")

    fig, ax = plt.subplots(figsize=(10, 6))

    gdf.plot(
        ax=ax,
        color='skyblue',
        edgecolor='black',
        linewidth=0.5
    )

    ax.set_title(
        "Styled Map Example",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_facecolor("lightgrey")

    st.pyplot(fig)
    plt.close(fig)


# ==========================================
# 2. MAP VISUAL HIERARCHY
# ==========================================

if map_type == "Map Visual Hierarchy":

    st.subheader("Map Visual Hierarchy")

    country_col = 'name'

    countries = sorted(
        gdf[country_col].dropna().unique().tolist()
    )

    default_countries = [
        "Brazil",
        "India",
        "China",
        "Australia",
        "South Africa",
        "Russia"
    ]

    highlighted_countries = st.multiselect(
        "Select countries to highlight in red",
        options=countries,
        default=[
            country for country in default_countries
            if country in countries
        ]
    )

    gdf['color'] = gdf[country_col].apply(
        lambda x: 'red'
        if x in highlighted_countries
        else 'skyblue'
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    gdf.plot(
        color=gdf['color'],
        edgecolor='black',
        linewidth=0.5,
        ax=ax
    )

    ax.set_title(
        "Map Visual Hierarchy with Selected Countries Highlighted"
    )

    st.pyplot(fig)
    plt.close(fig)


# ==========================================
# 3. CHOROPLETH MAP
# ==========================================

if map_type == "Choropleth Map":

    st.subheader("Choropleth Map")

    color_choice = st.selectbox(
        "Choose Color Scheme",
        ['OrRd', 'YlGn', 'Blues', 'Purples', 'Greens'],
        index=0
    )

    use_log_scale = st.checkbox(
        "Use Log Transformation",
        value=True
    )

    if use_log_scale:
        gdf['display_density'] = np.log1p(gdf['pop_density'])
        legend_label = "Log-transformed population density"
    else:
        gdf['display_density'] = gdf['pop_density']
        legend_label = "Population per km²"

    fig, ax = plt.subplots(figsize=(10, 6))

    gdf.plot(
        column='display_density',
        cmap=color_choice,
        edgecolor='black',
        linewidth=0.5,
        legend=True,
        legend_kwds={'label': legend_label},
        ax=ax
    )

    ax.set_title(
        f"Population Density by Country ({color_choice})"
    )

    st.pyplot(fig)
    plt.close(fig)


# ==========================================
# 4. GEO PROJECTION
# ==========================================

if map_type == "Geo Projection":

    st.subheader("Geo Projection")

    proj_choice = st.selectbox(
        "Select a Projection",
        list(projection_options.keys())
    )

    color_choice = st.selectbox(
        "Choose Color Scheme",
        ['OrRd', 'YlGn', 'Blues', 'Purples', 'Greens'],
        index=0
    )

    use_log_scale = st.checkbox(
        "Use Log Transformation for Population Density",
        value=True
    )

    if use_log_scale:
        gdf['display_density'] = np.log1p(gdf['pop_density'])
        legend_label = "Log-transformed population density"
    else:
        gdf['display_density'] = gdf['pop_density']
        legend_label = "Population per km²"

    # Convert geographical projection
    map_data = gdf.copy()

    # Exclude Antarctica in Mercator to avoid polar distortion
    if proj_choice == "Mercator":
        map_data = map_data[map_data['name'] != 'Antarctica']

    gdf_proj = map_data.to_crs(
        projection_options[proj_choice]
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    gdf_proj.plot(
        column='display_density',
        cmap=color_choice,
        edgecolor='black',
        linewidth=0.5,
        legend=True,
        legend_kwds={'label': legend_label},
        ax=ax
    )

    ax.set_title(f"Map in {proj_choice} Projection")

    st.pyplot(fig)
    plt.close(fig)

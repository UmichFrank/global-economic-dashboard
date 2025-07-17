import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Global Economic Indicators Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and cache data
@st.cache_data
def load_data():
    return px.data.gapminder()

# Load data
df = load_data()

# Dashboard title
st.title("🌍 Global Economic Indicators Dashboard")
st.markdown("**Interactive Multi-Visualization Analysis Platform**")

# Sidebar controls
st.sidebar.header("Dashboard Controls")

# Metric selection
metric_options = {
    'Life Expectancy (years)': 'lifeExp',
    'GDP per Capita (USD)': 'gdpPercap',
    'Population': 'pop'
}

selected_metric_label = st.sidebar.selectbox(
    "Select Metric:",
    options=list(metric_options.keys()),
    index=0
)
selected_metric = metric_options[selected_metric_label]

# Year selection
selected_year = st.sidebar.slider(
    "Select Year:",
    min_value=int(df['year'].min()),
    max_value=int(df['year'].max()),
    value=int(df['year'].max()),
    step=5
)

# Filter data
df_filtered = df[df['year'] == selected_year]

# Create dashboard layout
col1, col2 = st.columns(2)

with col1:
    # Scatter plot
    st.subheader(f"📊 {selected_metric_label} vs GDP per Capita ({selected_year})")
    
    scatter_fig = px.scatter(
        df_filtered,
        x='gdpPercap',
        y=selected_metric,
        size='pop',
        color='continent',
        hover_name='country',
        size_max=60,
        title=f'{selected_metric_label} vs GDP per Capita ({selected_year})'
    )
    
    scatter_fig.update_layout(height=400)
    st.plotly_chart(scatter_fig, use_container_width=True)
    
    # Time series
    st.subheader(f"📈 Historical Trends: {selected_metric_label}")
    
    major_countries = ['China', 'United States', 'India', 'Germany', 'Brazil', 'Japan']
    df_trends = df[df['country'].isin(major_countries)]
    
    line_fig = px.line(
        df_trends,
        x='year',
        y=selected_metric,
        color='country',
        title=f'{selected_metric_label} Trends Over Time (1952-2007)',
        markers=True
    )
    
    # Add vertical line for selected year
    line_fig.add_vline(
        x=selected_year,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Selected: {selected_year}"
    )
    
    line_fig.update_layout(height=400)
    st.plotly_chart(line_fig, use_container_width=True)

with col2:
    # Bar chart
    st.subheader(f"🏆 Top 10 Countries by {selected_metric_label} ({selected_year})")
    
    df_top = df_filtered.nlargest(10, selected_metric)
    
    bar_fig = px.bar(
        df_top,
        x=selected_metric,
        y='country',
        color='continent',
        orientation='h',
        title=f'Top 10 Countries by {selected_metric_label} ({selected_year})'
    )
    
    bar_fig.update_layout(height=400)
    st.plotly_chart(bar_fig, use_container_width=True)
    
    # Choropleth map
    st.subheader(f"🗺️ Global Distribution: {selected_metric_label} ({selected_year})")
    
    map_fig = px.choropleth(
        df_filtered,
        locations='iso_alpha',
        color=selected_metric,
        hover_name='country',
        color_continuous_scale='Viridis',
        title=f'Global {selected_metric_label} Distribution ({selected_year})'
    )
    
    map_fig.update_layout(height=400)
    st.plotly_chart(map_fig, use_container_width=True)

# Summary statistics
st.markdown("---")
st.subheader("📊 Summary Statistics")

max_country = df_filtered.loc[df_filtered[selected_metric].idxmax(), 'country']
min_country = df_filtered.loc[df_filtered[selected_metric].idxmin(), 'country']

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Countries",
        value=f"{len(df_filtered)}"
    )

with col2:
    st.metric(
        label="Highest Value",
        value=f"{df_filtered[selected_metric].max():.0f}",
        delta=f"{max_country}"
    )

with col3:
    st.metric(
        label="Lowest Value",
        value=f"{df_filtered[selected_metric].min():.0f}",
        delta=f"{min_country}"
    )

with col4:
    st.metric(
        label="Global Average",
        value=f"{df_filtered[selected_metric].mean():.0f}"
    )

# Information section
st.markdown("---")
st.subheader("ℹ️ About This Dashboard")

st.markdown("""
This interactive dashboard demonstrates multiple visualization techniques working together to explore global economic indicators:

- **Scatter Plot**: Shows relationships between GDP per capita and selected metrics
- **Bar Chart**: Displays top 10 countries for easy comparison
- **Time Series**: Reveals historical trends for major countries
- **World Map**: Provides geographic context and distribution patterns

**Data Source**: Gapminder dataset (1952-2007)  
**Built with**: Streamlit + Plotly  
**Author**: [Your Name]  
**Course**: [Your Course]
""")

# Technical details
with st.expander("🔧 Technical Details"):
    st.markdown("""
    **Libraries Used:**
    - Streamlit: Web app framework
    - Plotly: Interactive visualizations
    - Pandas: Data manipulation
    
    **Features:**
    - Responsive design
    - Interactive controls
    - Real-time updates
    - Cross-visualization coordination
    
    **Deployment:** Streamlit Cloud
    """)

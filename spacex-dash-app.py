import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# LOAD DATA
# =========================
spacex_df = pd.read_csv("spacex_launch_dash.csv")

min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# =========================
# TITLE
# =========================
st.title("SpaceX Launch Records Dashboard")

# =========================
# SIDEBAR INPUTS (équivalent Dash controls)
# =========================
site = st.selectbox(
    "Select a Launch Site",
    options=['ALL', 'CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40']
)

payload_range = st.slider(
    "Payload range (Kg)",
    min_value=int(min_payload),
    max_value=int(max_payload),
    value=(int(min_payload), int(max_payload)),
    step=1000
)

low, high = payload_range

# =========================
# FILTER DATA (global for scatter)
# =========================
df_filtered = spacex_df[
    (spacex_df['Payload Mass (kg)'] >= low) &
    (spacex_df['Payload Mass (kg)'] <= high)
]

if site != 'ALL':
    df_filtered = df_filtered[df_filtered['Launch Site'] == site]

# =========================
# PIE CHART
# =========================
st.subheader("Success Pie Chart")

if site == 'ALL':
    fig_pie = px.pie(
        spacex_df,
        names='Launch Site',
        values='class',
        title='Total Success Launches by Site'
    )
else:
    site_df = spacex_df[spacex_df['Launch Site'] == site]
    fig_pie = px.pie(
        site_df,
        names='class',
        title=f'Success vs Failure for {site}'
    )

st.plotly_chart(fig_pie, use_container_width=True)

# =========================
# SCATTER PLOT
# =========================
st.subheader("Payload vs Success Rate")

fig_scatter = px.scatter(
    df_filtered,
    x='Payload Mass (kg)',
    y='class',
    color='Booster Version Category',
    title='Payload vs Success Rate'
)

st.plotly_chart(fig_scatter, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("spacex_launch_dash.csv")

# =========================
# TITLE
# =========================
st.title("🚀 SpaceX Launch Records Dashboard")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.title("Filters")

sites = ['ALL'] + list(df['Launch Site'].unique())

site = st.sidebar.selectbox("Select Launch Site", sites)

min_payload = int(df['Payload Mass (kg)'].min())
max_payload = int(df['Payload Mass (kg)'].max())

payload_range = st.sidebar.slider(
    "Payload range (Kg)",
    min_value=min_payload,
    max_value=max_payload,
    value=(min_payload, max_payload),
    step=1000
)

low, high = payload_range

# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df['Payload Mass (kg)'] >= low) &
    (df['Payload Mass (kg)'] <= high)
]

if site != 'ALL':
    filtered_df = filtered_df[filtered_df['Launch Site'] == site]

# =========================
# PIE CHART
# =========================
st.subheader("📊 Success Overview")

if site == 'ALL':
    pie_data = df.groupby('Launch Site')['class'].sum().reset_index()

    fig_pie = px.pie(
        pie_data,
        names='Launch Site',
        values='class',
        title='Total Successful Launches by Site'
    )
else:
    site_df = df[df['Launch Site'] == site]
    outcome = site_df['class'].map({1: 'Success', 0: 'Failure'})

    fig_pie = px.pie(
        names=outcome,
        title=f'Success vs Failure for {site}'
    )

st.plotly_chart(fig_pie, use_container_width=True)

# =========================
# SCATTER PLOT
# =========================
st.subheader("📈 Payload vs Success")

fig_scatter = px.scatter(
    filtered_df,
    x='Payload Mass (kg)',
    y='class',
    color='Booster Version Category',
    title='Payload vs Launch Success'
)

st.plotly_chart(fig_scatter, use_container_width=True)
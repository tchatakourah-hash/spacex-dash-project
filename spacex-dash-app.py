import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Payload range
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Create Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # Pie chart
    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    html.P("Payload range (Kg):"),

    # Range slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={0: '0', 10000: '10000'}
    ),

    html.Br(),

    # Scatter plot
    dcc.Graph(id='success-payload-scatter-chart')
])


# =========================
# PIE CHART CALLBACK
# =========================
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(site):

    if site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Success Launches by Site'
        )
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for {site}'
        )
        return fig


# =========================
# SCATTER CALLBACK
# =========================
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(site, payload_range):

    low, high = payload_range

    df_filtered = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if site != 'ALL':
        df_filtered = df_filtered[df_filtered['Launch Site'] == site]

    fig = px.scatter(
        df_filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs Success Rate'
    )

    return fig


# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)
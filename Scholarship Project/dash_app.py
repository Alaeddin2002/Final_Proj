import pandas as pd
import warnings

import json
import urllib.request
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px



df = pd.read_csv('security_incidents.csv')
grouped_df = df.groupby('Country')['Total affected'].sum().reset_index()
grouped_df = grouped_df.sort_values(by='Total affected', ascending=False)
grouped_df.head(10)



bar_chart = px.bar(grouped_df.head(6), x='Country', y='Total affected', title="Total Affected by Country")

scatter_plot = px.scatter(df, x='Year', y='Total affected', color='Country', title="Scatter Plot of Total Affected over Time")



app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Plot Example"),
    html.Div([
        # The bar chart
        dcc.Graph(id='bar-chart', figure=bar_chart),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        # The scatter plot
        dcc.Graph(id='scatter-plot', figure=None),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    # Reset button
    html.Button("Reset", id="reset-button", n_clicks=0),
])

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('bar-chart', 'clickData'),
     Input('reset-button', 'n_clicks')])

def update_scatter_plot(clickData,n_clicks):

    if n_clicks > 0:
        return scatter_plot

    if clickData is not None:
        selected_country = clickData['points'][0]['x']
        filtered_df = df[df['Country'] == selected_country]

        updated_scatter_plot = px.scatter(filtered_df, x='Year', y='Total affected', color='Country', title=f"Scatter Plot for {selected_country}")
        return updated_scatter_plot

    return scatter_plot

if __name__ == '__main__':
    app.run(debug=False, port=8056, use_reloader=False)

    
import dash
from dash import dcc, html
import numpy as np
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('Total Emissions Per Country (2000-2020).csv')
df_new = pd.melt(df,
                 id_vars=['Area', 'Item', 'Element', 'Unit'],
                 value_vars=list(map(str, np.arange(2000, 2021))),
                 var_name='Year',
                 value_name='Total Emissions'
                 )

df_new2 = df_new.dropna()

top_10 = df_new2.groupby(['Area'])['Total Emissions'].agg(
    'sum').sort_values(ascending=False).head(10)

df_agg = df_new2.groupby(['Area', 'Year'])['Total Emissions'].agg('sum')
df_agg = df_agg.reset_index()

top_in_time = df_agg.loc[df_agg['Area'].isin(top_10.index)]

df_new3 = df_new2[['Area', 'Total Emissions']].groupby(['Area']).sum(
).reset_index().sort_values(by='Total Emissions', ascending=False)

df_new4 = df_new2[['Item', 'Total Emissions']].groupby(by=['Item']).sum(
).reset_index().sort_values(by='Total Emissions', ascending=False)

df_new5 = df_new2[['Year', 'Total Emissions']].groupby(
    by=['Year']).sum().reset_index()

df_new6 = df_new2[['Year', 'Element', 'Total Emissions']].groupby(
    by=['Year', 'Element']).sum().reset_index()
# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Green House gases Emissions by Country (2000-2020)"),

    dcc.Graph(
        id='pie_graph',
        figure=px.pie(names=top_10.index, values=top_10.values,
                      title='Total emissions from the largest emitters')
    ),

    dcc.Graph(
        id='line_graph',
        figure=px.line(top_in_time, x="Year", y="Total Emissions",
                       color='Area', title='Top 10 issuers over time')
    ),

    dcc.Graph(
        id='choropleth-map',
        figure=px.choropleth(
            df_new3,
            locations='Area',
            locationmode='country names',
            color='Total Emissions',
            hover_name='Area',
            color_continuous_scale=px.colors.sequential.Plasma,
            title='Total Emissions by Country (2020)'
        )
    ),
    dcc.Graph(
        id='bar-chart',
        figure=px.bar(df_new4, x='Total Emissions', y='Item', orientation='h',
                      title='Total Emissions By Source',
                      color='Item',
                      labels={
                          'Total Emissions': 'Emissions (kilotonnes)', 'Item': 'Source'},
                      template='plotly_white')
    ),

    dcc.Graph(
        id='line-plot',
        figure=px.line(df_new5, x='Year', y='Total Emissions',
                       title='Total Emissions Over The Years',
                       labels={
                           'Total Emissions': 'Emissions (kilotonnes)', 'Year': 'Year'},
                       template='plotly_white',
                       markers=True,  # Show markers on data points
                       line_shape='linear',  # Set line shape
                       color_discrete_sequence=['red']  # Set line color
                       )
    ),
    dcc.Graph(
        id='line-plots',
        figure=px.line(df_new6, x='Year', y='Total Emissions', color='Element',
                       title='Total Emissions Over The Years By Source',
                       labels={
                           'Total Emissions': 'Emissions (kilotonnes)', 'Year': 'Year'},
                       template='plotly_white',
                       markers=True,  # Show markers on data points
                       line_shape='linear',  # Set line shape
                       
                       )
    )


])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

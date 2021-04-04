import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

tab_2_layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Please choose a country', style={ 'text-align': 'center','fontColor': 'white'}), #'background-color': '#000000',
            dropdown_country,
            html.Br(),
            html.H1('Please choose genre(s)', style={'text-align': 'center','fontColor': 'white'}),#'background-color': '#000000', 
            dropdown_genre,
            html.Br(),
            radio_moviedata,
            year_slider
        ], style={'width': '20%', 'background-color': '#8B000000'}, className='box'),

        html.Div([
            html.Br(),
            html.Br(),
            dcc.Graph(id='graph_example'),
        ], style={'width': '80%', 'background-color': '#8B000000'}, className='box'),
            html.Br(),
            html.Br(),

    ], style={'display': 'flex','background-color': '#ADD8E6'}),


    html.Div([
        html.Br(),
        html.Br(),
        html.Div([
            dcc.Graph(id='graph_example2'),
        ], style={'width': '50%', 'background-color': '#8B000000'}, className='box'),

        html.Div([
            dcc.Graph(id='graph_example3'),
        ], style={'width': '50%', 'background-color': '#8B000000'}, className='box'),
  
    ], style={'display': 'flex'}),

])


@app.callback(
    Output('graph_example', 'figure'),
    [Input('country_drop', 'value'),
     Input('genre_drop', 'value'),
     Input('moviedata_radio', 'value'),
     Input('year_slider', 'value')]
)
def update_graph(countries, genres, moviedata, year):
    filtered_by_year_df = df[(df['year'] >= year[0]) & (df['year'] <= year[1])]

    scatter_data = []

    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['country'] == country]
        
    for genre in genres:
        filtered_by_year_and_country_and_genre_df = filtered_by_year_and_country_df.loc[filtered_by_year_and_country_df['genre'] == genre]

        temp_data = dict(
            type='scatter',
            y=filtered_by_year_and_country_and_genre_df[moviedata],
            x=filtered_by_year_and_country_and_genre_df['year'],
            name=country+ genre
        )

        scatter_data.append(temp_data)

    scatter_layout = dict(xaxis=dict(title='Year'),
                          yaxis=dict(title=moviedata)
                          )

    fig = go.Figure(data=scatter_data, layout=scatter_layout)
    
 
    return fig



@app.callback(
    Output('graph_example2', 'figure'),
    [Input('country_drop', 'value'),
     Input('genre_drop', 'value'),
     Input('moviedata_radio', 'value'),
     Input('year_slider', 'value')]
)


def update_graph2(countries,genres, moviedata, year):
    filtered_by_year_df = df[(df['year'] >= year[0]) & (df['year'] <= year[1])]

    scatter_data = []

    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['country'] == country]
        
    for genre in genres:
        filtered_by_year_and_country_and_genre_df = filtered_by_year_and_country_df.loc[filtered_by_year_and_country_df['genre'] == genre]
    

    top10 = filtered_by_year_and_country_and_genre_df.nlargest(10, "gross")
    top10.sort_values("gross", ascending = True, inplace = True)
    
    fig2 = px.bar(top10, x='gross', y='name')

    
    return fig2

@app.callback(
    Output('graph_example3', 'figure'),
    [Input('country_drop', 'value'),
     Input('genre_drop', 'value'),
     Input('moviedata_radio', 'value'),
     Input('year_slider', 'value')]
)

def update_graph3(countries,genres, moviedata, year):
    filtered_by_year_df = df[(df['year'] >= year[0]) & (df['year'] <= year[1])]


    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['country'] == country]
        
    for genre in genres:
        filtered_by_year_and_country_and_genre_df = filtered_by_year_and_country_df.loc[filtered_by_year_and_country_df['genre'] == genre]
    

    top10 = filtered_by_year_and_country_and_genre_df.nlargest(10, "score")
    top10.sort_values("score", ascending = True, inplace = True)
    
    fig3 = px.bar(top10, x='score', y='name')

    
    return fig3

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from app import app

df_II = pd.read_csv('movies.csv',encoding='ISO-8859-1')

df_gp_gross = df_II.groupby(['country', 'genre', 'year'])['gross'].sum().reset_index()
df_gp_score = df_II.groupby(['country', 'genre', 'year'])['score'].mean().reset_index()
df_gp = df_gp_gross.merge(df_gp_score)


country_options = [
    dict(label='Country ' + country, value=country)
    for country in df_II['country'].unique()]

genre_options = [
    dict(label='Genre ' + genre , value=genre)
    for genre in df_II['genre'].unique()]


moviedata_options = [
    {'label': 'Gross Revenue', 'value': 'gross'},
    {'label': 'Score', 'value': 'score'}
]

dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['USA'],
        multi=True
    )


dropdown_genre = dcc.Dropdown(
        id='genre_drop',
        options=genre_options,
        value=['Comedy'],
        multi=True
    )


radio_moviedata = dcc.RadioItems(
        id='moviedata_radio',
        options=moviedata_options,
        value='score',
        labelStyle={'display': 'block'}
    )

year_slider = dcc.RangeSlider(
        id='year_slider',
        min=1986,
        max=2016,
        value=[1986, 2016],
        marks={'1986': '1986',
               '1995': '1995',
               '2000': '2000',
               '2005': '2005',
               '2010': '2010',
               '2016': '2016'},
        step=1
    )


tab_2_layout = html.Div([

    html.H1('Exploring Genres in Movie Industry', style={ 'text-align': 'center','Color': '#228B22'}), #'background-color': '#000000',

    html.Div([
        html.Div([
            html.H1('Please choose 1 country', style={ 'text-align': 'center','fontColor': 'white'}), #'background-color': '#000000',
            dropdown_country,
            html.Br(),
            html.H1('Please choose 1 genre', style={'text-align': 'center','fontColor': 'white'}),#'background-color': '#000000', 
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
def update_graph(countries,genres, moviedata, year):
    
    filtered_by_year_df = df_gp[(df_gp['year'] >= year[0]) & (df_gp['year'] <= year[1])]

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
    filtered_by_year_df = df_II[(df_II['year'] >= year[0]) & (df_II['year'] <= year[1])]

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
    filtered_by_year_df = df_II[(df_II['year'] >= year[0]) & (df_II['year'] <= year[1])]


    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['country'] == country]
        
    for genre in genres:
        filtered_by_year_and_country_and_genre_df = filtered_by_year_and_country_df.loc[filtered_by_year_and_country_df['genre'] == genre]
    
    top10 = filtered_by_year_and_country_and_genre_df.nlargest(10, "score")
    top10.sort_values("score", ascending = True, inplace = True)
    
    fig3 = px.bar(top10, x='score', y='name')

    
    return fig3

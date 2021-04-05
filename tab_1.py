import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from app import app

df = pd.read_csv('movies.csv',encoding='ISO-8859-1')

df.columns = df.columns.str.capitalize()

###################### TAB 1 ############################

tab_1_layout = html.Div([
    html.Div([
        html.Div([
            html.Br(),
            html.Label(['Choose Country and Company:'],style={'font-weight': 'bold', "text-align": "left"}),
            dcc.Dropdown(id = 'country_drop',
                options = [{'label':country, 'value':country} for country in df['Country'].unique()],
                value = 'USA',
                multi = False,
                disabled=False,
                clearable=True,
                searchable=True,
                placeholder='Choose Country...',
                className='form-dropdown',
                style={'width':"90%"},
                persistence='string',
                persistence_type='memory'),
        
            dcc.Dropdown(id = 'company_drop',
                options = [{'label':company, 'value':company} for company in df['Company'].unique()],
                value = 'Paramount Pictures',
                multi = False,
                disabled=False,
                clearable=True,
                searchable=True,
                placeholder='Choose Company..',
                className='form-dropdown',
                style={'width':"90%"},
                persistence='string',
                persistence_type='memory'),
            
            dcc.Dropdown(id= 'genre_drop',
            options = [{'label': genre, 'value' : genre} for genre in df['Genre'].unique()],
            value = 'Drama',
            multi = False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Genre..',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory')            
            ], 
            
            style={'width': '30%', 'background-color': '#8B000000'}, className='box'),
    
        html.Div([
            dcc.Graph(id = 'line_graph'),
            ],style={'width': '70%'}, className='box'),
        
        ], style={'display': 'flex', 
                 'background-image':'url(https://st3.idealista.pt/news/arquivos/styles/news_detail/public/2020-07/denise-jans-oavjqz-nfd0-unsplash.jpg?sv=JkD9EvJB&itok=UiyQ_mjj)'}
        ),
    
    html.Br(),
    
    html.Div([

        html.Br(),
    
        html.Div([
            html.Div([
                html.H2('Do you want to know the best movies released by year? Just check them!'),
                dcc.Graph(id='sunburst_graph', style={'display': 'inline-block'})
                ], className="six columns"),

            html.Div([
                html.H2('Where are the most rating movies?'),
                dcc.Graph(id='choro_graph', style={'display': 'inline-block'})
            ], className="six columns"),
        ], className="row"),
        
        dcc.Slider(id='year_slider',
                   min=df.Year.min(),
                   max=df.Year.max(),
                   marks={str(i): '{}'.format(str(i)) for i in
                   [1990, 1995, 2000, 2005, 2010, 2014]},
                   value=df.Year.min(),
                   dots=True,
                   step=1,
                   tooltip={'always visible':False,  # show current slider values
                            'placement':'bottom'},
                  )
    
    ])
])

####################Callbacks#######################

@app.callback(
    [dash.dependencies.Output('line_graph', 'figure'),
     dash.dependencies.Output('sunburst_graph', 'figure'),
     dash.dependencies.Output('choro_graph', 'figure')],
    [dash.dependencies.Input("country_drop", "value"),
     dash.dependencies.Input("company_drop", "value"),
     dash.dependencies.Input("genre_drop", "value"),
     dash.dependencies.Input("year_slider", "value")
     ]
)


def plots(country,company, genre,year):
    
    #First plot
    new_df = df.loc[(df['Country'] == country) & (df['Genre'] == genre) & (df['Company'] == company)]
    revenue_df = new_df.groupby(by = ['Year'])['Gross','Budget'].sum()
    line = px.line(revenue_df, x=revenue_df.index, y=revenue_df.columns, title = 'Which Country has the highest revenue by category?')
    
    #Second plot
    sun_df = df.loc[(df.Year == year)].set_index('Star').groupby(['Genre'])['Score'].nlargest(1).to_frame().reset_index()
    sun = px.sunburst(
                       data_frame =sun_df,
                       path = ['Score','Star','Genre'],
                       color = 'Genre',
                       color_discrete_sequence=px.colors.qualitative.Pastel 
                        )
    
    #Third plot
    choro_df = df.loc[(df.Year == year) & (df.Genre == genre)]
    
    choro = px.choropleth(choro_df, locations="Country", color='Score', 
                    locationmode='country names',
                    range_color=[0,10],
                    color_continuous_scale=px.colors.sequential.speed
                   )
    choro.update_layout(margin=dict(l=0, r=0, t=100, b=100))
    
    
    return line, sun, choro
import dash

################################# The APP #################################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets = external_stylesheets)

app.title = "Movie Industry"

server = app.server
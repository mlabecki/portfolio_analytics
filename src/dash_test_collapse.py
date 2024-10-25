# Video:    [Bootstrap Collapse Dash Plotly](https://youtu.be/RnJGlgc9vcM)
# Docs:     [Collapse Documentation:](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/collapse/)
from dash import Dash, html, Input, Output, State       # pip install dash
import dash_bootstrap_components as dbc                 # pip install dash_bootstrap_components

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])  # https://bootswatch.com/default/
# app = Dash(__name__)
           
app.layout = html.Div([
    
    dbc.Button(
        "Why should I buy reheated pizza for $99?",
        color="link",
        id="button-question-1",
    ),
    
    dbc.Collapse(
        dbc.CardBody("Because it's a lot better than a hotdog."),
        id="collapse-question-1", is_open=False
    )

])


@app.callback(
    Output("collapse-question-1", "is_open"),
    [Input("button-question-1", "n_clicks")],
    [State("collapse-question-1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True, port=2000)
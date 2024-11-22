from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, Patch, callback

app = Dash(__name__)

app.layout = html.Div([
    html.Button("Add Filter", id="dynamic-add-filter-btn", n_clicks=0),
    html.Div(id='dynamic-dropdown-container-div', children=[]),
])

@callback(
    Output('dynamic-dropdown-container-div', 'children'),
    Input('dynamic-add-filter-btn', 'n_clicks')
    )
def display_dropdowns(n_clicks):
    patched_children = Patch()

    new_element = html.Div([
        dcc.Dropdown(
            ['NYC', 'MTL', 'LA', 'TOKYO'],
            id={
                'type': 'city-dynamic-dropdown',
                'index': n_clicks
            },
            style = {
                'width': 400
            }
        ),
        html.Div(
            id={
                'type': 'city-dynamic-output',
                'index': n_clicks
            }
        )
    ])
    patched_children.append(new_element)
    return patched_children


@callback(
    Output({'type': 'city-dynamic-output', 'index': MATCH}, 'children'),
    Input({'type': 'city-dynamic-dropdown', 'index': MATCH}, 'value'),
    State({'type': 'city-dynamic-dropdown', 'index': MATCH}, 'id'),
)
def display_output(value, id):
    return html.Div(f"Dropdown {id['index']} = {value}")


if __name__ == '__main__':
    app.run(debug = True, port = 8099)

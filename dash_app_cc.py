## Import required libraries
## Basic Funcionalities
import pandas as pd
import numpy as np

## Dash App Components
import dash
from flask import Flask
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate


## Plotly for plotting
import plotly.express as px
import plotly.graph_objects as go


## Color Style Sheets
corporate_colors = {
    'dark-blue-grey' : 'rgb(62, 64, 76)',
    'medium-blue-grey' : 'rgb(77, 79, 91)',
    'superdark-green' : 'rgb(41, 56, 55)',
    'dark-green' : 'rgb(57, 81, 85)',
    'medium-green' : 'rgb(93, 113, 120)',
    'light-green' : 'rgb(186, 218, 212)',
    'pink-red' : 'rgb(255, 101, 131)',
    'dark-pink-red' : 'rgb(247, 80, 99)',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : 'rgb(208, 206, 206)'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Load data
caffeine_dat = pd.read_csv('caffeine_cleaned.csv')

## Dictionary for Drop-down
drink_type_dict = {0: "Coffee",
                  1: "Energy Drinks",
                  2: "Energy Shots",
                  3: "Soft Drinks",
                  4: "Tea",
                  5: "Water"}

## Dictionary for Barmode of Main Histogram 2
barmode_dict = {0: "group",
                  1: "overlay",
                  2: "relative",
                  3: "stack"}

## Configure tab style
tabs_styles = {
    'height': '44px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'width': '50%',
    'color': 'black',
    "display": "inline-block"
}

tab_selected_style = {
    'borderTop': '1px solid gold',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': corporate_colors['light-grey'],
    'fontWeight': 'bold',
    'color': 'green',
    'padding': '6px'
}


## ID Last Selected
global _LAST_USED_IDS
_LAST_USED_IDS = np.arange(0, caffeine_dat.shape[0])

## Create global chart template
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"


## Web page layout
app.layout = html.Div([
    html.H1("Caffeine Content Visualization",
            style={'text-align':'center',
                    'color' : 'white',
                    'background-color' : corporate_colors['superdark-green']}),

    ## Main Histograms
    ## Drop down for main histogram 1
    html.Div([

        dcc.Tabs([

            ## Caffeine Distriution Histogram 1
              dcc.Tab(id="main_hist_tab", label='Overall Caffeine Distribution',
                        children=[

                dcc.Dropdown(id='features',
                    options=[
                        {"label": "Coffee", "value":0},
                        {"label": "Energy Drinks", "value":1},
                        {"label": "Energy Shots", "value":2},
                        {"label": "Soft Drinks", "value":3},
                        {"label": "Tea", "value":4},
                        {"label": "Water", "value":5},
                        ],
                        multi=True,
                        value=0,
                        style={'width': "50%",
                                'color' : corporate_colors['medium-blue-grey'],
                                'white-space': 'nowrap',
                                'text-overflow': 'ellipsis',
                                'border-radius' : '2px',
                                'margin-top' : '10px',
                                "margin-left" : "5px"}
                        ),

                html.Div([
                    html.Button('Select all', id='select_all', n_clicks=0),
                    html.Button('Clear', id='clear_all', n_clicks=0),
                        ],

                        className="row",
                        style={'width': '100%', "display": "inline-block",
                                'color' : corporate_colors['dark-blue-grey'],
                                'background-color' : corporate_colors['superdark-green'],
                                'margin-top' : '5px',
                                "margin-left" : "10px"}
                    ),

                dcc.Graph(id='caffeine_hist', figure={},
                          style={'width': "50%",
                                 'color' : corporate_colors['medium-blue-grey'],
                                 'white-space': 'nowrap',
                                 'text-overflow': 'ellipsis',
                                 'border-radius' : '2px',
                                 'margin-top' : '10px',
                                 "margin-left" : "10px"}),

                html.Div([
                    html.P("bin number:"),
                    dcc.Slider(id="bin_num", min=20, max=100, value=20,
                                        marks={20: '20', 100: '100'}),

                        ],

                        className="Slider Main Hist1",
                        style={'width': '30%', "display": "inline-block"}
                        ),

                    ],

                className="Caffeine Distribution Plot",
                style=tab_style, selected_style=tab_selected_style
            ),

            ## Caffeine Distriution Histogram 1
            dcc.Tab(label='Caffeine Distribution by Type',
                    children=[

                dcc.Dropdown(id='barmode',
                    options=[
                        {"label": "group", "value":0},
                        {"label": "overlay", "value":1},
                        {"label": "relative", "value":2},
                        {"label": "stack", "value":3},
                        ],
                        multi=False,
                        value=0,
                        clearable=False,
                        style={'width': "49%",
                                'color' : corporate_colors['medium-blue-grey'],
                                'white-space': 'nowrap',
                                'text-overflow': 'ellipsis',
                                'border-radius' : '2px',
                                'margin-top' : '10px',
                                "margin-left" : "5px"}
                        ),

                dcc.Graph(id='caffeine_hist2', figure={},
                          style={'width': "50%",
                                 'color' : corporate_colors['medium-blue-grey'],
                                 'white-space': 'nowrap',
                                 'text-overflow': 'ellipsis',
                                 'border-radius' : '2px',
                                 'margin-top' : '10px',
                                 "margin-left" : "10px"}),

                html.Div([
                    html.P("bin number:"),
                    dcc.Slider(id="bin_num2", min=20, max=100, value=20,
                                        marks={20: '20', 100: '100'}),

                        ],

                        className="Slider Main Hist2",
                        style={'width': '30%', "display": "inline-block"}
                        ),

                    ],

                className="Caffeine Distribution Plot",
                style=tab_style, selected_style=tab_selected_style,

                    ),
                ],

                className="row",
                parent_style={'width': '100%', "display": "inline-block"},
                style=tabs_styles,
                colors={
                    "border": 'black',
                    "primary":  'grey',
                    "background": 'grey'
                    }
            ),


        ## Reactive Histograms
        html.Div([

            ## Reactive Histogram Volumn
            html.Div([
                dcc.Graph(id='vol_hist', figure={},
                          style={'width': "100%",
                             'color' : corporate_colors['medium-blue-grey'],
                             'white-space': 'nowrap',
                             'text-overflow': 'ellipsis',
                             'border-radius' : '2px',
                             'margin-left' : '5px',
                             'margin-right' : '5px'
                             }),


                html.Div([
                    html.P("bin number:"),
                    dcc.Slider(id="bin_num_vol", min=20, max=100, value=20,
                                        marks={20: '20', 100: '100'}),
                        ],
                        className="Slider Volumn",
                        style={'width': '45%'}
                        ),

                ],

                className="Distribution of Volumn",
                style={'width': "45%",
                      'color' : corporate_colors['medium-blue-grey'],
                      'white-space': 'nowrap',
                      'text-overflow': 'ellipsis',
                      'border-radius' : '2px',
                      'margin-left' : '5px',
                      'margin-right' : '5px'
                      }
            ),

            ## Reactive Histogram Volumn
            html.Div([
                dcc.Graph(id='calories_hist', figure={},
                          style={'width': "100%",
                             'color' : corporate_colors['medium-blue-grey'],
                             'white-space': 'nowrap',
                             'text-overflow': 'ellipsis',
                             'border-radius' : '2px',
                             'margin-left' : '5px',
                             }),

                html.Div([
                    html.P("bin number:"),
                    dcc.Slider(id="bin_num_cal", min=20, max=100, value=20,
                                        marks={20: '20', 100: '100'}),
                        ],
                        className="Slider calories",
                        style={'width': '45%'}
                        ),

                    ],
                className="Distribution of Calories",
                style={'width': "45%",
                      'color' : corporate_colors['medium-blue-grey'],
                      'white-space': 'nowrap',
                      'text-overflow': 'ellipsis',
                      'border-radius' : '2px',
                      'margin-left' : '5px',
                      }
            ),

            ],
                className="row",
                style={'width': '100%', "display": "flex",
                        'color' : corporate_colors['medium-blue-grey'],
                        'white-space': 'nowrap',
                        'text-overflow': 'ellipsis',
                        'border-radius' : '2px',
                        'margin-top' : '30px'
                        }
            ),

        ],

        className="caffeine_distribution_hist_by_features",
        style={'width': '100%', "display": "inline-block",
                'background-color' : corporate_colors['superdark-green']}
        ),
])


## Create graphs
## Plot Main Caffeine Distribution Histrogram 1
@app.callback(
    Output(component_id='caffeine_hist', component_property='figure'),
    [Input(component_id='features', component_property='value'),
    Input(component_id="bin_num", component_property="value")]
    )
def plot_hist_caffeine(features, bin_num):

    caffeine_dat_c = caffeine_dat.copy()

    if (not isinstance(features, list)):
        features = [features]

    features_names = [drink_type_dict[type_int] for type_int in features]
    caffeine_dat_c = caffeine_dat_c[caffeine_dat_c['type'].isin(features_names)]


    x_min = np.min(caffeine_dat_c["caffeine"])
    x_max = np.max(caffeine_dat_c["caffeine"])

    _HIST_CAFFEINE = px.histogram(caffeine_dat_c, x="caffeine",
                                    hover_name="drink",
                                    nbins=bin_num,
                                    marginal="box",
                                    title = 'Caffeine Distribution',
                                    hover_data=caffeine_dat_c.columns)


    _HIST_CAFFEINE.update_xaxes(range=[x_min, x_max])
    _HIST_CAFFEINE = go.FigureWidget(_HIST_CAFFEINE)


    return _HIST_CAFFEINE

## Update Dropdown Item Upon Button
@app.callback(
    Output('features', 'value'),
    [Input('select_all', 'n_clicks')],
    [Input('clear_all', 'n_clicks')],
    [State('features', 'options')])
def update_dropdown(select_all_clicks, clear_all_clicks, feature_options):

    ## Check the source of trigger and select ids based on trigger
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate()
    else:
        trigged_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigged_id == 'select_all':
            if select_all_clicks == 0: ## Do not update in the beginning
                raise PreventUpdate()

            else: ## Select all options otherwise
                return [i['value'] for i in feature_options]

        if trigged_id == 'clear_all':
            if clear_all_clicks == 0: ## Do not update in the beginning
                raise PreventUpdate()
            else: ## Else clear all the options
                return []
        else:
            raise PreventUpdate()


## Plot Main Caffeine Distribution Histrogram 1
@app.callback(
    Output(component_id='caffeine_hist2', component_property='figure'),
    [Input(component_id='barmode', component_property='value'),
    Input(component_id="bin_num2", component_property="value")]
    )
def plot_hist_caffeine2(barmode, bin_num2):

    caffeine_dat_c = caffeine_dat.copy()

    x_min = np.min(caffeine_dat_c["caffeine"])
    x_max = np.max(caffeine_dat_c["caffeine"])

    _HIST_CAFFEINE2 = px.histogram(caffeine_dat_c, x="caffeine",
                                    hover_name="drink",
                                    color='type',
                                    nbins=bin_num2,
                                    marginal="box",
                                    opacity=0.9,
                                    barmode = barmode_dict[barmode],
                                    title = 'Caffeine Distribution by Type',
                                    hover_data=caffeine_dat_c.columns)


    _HIST_CAFFEINE2.update_xaxes(range=[x_min, x_max])
    _HIST_CAFFEINE2 = go.FigureWidget(_HIST_CAFFEINE2)


    return _HIST_CAFFEINE2

## Plot Reactive Volumn Distribtion Histrogram
@app.callback(
    Output(component_id='vol_hist', component_property='figure'),
    [Input(component_id='caffeine_hist', component_property='clickData'),
     Input(component_id='caffeine_hist2', component_property='clickData'),
     Input(component_id='bin_num_vol', component_property='value')],
    )
def plot_hist_volumn(caffeine_hist_clickData, caffeine_hist2_clickData,
                     bin_num_vol):

    global _LAST_USED_IDS

    caffeine_dat_c = caffeine_dat.copy()

    ## Check the source of trigger and select ids based on trigger
    ctx = dash.callback_context
    if not ctx.triggered:
        pass
    else:
        trigged_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigged_id == 'bin_num_vol':
            selected_ids = _LAST_USED_IDS

        if trigged_id == 'caffeine_hist':
            selected_ids = caffeine_hist_clickData['points'][0]['pointNumbers']
            _LAST_USED_IDS = selected_ids

        if trigged_id == 'caffeine_hist2':
            selected_ids = caffeine_hist2_clickData['points'][0]['pointNumbers']
            _LAST_USED_IDS = selected_ids

        caffeine_dat_c = caffeine_dat_c.iloc[selected_ids]


    x_min = np.min(caffeine_dat_c["volumn"])
    x_max = np.max(caffeine_dat_c["volumn"])

    _HIST_VOL = px.histogram(caffeine_dat_c, x="volumn",
                             hover_name="drink",
                             nbins=bin_num_vol,
                             marginal="box",
                             title = 'Volumn Distributionof Selected Data',
                             hover_data=caffeine_dat_c.columns)


    _HIST_VOL.update_xaxes(range=[x_min, x_max])
    _HIST_VOL = go.FigureWidget(_HIST_VOL)

    return _HIST_VOL

## Plot Reactive Calories Distribtion Histrogram
@app.callback(
    Output(component_id='calories_hist', component_property='figure'),
    [Input(component_id='caffeine_hist', component_property='clickData'),
     Input(component_id='caffeine_hist2', component_property='clickData'),
     Input(component_id='bin_num_cal', component_property='value')],
    )
def plot_hist_cal(caffeine_hist_clickData, caffeine_hist2_clickData, bin_num_cal):

    global _LAST_USED_IDS

    caffeine_dat_c = caffeine_dat.copy()

    ## Check the source of trigger and select ids based on trigger
    ctx = dash.callback_context
    if not ctx.triggered:
        pass
    else:
        trigged_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigged_id == 'bin_num_cal':
            selected_ids = _LAST_USED_IDS

        if trigged_id == 'caffeine_hist':
            selected_ids = caffeine_hist_clickData['points'][0]['pointNumbers']
            _LAST_USED_IDS = selected_ids

        if trigged_id == 'caffeine_hist2':
            selected_ids = caffeine_hist2_clickData['points'][0]['pointNumbers']
            _LAST_USED_IDS = selected_ids

        caffeine_dat_c = caffeine_dat_c.iloc[selected_ids]

    x_min = np.min(caffeine_dat_c["calories"])
    x_max = np.max(caffeine_dat_c["calories"])

    _HIST_CAL = px.histogram(caffeine_dat_c, x="calories",
                             hover_name="drink",
                             nbins=bin_num_cal,
                             marginal="box",
                             title = 'Calories Distribution of Selected Data',
                             hover_data=caffeine_dat_c.columns)


    _HIST_CAL.update_xaxes(range=[x_min, x_max])
    _HIST_CAL = go.FigureWidget(_HIST_CAL)

    return _HIST_CAL

# @server.route("/dash")
# def MyDashApp():
#     app.title = "Caffeine Data Visualization"
#     return app.index()

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8725, debug=True)

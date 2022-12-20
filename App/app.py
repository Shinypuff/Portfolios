import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px

# COLOR
colors = {'background': '#111111', 'text': '#322433'}

# LOAD DATA
metr = pd.read_excel('Data/metrics_all.xlsx')
prices = pd.read_excel('Data/metrics_price.xlsx')

ports = list(metr['index'].unique())
meth = list(metr['Method'].unique())

options_p = []
options_m = []
options_metr=[]

for p in ports:
 options_p.append({'label': p, 'value': p})

for m in meth:
 options_m.append({'label': m, 'value': m})

for metric in metr.columns:
    options_metr.append({'label': metric, 'value': metric})

method_selector = dcc.Dropdown(
 id='method_selector',
 options=options_m,
 value='Sharpe',
 multi=False
)

port_selector = dcc.Dropdown(
 id='port_selector',
 options=options_p,
 multi=False
)

metrics_selector = dcc.Dropdown(
 id='metrics_selector',
 options=options_metr,
 value='AVG_returns',
 multi=False
)

# LAYOUT
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP] ,suppress_callback_exceptions=True)

weights = html.Div(
    [
        html.Div('Markowitz',style={'margin-left': '20px', 'margin-top':'5px'}),
        html.Div( style={'width': '50px','margin-top':'5px','margin-bottom': '10px', 'margin-left': '20px'}),
        html.Div('Sharpe', style={'margin-left': '20px'}),
        html.Div( style={'width': '50px', 'margin-bottom': '10px', 'margin-left': '20px'}),
        html.Div('Tobin', style={'margin-left': '20px'}),
        html.Div( style={'width': '50px', 'margin-bottom': '30px', 'margin-left': '20px'})

    ], style = {'width':'300px',
             'height':'245px',
             'margin-bottom': '40px',
             'margin-left':'5px',
             'border-radius': '25px',
             'border': '6px solid #efbbcc',
             'backgroundColor':'#ffffff'}
)

selectors = html.Div(
    [
        html.Div('Portfolio selector',style={'margin-left': '20px', 'margin-top':'5px'}),
        html.Div(port_selector, style={'width': '500px','margin-top':'5px','margin-bottom': '10px', 'margin-left': '20px'}),
        html.Div('Method selector', style={'margin-left': '20px'}),
        html.Div(method_selector, style={'width': '500px', 'margin-bottom': '10px', 'margin-left': '20px'}),
        html.Div('Metric selector', style={'margin-left': '20px'}),
        html.Div(metrics_selector, style={'width': '500px', 'margin-bottom': '30px', 'margin-left': '20px'})

    ], style = {'width':'560px',
             'height':'245px',
             'margin-bottom': '40px',
             'margin-left':'50px',
             'border-radius': '25px',
             'border': '6px solid #efbbcc',
             'backgroundColor':'#ffffff'}
)

metr_gr = html.Div(
    [html.Div(children='Metrics', style={'textAlign': 'center', 'color': colors['text']}),
    dcc.Graph(id='srez_metr', style={'width': '100px', 'margin-bottom': '50px', 'border-radius': '25px'})],
    style = {'width':'750px',
             'height':'500px',
             'margin-bottom': '50px',
             'margin-left':'50px',
             'border-radius': '25px',
             'border': '6px solid #efbbcc',
             'backgroundColor':'#ffffff'}
)

pr_gr = html.Div(
    [html.Div(children='Price', style={'textAlign': 'center', 'color': colors['text']}),
     dcc.Graph(id='price_metr', style={'width': '100px','margin-bottom': '50px'})],
    style={'width': '750px',
           'height':'500px',
           'margin-bottom': '50px',
           'border-radius': '25px',
           'border': '6px solid #efbbcc',
           'backgroundColor':'#ffffff'}
)

app.layout = html.Div([
    html.H1(children='PORTFOLIO ANALYSIS', style={'margin-bottom':'35px','textAlign': 'center', 'color': colors['text']}),

    dbc.Row([dbc.Col([selectors], width=3), dbc.Col([weights], width={"size": 6, "offset": 2})]),
    dbc.Row([dbc.Col(metr_gr, width=6), dbc.Col(pr_gr, width=6) ])
],
 style={'margin-top':'15px','margin-left': '15px', 'margin-right': '15px','border-radius': '25px','backgroundColor':'#f5dde0'})


#PLOTTING

#CALLBACKS
@app.callback(
    [Output(component_id='srez_metr', component_property='figure'),
    Output(component_id='price_metr', component_property='figure')],
    [Input(component_id='port_selector', component_property='value'),
     Input(component_id='metrics_selector', component_property='value'),
     Input(component_id='method_selector', component_property='value')]
)

def get_srez(port,metrics ,method):

    melted = prices.melt(id_vars=['Date', 'Method'])

    if port != None and method == None:
        asd = metr.loc[metr['index'] == port, :]
        bars = 'Method'
        val=metrics

        mask = melted.loc[melted['variable']==port, :]
        cut = mask.pivot_table(index = 'Date', columns='Method', values='value')
        name='Portfolio: '+port

    elif method != None and port == None:
        asd = metr.loc[metr['Method'] == method, :]
        bars = 'index'
        val = metrics

        mask = melted.loc[melted['Method']==method, :]
        cut = mask.pivot_table(index = 'Date', columns='variable', values='value')
        name='Method: Top 20 '+method

    elif port != None and method != None:
        asd = metr.loc[metr['Method'] == method, :]
        asd = asd.loc[asd['index'] == port, metrics]
        bars = str(metrics)
        val = asd

        cut = prices.loc[prices['Method'] == method, :].drop('Method', axis=1)
        cut = cut.loc[:, port].to_frame()
        name = 'Portfolio: ' + port + '   ' + 'Method: ' + method

    else:
        cut = pd.DataFrame()
    print(asd)

    fig = px.bar(asd, x=bars, y=val, title=name,barmode='relative', color=bars, width=700, height=450)

    fig1 = px.line(cut, x=cut.index, y=cut.columns, title=name, width=700, height=450, )

    return fig, fig1

if __name__ == '__main__':
    app.run_server(debug = True)
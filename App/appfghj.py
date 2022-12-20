import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px

# COLOR
my_colors = ["#1a4441", "#2b5553", "#e6bf7b", "#c8a36c", "#936747"]
sns.palplot(sns.color_palette(my_colors))

# STYLE
sns.set_style("white")
mpl.rcParams['xtick.labelsize'] = 16
mpl.rcParams['ytick.labelsize'] = 16
mpl.rcParams['axes.spines.left'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False

# LOAD DATA
metr = pd.read_excel('metrics_all.xlsx')
prices = pd.read_excel('metrics_price.xlsx')

ports = list(metr['index'].unique())
meth = list(metr['Method'].unique())

options_p = []
options_m = []

for p in ports:
 options_p.append({'label': p, 'value': p})

for m in meth:
 options_m.append({'label': m, 'value': m})

method_selector = dcc.Dropdown(
 id='method_selector',
 options=options_m,
 value=list(metr['Method'].unique()),
 multi=0
)

port_selector = dcc.Dropdown(
 id='port_selector',
 options=options_p,
 value=list(metr['index'].unique()),
 multi=0
)

# LAYOUT
app = dash.Dash(__name__)

app.layout = html.Div([
 html.H1('PORTFOLIO ANALYSIS'),
 html.Div('Portfolio selector'),
 html.Div(port_selector,
          style={'width': '500px',
                 'margin-bottom': '50px'}),
 html.Div('Method selector'),
 html.Div(method_selector,
          style={'width': '500px',
                 'margin-bottom': '50px'}),
 html.Div('Weapon class - Damage dependancy')
],
 style={'margin-left': '90px', 'margin-left': '90px'})

if __name__ == '__main__':
 app.run_server(debug=True)
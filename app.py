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

#COLOR
my_colors = ["#1a4441", "#2b5553", "#e6bf7b", "#c8a36c", "#936747"]
sns.palplot(sns.color_palette(my_colors))

#STYLE
sns.set_style("white")
mpl.rcParams['xtick.labelsize'] = 16
mpl.rcParams['ytick.labelsize'] = 16
mpl.rcParams['axes.spines.left'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False

#LOAD DATA
metr = pd.read_excel('metrics_all.xlsx')
prices = pd.read_excel('metrics_price.xlsx')

ports = list(metr['index'].unique())
meth = list(metr['Method'].unique())

options_p=[]
options_m=[]
for p,m in ports, meth:
    options_p.append({'label': p, 'value': p})
    options_m.append({'label': m, 'value': m})
    

method_selector = dcc.Dropdown(
    id = 'method_selector',
    options=options_m,
    value = list(metr['Method'].unique()),
    multi=0
)

port_selector = dcc.Dropdown(
    id = 'port_selector',
    options=options_p,
    value = list(metr['index'].unique()),
    multi=0
)


#PLOTTING
def show_values_on_bars(axs, h_v="v", space=0.4):
    def _show_on_single_plot(ax):
        if h_v == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height()
                value = int(p.get_height())
                ax.text(_x, _y, format(value, ','), ha="center")
        elif h_v == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height()
                value = int(p.get_width())
                ax.text(_x, _y, format(value, ','), ha="left")
    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)


fig_2, ax = plt.subplots(figsize=(25, 13))
fig_2 = sns.barplot(data=df['Type'].value_counts().reset_index(), x='Type', y='index')
show_values_on_bars(axs=ax, h_v="h", space=0.1)

app = dash.Dash(__name__)

#LAYOUT
app.layout = html.Div([
    html.H1('ELDEN RING'),
    html.Div('Damage output selector'),
    html.Div(damage_selector,
             style={'width': '500px',
                    'margin-bottom': '50px'}),
    html.Div('Weight categories'),
    html.Div(wgt_selector,
             style={'width': '500px',
                    'margin-bottom': '50px'}),
    html.Div('Weapon class - Damage dependancy'),
    dcc.Graph(id='phy-class-chart')
],
    style={'margin-left': '90px', 'margin-left': '90px'})

#CALLBACKS
@app.callback(
    Output(component_id='phy-class-chart', component_property='figure'),
    [Input(component_id='range-slider', component_property='value'),
     Input(component_id='weight_selector', component_property='value')]
)
def update_wgt_class_chart(damage_range, wpn_dmg):
    chart_data = group_result[(group_result['Phy'] > damage_range[0]) &
                      (group_result['Phy'] < damage_range[1]) &
                      (group_result['Wgt'].isin(wpn_dmg))]
    fig = px.histogram(chart_data, y='Phy', x='Type', labels = {'Phy': 'Damage', 'Type':'Type'}).update_layout(yaxis_title = 'Damage')

    return fig


if __name__ == '__main__':
    app.run_server(debug = True)

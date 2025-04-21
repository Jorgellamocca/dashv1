import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from sklearn.datasets import load_iris, load_wine

import dash
import dash_core_components as dcc
import dash_html_components as html
#from dash import dcc, html

from dash.dependencies import Input, Output


############ Loading Datasets ##################
iris = load_iris()

iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df["FlowerType"] = [iris.target_names[target] for target in iris.target]

wine = load_wine()

wine_df = pd.DataFrame(data=wine.data, columns=wine.feature_names)
wine_df["WineType"] = [wine.target_names[target] for target in wine.target]


file_path = "/home/wrf/datasets/AAPL.csv"
apple_df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')

print("Columnas del archivo CSV:", apple_df.columns.tolist())


################# Line Chart ##############################
chart1 = go.Figure()

chart1.add_trace(go.Scatter(x=apple_df.Date, y=apple_df.Open,
                            marker={"color":"tomato"},
                            mode="lines"))


chart1.update_layout(height=500,
                     xaxis_title="Date",
                     yaxis_title="Price ($)",
                     title="Apple Stock Prices [Apr-2019-Mar-2020]")

################# Scatter Plot ################################
chart2 = px.scatter(data_frame=wine_df,
                   x=wine.feature_names[0],
                   y=wine.feature_names[1],
                   color="WineType",
                   title="alcohol vs malic_acid color-encoded by wine type",
                   height=500,
                   )


################## Bar Chart ###############################                   
iris_avg_by_flower_type = iris_df.groupby(by="FlowerType").mean().reset_index()

chart3 = px.bar(data_frame=iris_avg_by_flower_type,
               x="FlowerType",
               y=iris.feature_names[0],
               title="Avg %s Per Flower Type"%iris.feature_names[0],
               height=500,
               )

#################### Creating App Object ############################               
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

####################### Setting Graphs as HTML Children ##############             
graph1 = dcc.Graph(
        id='graph1',
        figure=chart1,
        #className="eight columns"
    )

graph2 = dcc.Graph(
        id='graph2',
        figure=chart2,
        #className="five columns"
    )

graph3 = dcc.Graph(
        id='graph3',
        figure=chart3,
        #className="five columns"
    )


############### Creating Widgets For Each Graph #########################    
multi_select_line_chart = dcc.Dropdown(
        id="multi_select_line_chart",
        options=[{"value":label, "label":label} for label in ["Open", "Low", "High", "Close"]],
        value=["Open"],
        multi=True,
        clearable = False
    )

dropdown1_scatter_chart = dcc.Dropdown(
        id="dropdown1_scatter_chart",
        options=[{"value":label, "label":label} for label in wine.feature_names],
        value=wine.feature_names[0],
        className="six columns",
        clearable = False
    )

dropdown2_scatter_chart = dcc.Dropdown(
        id="dropdown2_scatter_chart",
        options=[{"value":label, "label":label} for label in wine.feature_names],
        value=wine.feature_names[1],
        className="six columns",
        clearable = False
    )

dropdown_bar_chart = dcc.Dropdown(
        id="dropdown_bar_chart",
        options=[{"value":label, "label":label} for label in iris.feature_names],
        value=iris.feature_names[0],
        clearable = False
    )


######################### Laying out Charts & Widgets to Create App Layout ##########
header = html.H2(children="Simple Dashboard With Widgets")

row1 = html.Div(children=[multi_select_line_chart, graph1], className="eight columns")

scatter_div = html.Div(children=[html.Div(children=[dropdown1_scatter_chart, dropdown2_scatter_chart], className="row") , graph2], className="six columns")

bar_div = html.Div(children=[dropdown_bar_chart, graph3], className="six columns")

row2 = html.Div(children=[scatter_div, bar_div], className="eight columns")

layout = html.Div(children=[header, row1, row2], style={"text-align": "center", "justifyContent":"center"})

############### Setting App Layout ########################################
app.layout = layout


################## Creating Callbacks for Each Widget ############################
@app.callback(Output('graph1', 'figure'), [Input('multi_select_line_chart', 'value')])
def update_line(price_options):
    chart1 = go.Figure()

    for price_op in price_options:
        chart1.add_trace(go.Scatter(x=apple_df.Date, y=apple_df[price_op],
                                mode="lines", name=price_op))


    chart1.update_layout(
                         xaxis_title="Date",
                         yaxis_title="Price ($)",
                         title="Apple Stock Prices [Apr-2019-Mar-2020]",
                         height=500,)
    return chart1



@app.callback(Output('graph2', 'figure'), [Input('dropdown1_scatter_chart', 'value'), Input('dropdown2_scatter_chart', 'value')])
def update_scatter(drop1, drop2):
    chart2 = px.scatter(data_frame=wine_df,
                   x=drop1,
                   y=drop2,
                   color="WineType",
                   title="%s vs %s color-encoded by wine type"%(drop1, drop2),
                   height=500,
                   )

    return chart2


@app.callback(Output('graph3', 'figure'), [Input('dropdown_bar_chart', 'value')])
def update_bar(bar_drop):
    chart3 = px.bar(data_frame=iris_avg_by_flower_type,
               x="FlowerType",
               y=bar_drop,
               title="Avg %s Per Flower Type"%bar_drop,
               height=500,
               )
    return chart3


################## Running App #####################################

if __name__ == "__main__":
    app.run_server(debug=True)

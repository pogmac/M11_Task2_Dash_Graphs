import pandas as pd
import datetime as dt
import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

def render_tab(df):

    dfweekday = df
    dfweekday['weekday'] = df['tran_date'].dt.day_name()
    grouped =dfweekday[dfweekday['total_amt']>0].groupby(['Store_type','weekday'])['total_amt'].sum()

    traces = []
    for col in grouped.columns:
        traces.append(go.Bar(x=grouped.index,y=grouped[col],name=col,hoverinfo='text',
                             hovertext=[f'{y/1e3:.2f}k' for y in grouped[col].values]))
    data = traces
    fig = go.Figure(data=data,layout=go.Layout(title='Income per Store-type and weekday',barmode='stack',legend=dict(x=0,y=-0.5)))

#    return fig

    layout = html.Div([html.H1('Store Type',style={'text-align':'center'}),
                        #html.Div([dcc.DatePickerRange(id='sales-range',
                        #start_date=df['tran_date'].min(),
                        #end_date=df['tran_date'].max(),
                        #display_format='YYYY-MM-DD')],style={'width':'100%','text-align':'center'}),
                        #html.Div([html.Div([dcc.Graph(id='bar-sales')],style={'width':'50%'}),
                        #html.Div([dcc.Graph(id='choropleth-sales')],style={'width':'50%'})],style={'display':'flex'})
                        
                        html.Div([html.Div([dcc.Graph(id='income-per-cat-weekday',figure=fig)],style={'width':'50%'}),
                        html.Div([dcc.Dropdown(id='prod_dropdown',
                                    options=[{'label':prod_cat,'value':prod_cat} for prod_cat in df['prod_cat'].unique()],
                                    value=df['prod_cat'].unique()[0]),
                                    dcc.Graph(id='barh-prod-subcat2')],style={'width':'50%'})],
                                    style={'display':'flex'}),
                                    html.Div(id='temp-out')
                        ])

    return layout

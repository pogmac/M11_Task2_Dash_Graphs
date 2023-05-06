import pandas as pd
import datetime as dt
import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

def render_tab(df):
    fig = go.Figure()
    dfweekday = df
    dfweekday['weekday'] = df['tran_date'].dt.dayofweek
    #dfweekday['weekday'] = df['tran_date'].dt.day_name()
    grouped =dfweekday[dfweekday['total_amt']>0].groupby(['Store_type','weekday'])['total_amt'].sum().reset_index()
    #grouped =dfweekday[dfweekday['total_amt']>0].groupby(['Store_type','weekday'])['total_amt'].sum().reset_index()
    #grouped_new_index = 
    print(grouped['weekday'])
    grouped.set_index('weekday', inplace =True)
    traces = []
    
    
    groupedp = grouped.pivot_table(values='total_amt',index='weekday',columns='Store_type',aggfunc=np.sum)

    obj = groupedp     
    print(obj)
    print(type(obj))
    print(obj.shape)

    for col in obj.columns:
         print(col)
         traces.append(go.Bar(x=obj.index,y=obj[col],name=col)) #,hoverinfo='text',
         #                   hovertext=[f'{y/1e3:.2f}k' for y in grouped[col].values]))
    data = traces

    print(data)
    fig = go.Figure(data=data,layout=go.Layout(title='Income per shop cat and weekday',barmode='stack',legend=dict(x=0,y=-0.5)))

    layout = html.Div([html.H1('Store Type',style={'text-align':'center'}),
                        #html.Div([dcc.DatePickerRange(id='sales-range',
                        #start_date=df['tran_date'].min(),
                        #end_date=df['tran_date'].max(),
                        #display_format='YYYY-MM-DD')],style={'width':'100%','text-align':'center'}),
                        #html.Div([html.Div([dcc.Graph(id='bar-sales')],style={'width':'50%'}),
                        #html.Div([dcc.Graph(id='choropleth-sales')],style={'width':'50%'})],style={'display':'flex'})
                        
                        html.Div([html.Div([dcc.Graph(id='income-per-cat-weekday',figure=fig)],style={'width':'50%'}),                        
                        html.Div([dcc.Graph()],style={'width':'50%'})],
                                    style={'display':'flex'}),
                                    html.Div(id='temp-out')
                        ])

    return layout
"""
    x = [
    ["BB+", "BB+", "BB+", "BB", "BB", "BB"],
    [16, 17, 18, 16, 17, 18,]
    ]
    print(x)
    fig = go.Figure()
    fig.add_bar(x=x,y=[1,2,3,4,5,6])
    fig.add_bar(x=x,y=[6,5,4,3,2,1])
"""
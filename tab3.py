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
###### BEGIN graph "fig2"    
    fig2 = go.Figure()
    dfage = df
    print(dt.date.today())
    print(type(df['tran_date']))
    print(df['tran_date'])
    print(df.iloc[0,2])
    dfage['age'] = 2023 - pd.DatetimeIndex(df['DOB']).year
    print(type(dfage['age']))
    print(dfage[['Store_type','age']])
    dfAgeStore = dfage[['Store_type','age']]
    dfAgeStore['count_age'] = dfAgeStore.groupby(['Store_type','age'])['age'].transform('count')
    dfAgeStoreF = dfAgeStore.groupby(['Store_type','age']).first().reset_index()
    #dfAgeStoreF.set_index('age', inplace = True)


    dfAgeStoreF = dfAgeStoreF.pivot_table(values='count_age',index=('age'),columns='Store_type',aggfunc=np.sum)
    #grouped2 = dfAgeStore.groupby(['Store_type','age'])['age'].count()
    #print(grouped2.set_index(name ='age'))
    obj = dfAgeStoreF
    print(obj)
    print(type(obj))
    print(obj.shape)
    #print(obj.index)

    traces = []
    for col in obj.columns:
         print(col)
         traces.append(go.Bar(x=obj.index,y=obj[col],name=col)) 
    data = traces
    fig2 = go.Figure(data=data,layout=go.Layout(title='Customer age per Store Type',barmode='stack',legend=dict(x=0,y=-0.5)))
    
###### END graph "fig2"    

###### BEGIN first graph "fig"    
    fig = go.Figure()
    dfweekday = df
    dfweekday['weekday'] = df['tran_date'].dt.dayofweek
    dfweekday['weekday_eng'] = df['tran_date'].dt.day_name()
    grouped =dfweekday[dfweekday['total_amt']>0].groupby(['Store_type','weekday','weekday_eng'])['total_amt'].sum().reset_index()
    grouped.set_index('weekday', inplace =True)
    traces = []
    
    
    groupedp = grouped.pivot_table(values='total_amt',index=('weekday','weekday_eng'),columns='Store_type',aggfunc=np.sum)
    groupedp.reset_index(inplace =True)
    groupedp.drop(['weekday'], axis =1, inplace = True)
    groupedp.set_index('weekday_eng', inplace =True)

    obj = groupedp     
    print(obj)
    print(type(obj))
    print(obj.shape)

    for col in obj.columns:
         #print(col)
         traces.append(go.Bar(x=obj.index,y=obj[col],name=col)) #,hoverinfo='text',
         #                   hovertext=[f'{y/1e3:.2f}k' for y in grouped[col].values]))
    data = traces
    #print(data)
    fig = go.Figure(data=data,layout=go.Layout(title='Income per shop cat and weekday',barmode='stack',legend=dict(x=0,y=-0.5)))
###### END first graph "fig"    

    layout = html.Div([html.H1('Store Type',style={'text-align':'center'}),
                        #html.Div([dcc.DatePickerRange(id='sales-range',
                        #start_date=df['tran_date'].min(),
                        #end_date=df['tran_date'].max(),
                        #display_format='YYYY-MM-DD')],style={'width':'100%','text-align':'center'}),
                        #html.Div([html.Div([dcc.Graph(id='bar-sales')],style={'width':'50%'}),
                        #html.Div([dcc.Graph(id='choropleth-sales')],style={'width':'50%'})],style={'display':'flex'})
                        
                        html.Div([html.Div([dcc.Graph(id='income-per-cat-weekday',figure=fig)],style={'width':'50%'}),                        
                        html.Div([dcc.Graph(id='age-count-per-store-type',figure=fig2)],style={'width':'50%'})],
                                    style={'display':'flex'}),
                                    html.Div(id='temp-out')
                        ])

    return layout
    
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging

from flask import Flask

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

import pandas as pd

import plotly.graph_objs as go


app=dash.Dash(
    name=__name__,
    # server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server=app.server

# Data import
df = pd.read_csv('./static/fraud.csv')

from calendar import month_name

optoinsToRemove=[
    'sendDataToCloud',
    'select2d',
    'lasso2d',
    'zoomIn2d',
    'zoomOut2d',
    'autoScale2d',
    'hoverClosestCartesian',
    'hoverCompareCartesian',
    'toggleSpikelines'
]

months={
    1:'Январь',
    2:'Февраль',
    3:'Март',
    4:'Апрель',
    5:'Май',
    6:'Июнь',
    7:'Июль',
    8:'Август',
    9:'Сентябрь',
    10:'Октябрь',
    11:'Ноябрь',
    12:'Декабрь'
}

# Data preparation
df.drop(columns='Unnamed: 0', inplace=True)
df['Date'] = pd.to_datetime(df.Date)
df['Day'] = df.Date.dt.weekday.apply(lambda x: 'Рабочий' if x < 5 else 'Выходной')
df['WeekInMonth']=(df.Date.dt.day-1)//7
df.sort_values('Date', inplace=True)
df.set_index('Date', inplace=True)


body=dbc.Container(
    [
        dbc.Row([html.H2('Статистика за 2017 год')]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='first',
                    figure=go.Figure(
                        data = [
                            go.Bar(
                                x=df[df.Day=='Рабочий'].index,
                                y=df[df.Day=='Рабочий'].Count,
                                name='Рабочий'
                            ),
                            go.Bar(
                                x=df[df.Day=='Выходной'].index,
                                y=df[df.Day=='Выходной'].Count,
                                name='Выходной'
                            )
                        ],
                        layout = go.Layout(
                            title='Количество выписок',
                            xaxis=dict(
                                rangeselector=dict(
                                    buttons=list([
                                        dict(
                                            count=1,
                                            label='1 месяц',
                                            step='month',
                                            stepmode='backward'
                                        ),
                                        dict(
                                            count=6,
                                            label='6 месяцев',
                                            step='month',
                                            stepmode='backward'
                                        ),
                                        dict(label='Год', step='all')
                                    ])
                                ),
                                rangeslider=dict(visible=True),
                                range=[
                                    df.index.min()-pd.to_timedelta('1d'),
                                    df.index.max()+pd.to_timedelta('1d')
                                ],
                                type='date',
                            ),
                            dragmode='pan'
                        )
                    ),
                    config=dict(modeBarButtonsToRemove=optoinsToRemove)
                ),
                md=12
            )
        ]),
        dbc.Row([html.H2('Детальная статистика')]),
        dbc.Row([
            dbc.Col(
                [
                    html.H4('Группировать по'),
                    dcc.Dropdown(
                        id='dropdownAgg',
                        options=[
                            dict(label='1 неделя', value='1w'),
                            dict(label='2 недели', value='2w'),
                            dict(label='1 месяц', value='1m'),
                        ],
                        value='1m',
                        clearable=False
                    )
                ],
                md=6,
            ),
            dbc.Col(
                [
                    html.H4('Месяц'),
                    dcc.Dropdown(
                            id='dropdownMon',
                            options=[
                                dict(label=months[i], value=i) \
                                for i in range(1,13)
                            ],
                            multi=True,
                            value=[1, 2],
                            placeholder='Выберите месяц(ы)'
                    )
                ],
                md=6
            )
        ]),
        dbc.Row([
            dbc.Col(
                [dcc.Graph(
                    id='graphAgg',
                    config=dict(modeBarButtonsToRemove=optoinsToRemove)
                )],
                md=6
            ),
            dbc.Col(
                [dcc.Graph(
                    id='graphMon',
                    config=dict(modeBarButtonsToRemove=optoinsToRemove)
                )],
                md=6
            )
        ])
    ],
    className="mt-4"
)

app.layout=html.Div([body])

@app.callback(
    Output('graphAgg', 'figure'),
    [Input('dropdownAgg', 'value')]
)
def updateGraphAgg(agg):
    temp = {'1w':'week', '2w':'2 weeks', '1m':'month'}

    return go.Figure(
        data=[go.Bar(
            x=df.Count.resample(agg).sum().index,
            y=df.Count.resample(agg).sum(),
            marker=dict(
                color=df.Count.resample(agg).sum(),
                colorscale='Viridis'
            ),
            name='',
            hoverinfo=None,
        )],
        layout=go.Layout(
            title='Количество выписок по группированию',
            dragmode='pan'
        )
    )

@app.callback(
    Output('graphMon', 'figure'),
    [Input('dropdownMon', 'value')]
)
def udpateGraphMon(mons):
    return go.Figure(
        data=[
            go.Scatter(
                x=df[df.index.month==m].index.day,
                y=df[df.index.month==m].Count,
                mode='markers+lines',
                name=months[m],
            ) for m in mons
        ],
        layout=go.Layout(
            title='Количество выписок в разрезе месяцев',
            yaxis=dict(range=[df.Count.min(), df.Count.max()]),
            xaxis=dict(title='День месяца'),
            dragmode='pan',
        )
    )



@server.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return app.index()


@server.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run_server(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]

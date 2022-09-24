# load packages

import numpy as np
from dash import Dash, dash_table, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px

import fpl_league_table

# %% spoof here for input data...

visible_cols = [
    'player_name',
    'entry_name',
    'rank',
    'event_total',
    'total',
]

# Create app

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# %% App Layout

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Fantasy Premier League Table",
                        className='text-left text-primary'), width=10)
    ]),
    dbc.Row([
        dbc.Col(html.Div('Enter League Code'), ),
        dbc.Col(
            dcc.Input(id="lg_code", type='number', step=1, debounce=True
                      ), ),
    ]),
    dbc.Row([
        dbc.Col(html.H3("Game Week Scores",
                        className='text-left text-primary'), width=10)
    ]),
    html.Div(id='bar_container'),
    html.Br(),
    dbc.Row([
        dbc.Col(html.H3("Seasonal Scores",
                        className='text-left text-primary'), width=10)
    ]),
    html.Div(id='bar_container2'),
    html.Br(),
    html.Div(id='the_table'),
    html.Br(),
])

# App callbacks


@app.callback(
    [
        Output(component_id='bar_container', component_property='children'),
        Output(component_id='bar_container2', component_property='children'),
        Output(component_id='the_table', component_property='children')
    ],
    [
        Input(component_id='lg_code', component_property='value'),
    ]
)
def bar_charts(lg_code):
    if lg_code is None:
        raise PreventUpdate
    else:
        previous_week, current_week, next_week, current_average = fpl_league_table.fpl_game_weeks()
        league_name = fpl_league_table.fpl_league_name(lg_code)

        df = fpl_league_table.fpl_league_table(lg_code)
        df['rank_change'] = df['last_rank'] - df['rank']
        df['diff_to_avg'] = df['event_total'] - current_average
        df['above_avg'] = 0
        df['above_avg'] = np.where(df.diff_to_avg > 0, 1, 0)

        print(df)

        fig = dcc.Graph(id='bar-chart',
                        figure=px.bar(
                            data_frame=df,
                            x="player_name",
                            y='event_total',
                            text='event_total',
                            labels={"event_total": "Game Week Points"},
                            title="Game Week " + str(current_week) + ": Points",
                            color='above_avg', range_color=[0, 1],
                            color_continuous_scale=['firebrick', 'gold']
                        )
                        .update_layout(showlegend=False, xaxis={'categoryorder': 'total descending'})
                        .update_yaxes(range=[df['event_total'].min() * 0.8, df['event_total'].max() * 1.1])
                        )

        fig2 = dcc.Graph(id='bar-chart2',
                         figure=px.bar(
                             data_frame=df,
                             x="player_name",
                             y='total',
                             text='total',
                             labels={"total": "Total Points"},
                             title=str(league_name) + ':  Total Points',
                             color='rank_change', range_color=[df.rank_change.abs().max() * -1,
                                                               df.rank_change.abs().max()],
                             color_continuous_scale=px.colors.sequential.RdBu_r
                         )
                         .update_layout(showlegend=False, xaxis={'categoryorder': 'total descending'})
                         .update_yaxes(range=[df['total'].min() * 0.8, df['total'].max() * 1.1])
                         )

        display_table = dash_table.DataTable(
            id='datatable',
            columns=[
                {"name": i, "id": i}
                for i in visible_cols
            ],
            data=df.to_dict('records'),
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="single",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=25,
            style_cell={
                'minWidth': 95, 'maxWidth': 95, 'width': 95
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['player_name', 'entry_name']
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            }
        ),

        return fig, fig2, display_table


# App Run

if __name__ == '__main__':
    app.run_server(debug=False)

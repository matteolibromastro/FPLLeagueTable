import json as js
import requests as rq
import pandas as pd
import numpy as np


def fpl_league_table(league_id):
    page = 1
    fpl_leagues_api = 'https://fantasy.premierleague.com/api/leagues-classic/' + str(
        league_id) + '/standings?page_standings=' + str(page)
    fpldata = js.loads(rq.get(fpl_leagues_api).text)
    league_players = fpldata['standings']['results']
    while fpldata['standings']['has_next']:
        page = page + 1
        fpl_leagues_api = 'https://fantasy.premierleague.com/api/leagues-classic/' + str(
            league_id) + '/standings?page_standings=' + str(page)
        fpldata = js.loads(rq.get(fpl_leagues_api).text)
        for i in fpldata['standings']['results']:
            league_players.append(i)
    league_data = pd.DataFrame(league_players)
    league_data = league_data.sort_values(by=['event_total', ], ascending=[False, ])
    return league_data


def fpl_league_name(league_id):
    fpl_leagues_api = 'https://fantasy.premierleague.com/api/leagues-classic/'+str(league_id)+'/standings'
    fpldata = js.loads(rq.get(fpl_leagues_api).text)
    league_name = fpldata['league']['name']
    return league_name


def fpl_game_weeks():
    fpl_api = "https://fantasy.premierleague.com/api/bootstrap-static/"
    fpldata = js.loads(rq.get(fpl_api).text)
    fpl_events = fpldata['events']
    for i in np.arange(len(fpl_events)):
        if fpl_events[i]['is_previous']:
            previous_week = fpl_events[i]['id']
        if fpl_events[i]['is_current']:
            current_week = fpl_events[i]['id']
            current_average = fpl_events[i]['average_entry_score']
        if fpl_events[i]['is_next']:
            next_week = fpl_events[i]['id']
    return previous_week, current_week, next_week, current_average


def fpl_team_event_points(league_df):
    teams_points = {}
    for team, player in zip(league_df['entry'].to_list(), league_df['player_name'].to_list()):
        previous_week, current_week, next_week, current_average = FplGameWeeks()
        events = np.arange(1,current_week)
        team_id = team
        event_history = {}
        for event in events:
            team_history_api = 'https://fantasy.premierleague.com/api/entry/'+str(team_id)+'/event/'+str(event)+'/picks/'
            team_history = js.loads(rq.get(team_history_api).text)
            event_history[event] = team_history['entry_history']
        teams_points[player] = pd.DataFrame.from_dict(event_history).T
    return teams_points


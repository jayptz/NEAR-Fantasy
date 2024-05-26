from flask import Flask, request, render_template, jsonify
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
# from jinja2 import Environment

app = Flask(__name__)


def authenticate():
    sc = OAuth2(None, None, from_file='json/ouath2.json')
    return sc

# def multiply(value, factor):
#     return value * factor
# app.jinja_env.filters['multiply'] = multiply


def fetch_league_info(league_id):

    sc = authenticate()
    

    gm = yfa.Game(sc, 'nba')

    lg = gm.to_league(league_id)

    standings = lg.standings()

    data = {"standings": standings}

    team_data = {}

    for team_standings in standings:
        team_key = team_standings['team_key']
        team = lg.to_team(team_key)
        team_roster = team.roster()
        team_data[team_key] = team_roster

    with open('json/fantasy_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
    with open('json/fantasy_team_data.json', 'w') as json_file:
        json.dump(team_data, json_file, indent=4)



def read_json_data():
    with open('json/fantasy_data.json', 'r') as json_file:
        data = json.load(json_file)
    return data

def read_json_team_data():
    with open('json/fantasy_team_data.json', 'r') as json_file:
        team_data = json.load(json_file)
    return team_data



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        league_id = request.form['league_id']
        fetch_league_info(league_id)
        data = read_json_data()
        standings = data['standings']
        team_data = read_json_team_data()

        return render_template('index.html', standings=standings, team_data=team_data)
    return render_template('index.html')

@app.route('/rules')
def rules():
    return render_template('/rules.html')
    

if __name__ == '__main__':
    app.run(debug=True)

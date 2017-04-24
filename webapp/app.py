#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import logging
from logging import Formatter, FileHandler
from forms import LoginForm, InsertForm, PlayerYearForm, PlayerSearchForm, CollegeForm, CoachYearForm, categotyForm
import os
import Models
from flask_bootstrap import Bootstrap
from db_conn import db_conn_utils as dcu
import json
#from time import sleep

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

#SQLALCHEMY_DATABASE_URI = "oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl"

# Automatically tear down SQLAlchemy.
'''`
@app.teardown_request
def shutdown_session(exception=None
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def home():
    #return render_template('pages/placeholder.home.html')
    return render_template("cop5725_index.html")

@app.route('/counttuples')
def count():
    #working code:
    number = dcu.get_tuple_count()

    #data format:
    #number = [{'table': 'team', 'data': 30}, {'table': 'games', 'data': 4688}, {'table': 'stats', 'data': 121297}, {'table': 'seasons', 'data': 40}, {'table': 'players', 'data': 4448}, {'table': 'coach', 'data': 180}]
    #number = [{'data': 40},{'data': 30},{'data': 20}]
    return render_template("cop5725_count.html", number = number)

@app.route('/team')
def team():
    # '''
    # {'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'E', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'}
    # '''
    # # t = Team.query.get('ATL')
    # # json_data = jsonify(t.get_public())
    # # json_data = dcu.team_info()
    # # flash(json_data)
    teams = Models.Team.query.all()
    json_data = json.loads(json.dumps(Models.Team.serialize_list(teams)))

    return render_template("cop5725_team.html", json_data = json_data)

    #***************************************Test CODE*********************************************
    # dic = [{'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'E', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'},
    #        {'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'E', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'},
    #        {'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'W', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'},
    #        {'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'W', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'},
    #        {'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'W', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'},
    #        {'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'E', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'},
    #        {'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'E', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'}
    #        ]
    # json_data = json.loads(json.dumps(dic));
    # return render_template("cop5725_team.html", json_data = json_data)

@app.route('/team/show/<team_name_abbr>')
def showteam(team_name_abbr):
    teamdic = {
                'CLE': 'https://www.youtube.com/embed/YmZayeouEGg',
                'BOS': 'https://www.youtube.com/embed/nYW14SaTYOE',
                'TOR': 'https://www.youtube.com/embed/pre3EhNx9IQ',
                'WAS': 'https://www.youtube.com/embed/Dn04H4VAYh8',
                'ATL': 'https://www.youtube.com/embed/t7QFdDsI1jY',
                'MIL': 'https://www.youtube.com/embed/KMsA3tHXcm0',
                'IND': 'https://www.youtube.com/embed/FGnFOdrloc4',
                'CHI': 'https://www.youtube.com/embed/LekwCc_vZEw',
                'MIA': 'https://www.youtube.com/embed/Q9hrSS_CxZk',
                'DET': 'https://www.youtube.com/embed/pnpb80DFljo',
                'NOH': 'https://www.youtube.com/embed/xPM13hmjf1U',
                'NYK': 'https://www.youtube.com/embed/l3p-TKkvsuQ',
                'ORL': 'https://www.youtube.com/embed/HEdWsImBKSQ',
                'PHI': 'https://www.youtube.com/embed/9j88WP6PCmw',
                'BRK': 'https://www.youtube.com/embed/OL7D4RfUMRU',
                'GSW': 'https://www.youtube.com/embed/xWmW4lVXpSo',
                'SAS': 'https://www.youtube.com/embed/lImYbfXNAO4',
                'HOU': 'https://www.youtube.com/embed/FPzAYPmsWJo',
                'LAC': 'https://www.youtube.com/embed/HSeTN3HAQhk',
                'UTA': 'https://www.youtube.com/embed/2rxyFgZfuNE',
                'OKC': 'https://www.youtube.com/embed/ACkUya0TWFo',
                'MEM': 'https://www.youtube.com/embed/B-EtM4KuHSA',
                'POR': 'https://www.youtube.com/embed/_I4fUByw5OA',
                'DEN': 'https://www.youtube.com/embed/WP2P_pxSC8I',
                'CHA': 'https://www.youtube.com/embed/HljCpKlh-X0',
                'DAL': 'https://www.youtube.com/embed/xvH0sTN01Fk',
                'SAC': 'https://www.youtube.com/embed/VuOzYN3SC9s',
                'MIN': 'https://www.youtube.com/embed/ytVUfYA1cFI',
                'LAL': 'https://www.youtube.com/embed/dqGgVJb-9xo',
                'PHO': 'https://www.youtube.com/embed/whg91jBsX7k'
                }
    # '''
    # {'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'E', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'}
    # '''
    # # t = Team.query.get('ATL')
    # # json_data = jsonify(t.get_public())
    # # json_data = dcu.team_info()
    # # flash(json_data)
    teams = Models.Team.query.filter_by(team_name_abbr = team_name_abbr)
    json_data = json.loads(json.dumps(Models.Team.serialize_list(teams)))
    # name = json_data.team_name_abbr
    #flash(json_data[0])
    #dic = [{'stadium': 'Philips Arena', 'location': 'Atlanta', 'mascot': 'Harry the Hawk', 'team_name_abbr': 'ATL', 'name': 'Atlanta Hawks', 'conference': 'E', 'mascoticon': 'https://i.kinja-img.com/gawker-media/image/upload/s--XzaUcNcA--/c_scale,fl_progressive,q_80,w_800/slum1imo6mtlolhmhmvz.jpg', 'webpage': 'http://www.nba.com/teams/hawks', 'logo': 'http://i.cdn.turner.com/nba/nba/assets/logos/teams/primary/web/ATL.svg'}]
    #json_data = json.loads(json.dumps(dic));

    #############video process**************
    #set up a video library: retreive the video based on team abbr and pass the video location as url param

    return render_template("cop5725_team_show.html", json_data = json_data, teamdic = teamdic)

@app.route('/season')
def season():
    return render_template("cop5725_season.html")

@app.route('/season/show/<sid>')
def showSeason(sid):
    #get sid season data from db
    # with engine.begin() as conn:
    #     res = conn.execute("select * from seasons where s_id = '{}'".format(sid))
    #dd is data dictionary
    dd =dict()
    #**************Work code**********************
    dd['sid'] = sid
    res = dcu.select_all_where('seasons', sid)
    data = res.fetchone()
    res.close()
    #data insert to template
    mvp = data['mvp']
    champ = data['champion']
    rookie = data['best_rookie']
    score_leader = data['most_points'].split('(')
    sl_name = score_leader[0].strip()
    sl_pts = score_leader[1][:-1].strip()
    reb_leader = data['most_rebounds'].split('(')
    rl_name = reb_leader[0].strip()
    rl_rebs = reb_leader[1][:-1].strip()
    ast_leader = data['most_assists'].split('(')
    al_name = ast_leader[0].strip()
    al_ast = ast_leader[1][:-1].strip()
    ws_leader = data['most_win_shares'].split('(')
    ws_name = ws_leader[0].strip()
    ws_ws = ws_leader[1][:-1].strip()

    tabbr = dcu.get_teamabbr(champ)

    #l = [mvp, rookie, sl_name, rl_name, al_name]
    mvp_id = -1
    rookie_id = -1
    sl_id = -1
    al_id = -1
    rl_id = -1
    ws_id = -1

    x = json.loads(dcu.get_player_list(mvp))
    if len(x) != 0:
        mvp_id = x[0]['pid']

    y = json.loads(dcu.get_player_list(rookie))
    if len(y) != 0:
        rookie_id = y[0]['pid']

    z = json.loads(dcu.get_player_list(sl_name))
    if len(z) != 0:
        sl_id = z[0]['pid']

    m = json.loads(dcu.get_player_list(rl_name))
    if len(m) != 0:
        rl_id = m[0]['pid']

    n = json.loads(dcu.get_player_list(al_name))
    if len(n) != 0:
        al_id = n[0]['pid']

    b = json.loads(dcu.get_player_list(ws_name))
    if len(b) != 0:
        ws_id = b[0]['pid']

    dd['mvpid'] = mvp_id
    dd['rookieid'] = rookie_id
    dd['slid'] = sl_id
    dd['rlid'] = rl_id
    dd['alid'] = al_id
    dd['wsid'] = ws_id

    dd['mvp'] = mvp
    dd['champ'] = champ
    dd['rookie'] = rookie
    dd['sl_name'] = sl_name
    dd['sl_pts'] = sl_pts
    dd['rl_name'] = rl_name
    dd['rl_rebs'] = rl_rebs
    dd['al_name'] = al_name
    dd['al_ast'] = al_ast
    dd['ws_name'] = ws_name
    dd['ws_ws'] = ws_ws
    dd['mvp_image'] = "/" + dcu.get_player_image(mvp)[0]
    dd['rookie_image'] = "/" + dcu.get_player_image(rookie)[0]
    dd['score_leader_image'] = "/" + dcu.get_player_image(sl_name)[0]
    dd['reb_leader_image'] = "/" + dcu.get_player_image(rl_name)[0]
    dd['ast_leader_image'] = "/" + dcu.get_player_image(al_name)[0]
    dd['ws_leader_image'] = "/" + dcu.get_player_image(ws_name)[0]
    dd['champ_image'] = dcu.get_team_logo(champ)[0]

    #*********************  Test  *********************************************
    # dd['mvp'] = 'mvp'
    # dd['champ'] = 'champ'
    # dd['rookie'] = 'rookie'
    # dd['sl_name'] = 'sl_name'
    # dd['sl_pts'] = 'sl_pts'
    # dd['rl_name'] = 'rl_name'
    # dd['rl_rebs'] = 'rl_rebs'
    # dd['al_name'] = 'al_name'
    # dd['al_ast'] = 'al_ast'
    # dd['ws_name'] = 'ws_name'
    # dd['ws_ws'] = 'ws_ws'
    # dd['mvp_image'] = "/static/useful_pics/None.jpg"
    # dd['rookie_image'] = "/static/useful_pics/None.jpg"
    # dd['score_leader_image'] = "/static/useful_pics/None.jpg"
    # dd['reb_leader_image'] = "/static/useful_pics/None.jpg"
    # dd['ast_leader_image'] = "/static/useful_pics/None.jpg"
    # dd['ws_leader_image'] = "/static/useful_pics/None.jpg"
    # dd['champ_image'] = "/static/useful_pics/None.jpg"
    #***********************************************************************
    return render_template("cop5725_season_show.html", **dd, abbr = tabbr)
        # sid = sid, mvp = mvp, champ = champ,
        # rookie = rookie, sl_name = sl_name, sl_pts = sl_pts, rl_name = rl_name, rl_rebs = rl_rebs,
        # al_name = al_name, al_ast = al_ast, ws_name = ws_name, ws_ws = ws_ws, mvp_image = mvp_image)

#To do
@app.route('/player', methods=['GET', 'POST'])
def player():
    form1 = PlayerSearchForm()
    if form1.go.data and form1.validate_on_submit():
        player_name_search = form1.player_name.data
        return redirect(url_for('showplayer', name = player_name_search))

    # # select seasons form
    seasons = dcu.all_seasons()
    #seasons = [(1000, 1002),(2006, 2007)]

    form2 = PlayerYearForm()
    form2.edit_year(seasons)
    if form2.sub.data and form2.validate_on_submit():
        s_id = form2.year.data
        return redirect(url_for('player_year', year = s_id))
    #     #flash(s_id)

    #get all time score leader (first 5)
    sl_data = dcu.get_alltime_first5_leader("pts")
    '''
    [{'name':'Kevin Durant','stats':'28.55'}*5]
    '''
    #get all time rebound leader (first 5)
    rl_data = dcu.get_alltime_first5_leader("trb")

    #get all time assist leader (first 5)
    al_data = dcu.get_alltime_first5_leader("ast")

    return render_template("cop5725_player.html", form1 = form1, form2 = form2, sl = sl_data, rl = rl_data, al = al_data)

    #***************************************************Test Code***********************************************************
    # sl_data =   [{'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'}]
    # rl_data =[{'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'}]
    # al_data =[{'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'},
    #             {'name':'Kevin Durant','stats':'28.55'}]
    return render_template("cop5725_player.html" ,form1 = form1, form2 = form2, sl = sl_data, rl = rl_data, al = al_data)

@app.route('/advanced_search', methods=['GET', 'POST'])
def advanced_search():
    '''
    when you design the page, first to make sure the attributes (gator, sc, coach_record) below is not None or empty list
    if these case happen, show a sentence as "data not available"
    '''
    gator = None
    sc = None
    coach_record = None
    best_3 = None
    #1. search college players who won the nba champ
    '''
    [{'name': 'Mike Miller', 'team': 'Miami Heat', 'season': '2012-13'},
    {'name': 'Udonis Haslem', 'team': 'Miami Heat', 'season': '2012-13'},
    {'name': 'Mike Miller', 'team': 'Miami Heat', 'season': '2011-12'},
    {'name': 'Udonis Haslem', 'team': 'Miami Heat', 'season': '2011-12'},
    {'name': 'Corey Brewer', 'team': 'Dallas Mavericks', 'season': '2010-11'}]
    '''
    # colls = dcu.get_colleges()
    colls = [("empty", "Select"),('University of Florida','University of Florida'),('Gonzaga University','Gonzaga University'),
            ('University of Arizona','University of Arizona'),('California State University, Los Angeles','California State University, Los Angeles')]
    form1 = CollegeForm()
    form1.edit_coll(colls)
    coll = None
    if form1.sub1.data and form1.validate_on_submit():
        coll = form1.coll.data
    if coll is not None:
        gator = json.loads(dcu.get_college_champ_player_list(coll))

    #2. top 10 highest score in season
    '''
    [{'name': 'Brandon Jennings', 'age': 20, 'score': 55},
    {'name': 'Andre Miller', 'age': 34, 'score': 52},
    {'name': 'Carmelo Anthony', 'age': 25, 'score': 50},
    {'name': 'LeBron James', 'age': 25, 'score': 48},
    {'name': 'Kevin Martin', 'age': 27, 'score': 48},
    {'name': 'Vince Carter', 'age': 33, 'score': 48},
    {'name': 'Monta Ellis', 'age': 24, 'score': 46},
    {'name': 'Kevin Durant', 'age': 21, 'score': 45}]
    '''
    ss = None
    seasons = dcu.all_seasons()
    form2 = PlayerYearForm()
    form2.edit_year(seasons)
    if form2.sub.data and form2.validate_on_submit():
        ss = form2.year.data
    if ss is not None:
        sc = json.loads(dcu.get_highest_season_score(ss))

    #3. all time best 3point shooter (>400 made >0.4 percentage)
    '''
    [{'name': 'Ray Allen', 'pid': 56, 'fg3p': '0.4143', 'fg3a': '1832', 'fg3': '759'},
    {'name': 'Stephen Curry', 'pid': 839, 'fg3p': '0.4448', 'fg3a': '1450', 'fg3': '645'},
    {'name': 'Kyle Korver', 'pid': 2203, 'fg3p': '0.4359', 'fg3a': '1358', 'fg3': '592'},
    {'name': 'Mo Williams', 'pid': 4302, 'fg3p': '0.401', 'fg3a': '1429', 'fg3': '573'} ]
    '''
    models = [("empty", "Select"), ('ft', 'free throw'), ('fg', 'field goal'), ('fg3','3 pointer')]

    mm = None
    form4 = categotyForm()
    form4.edit_model(models)
    if form4.sub2.data and form4.validate_on_submit():
        mm = form4.model.data
    if mm is not None:
        best_3 = json.loads(dcu.get_player_top_goal_percentage(mm))

    #4. coach win in each season
    '''
    [{'coach': 'Tom Thibodeau', 'team': 'Chicago Bulls', 'win': 62}...]
    '''
    cc = None
    seasons1 = dcu.all_seasons()
    seasons1.pop(1)
    form3 = CoachYearForm()
    form3.edit_season(seasons1)
    if form3.submit.data and form3.validate_on_submit():
        cc = form3.seas.data
    if cc is not None:
        coach_record = json.loads(dcu.get_coach_win(cc))

    return render_template("cop5725_advanced_search.html", gator = gator, sc = sc, best_3 = best_3, coach_record = coach_record,
     form1 = form1, form2 = form2, form3 = form3, form4 = form4)

@app.route('/player/season/<year>', methods=['GET', 'POST'])
def player_year(year):
    form1 = PlayerSearchForm()
    if form1.go.data and form1.validate_on_submit():
        player_name_search = form1.player_name.data
        return redirect(url_for('showplayer', name = player_name_search))

    # select seasons form
    seasons = dcu.all_seasons()
    form2 = PlayerYearForm()
    form2.edit_year(seasons)
    if form2.sub.data and form2.validate_on_submit():
        s_id = form2.year.data
        return redirect(url_for('player_year', year = s_id))

    #get current season score leader (first 5)
    sl_data = dcu.get_season_first5_score_leader(year)
    #[{'name':'Kevin Durant','stats':'28.55'}*5]
    #if seasons data is more than stats data, we need to handle none case

    #get current season rebound leader (first 5)
    rl_data = dcu.get_season_first5_rebound_leader(year)

    #get current season assist leader (first 5)
    al_data = dcu.get_season_first5_assist_leader(year)

    return render_template("cop5725_player_season.html", form1 = form1, form2 = form2, year = year, sl = sl_data, rl = rl_data, al = al_data)

#you can skip this here for now, it will be a very simple page
@app.route('/player/searchlist/<name>')
def showplayer(name):
    ml = dcu.get_player_list(name)
    #decode json
    matched_list = json.loads(ml)
    #flash(matched_list)
    '''
    [{'pid': 327, 'name': 'James Blackwell'}, {'pid': 84, 'name': 'James Anderson'}]
    '''
    return render_template("cop5725_player_searchlist.html", matched = matched_list)

@app.route('/player/showplayer/<pid>')
def showplayerinfo(pid):
    if pid == -1:
        return redirect(url_for('inter`nal_error'))
    else:
        info = dcu.get_player_info(pid)
        total_stats = dcu.get_player_stats(pid)
        each_season_stats = dcu.get_player_eachseason_stats(pid)
    # '''
    # info data
    # {'position': 'F-G', 'name': 'LeBron James', 'headshot': 'static/useful_pics/LeBron James.png\n', 'pid': 1907, 'age': 33,
    #     'college': None, 'rookie_year': '2004', 'birthday': '1984-12-30', 'weight': 250, 'height': '6-8 '}


    # stats data
    # {'ast': '7.3', 'ft': '6.63', 'stl': '1.68', 'fta': '8.65', 'fg3': '1.36', 'player_name': 'LeBron James', 'fg': '9.9', 'blk': '0.9', 'orb': '1.2', 'trb': '7.64', 'tov': '3.28', 'fg3a': '3.89', 'player_id': '1907', 'fga': '19.11', 'drb': '6.45', 'pts': '27.79', 'pf': '1.68'}
    # #important!!! we have 'fgp', 'fg3p', 'ftp' also in data

    #队长请注意！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    #下面数据里的Decimal不知道为什么会报错！！！！！！！！！！！！！！！

    # each season data
    # [{'data': {'pname': 'LeBron James', 'fg3': '1.63'), 'stl': Decimal('1.69'), 'orb': Decimal('1.31'), 'fg3a': Decimal('4.74'), 'fta': Decimal('9.41'), 'drb': Decimal('6.26'), 'blk': Decimal('1.15'), 'pf': Decimal('1.72'), 'tov': Decimal('2.98'), 'ft': Decimal('7.33'), 'pts': Decimal('28.44'), 'pid': 1907, 'fg': Decimal('9.74'), 'trb': Decimal('7.57'), 'ast': Decimal('7.25'), 'fga': Decimal('19.91')}, 'season': '2008-09'},
    # {'data': {'pname': 'LeBron James', 'fg3': Decimal('1.7'), 'stl': Decimal('1.64'), 'orb': Decimal('0.93'), 'fg3a': Decimal('5.09'), 'fta': Decimal('10.17'), 'drb': Decimal('6.36'), 'blk': Decimal('1.01'), 'pf': Decimal('1.57'), 'tov': Decimal('3.43'), 'ft': Decimal('7.8'), 'pts': Decimal('29.71'), 'pid': 1907, 'fg': Decimal('10.11'), 'trb': Decimal('7.29'), 'ast': Decimal('8.57'), 'fga': Decimal('20.11')}, 'season': '2009-10'},
    # {'data': {'pname': 'LeBron James', 'fg3': Decimal('1.16'), 'stl': Decimal('1.57'), 'orb': Decimal('1.01'), 'fg3a': Decimal('3.53'), 'fta': Decimal('8.39'), 'drb': Decimal('6.46'), 'blk': Decimal('0.63'), 'pf': Decimal('2.06'), 'tov': Decimal('3.59'), 'ft': Decimal('6.37'), 'pts': Decimal('26.72'), 'pid': 1907, 'fg': Decimal('9.59'), 'trb': Decimal('7.47'), 'ast': Decimal('7.01'), 'fga': Decimal('18.8')}, 'season': '2010-11'},
    # {'data': {'pname': 'LeBron James', 'fg3': Decimal('0.87'), 'stl': Decimal('1.85'), 'orb': Decimal('1.52'), 'fg3a': Decimal('2.4'), 'fta': Decimal('8.1'), 'drb': Decimal('6.42'), 'blk': Decimal('0.81'), 'pf': Decimal('1.55'), 'tov': Decimal('3.44'), 'ft': Decimal('6.24'), 'pts': Decimal('27.15'), 'pid': 1907, 'fg': Decimal('10.02'), 'trb': Decimal('7.94'), 'ast': Decimal('6.24'), 'fga': Decimal('18.85')}, 'season': '2011-12'},
    # {'data': {'pname': 'LeBron James', 'fg3': Decimal('1.36'), 'stl': Decimal('1.7'), 'orb': Decimal('1.28'), 'fg3a': Decimal('3.34'), 'fta': Decimal('7.04'), 'drb': Decimal('6.75'), 'blk': Decimal('0.88'), 'pf': Decimal('1.45'), 'tov': Decimal('2.97'), 'ft': Decimal('5.3'), 'pts': Decimal('26.79'), 'pid': 1907, 'fg': Decimal('10.07'), 'trb': Decimal('8.03'), 'ast': Decimal('7.25'), 'fga': Decimal('17.82')}, 'season': '2012-13'}]
    # '''
    # return render_template("cop5725_player_showpage.html", info = info, total = total_stats, each_season = each_season_stats)
 #**************************************************Test code***********************************************************************
    #info = dcu.get_player_info(pid)
    #total_stats = dcu.get_player_stats(pid)
    #each_season_stats = dcu.get_player_eachseason_stats()

    # info = [{'position': 'F-G', 'name': 'LeBron James', 'headshot': 'static/useful_pics/LeBron James.png\n', 'pid': 1907, 'age': 33, 'college': None, 'rookie_year': '2004', 'birthday': '1984-12-30', 'weight': 250, 'height': '6-8 '}]

    #total_stats = [{'ast': '7.3', 'ft': '6.63', 'stl': '1.68', 'fta': '8.65', 'fg3': '1.36', 'player_name': 'LeBron James', 'fg': '9.9', 'blk': '0.9', 'orb': '1.2', 'trb': '7.64', 'tov': '3.28', 'fg3a': '3.89', 'player_id': '1907', 'fga': '19.11', 'drb': '6.45', 'pts': '27.79', 'pf': '1.68'}]
    # #important!!! we have 'fgp', 'fg3p', 'ftp' also in data
    # each_season_stats = [{'data': {'pname': 'LeBron James', 'fg3': '1.63', 'stl': '1.69', 'orb': '1.31', 'fg3a': '4.74', 'fta': '9.41', 'drb': '6.26', 'blk': '1.15', 'pf': '1.72', 'tov': '2.98', 'ft': '7.33', 'pts': '28.44', 'pid': 1907, 'fg': '9.74', 'trb': '7.57', 'ast': '7.25', 'fga': '19.91'}, 'season': '2008-09'},
    # {'data': {'pname': 'LeBron James', 'fg3': '1.7', 'stl': '1.64', 'orb': '0.93', 'fg3a': '5.09', 'fta': '10.17', 'drb': '6.36', 'blk': '1.01', 'pf': '1.57', 'tov': '3.43', 'ft': '7.8', 'pts': '29.71', 'pid': 1907, 'fg': '10.11', 'trb': '7.29', 'ast': '8.57', 'fga': '20.11'}, 'season': '2009-10'},
    # {'data': {'pname': 'LeBron James', 'fg3': '1.16', 'stl': '1.57', 'orb': '1.01', 'fg3a': '3.53', 'fta': '8.39', 'drb': '6.46', 'blk': '0.63', 'pf': '2.06', 'tov': '3.59', 'ft': '6.37', 'pts': '26.72', 'pid': 1907, 'fg': '9.59', 'trb': '7.47', 'ast': '7.01', 'fga': '18.8'}, 'season': '2010-11'},
    # {'data': {'pname': 'LeBron James', 'fg3': '0.87', 'stl': '1.85', 'orb': '1.52', 'fg3a': '2.4', 'fta': '8.1', 'drb': '6.42', 'blk': '0.81', 'pf': '1.55', 'tov': '3.44', 'ft': '6.24', 'pts': '27.15', 'pid': 1907, 'fg': '10.02', 'trb': '7.94', 'ast': '6.24', 'fga': '18.85'}, 'season': '2011-12'},
    # {'data': {'pname': 'LeBron James', 'fg3': '1.36', 'stl': '1.7', 'orb': '1.28', 'fg3a': '3.34', 'fta': '7.04', 'drb': '6.75', 'blk': '0.88', 'pf': '1.45', 'tov': '2.97', 'ft': '5.3', 'pts': '26.79', 'pid': 1907, 'fg': '10.07', 'trb': '8.03', 'ast': '7.25', 'fga': '17.82'}, 'season': '2012-13'}]
    return render_template("cop5725_player_showpage.html", info = info, total = total_stats, each_season = each_season_stats)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    flag = 0
    form = LoginForm()
    if form.validate_on_submit():
        admin = Models.Admin.query.filter_by(admin_= form.name.data).first()
        #validate = Admin.query.filter_by(pwd = form.password.data).first()
        if admin is not None:
            if admin.check_password(form.password.data):
                return redirect(url_for('backend'))
            else:
                flag = 2
        else:
            flag = 1
    if flag == 0:
        pass
    elif flag == 1:
        flash("admin name is not correct!")
    else:
        flash("password is not correct!")
    return render_template('cop5725_login.html', form = form)

@app.route('/backend', methods=['GET', 'POST'])
def backend():
    form = InsertForm()
    flag_inputerr = 0
    if form.validate_on_submit():
        # process the data collected from the input form into json format
        #data categorized into
        #{home:{"p1":{"pts":xx, "ast":xx...}, "p2":{...}...},
        # away:{"p1":{"pts":xx, "ast":xx...}...}}
        home_team = form.h_team.data
        away_team = form.a_team.data
        date = form.date.data
        #all the data need from stats (TODO: complete all)
        stats = ["pts", "rb", "ast"]

        data_dict = dict()
        home = dict()
        away = dict()
        data_dict[home_team] = home
        data_dict[away_team] = away

        hps = form.home_team_player.data
        try:
            for each_pd in hps.split(";"):
                i = 0
                temp = dict()
                data = each_pd.split("(")
                home[data[0].strip()] = temp

                stats_data = data[1][:-1].split(",")
                for d in stats_data:
                    temp[stats[i]] = int(d)
                    i += 1

            aps = form.away_team_player.data
            for each_pd in aps.split(";"):
                i = 0
                temp = dict()
                data = each_pd.split("(")
                away[data[0].strip()] = temp

                stats_data = data[1][:-1].split(",")
                for d in stats_data:
                    temp[stats[i]] = int(d)
                    i += 1
        except:
            flag_inputerr = 1

        if flag_inputerr:
            flash("insert data has error!")
        else:
            #create connection with db
            engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
            #the following code is example code to show how to interact with db
            for each in data_dict[home_team].keys():
                pts = 0
                rb = 0
                ast = 0
                for st in data_dict[home_team][each].keys():
                    d = data_dict[home_team][each][st]
                    if st == 'pts':
                        pts = d
                    elif st == 'rb':
                        rb = d
                    else:
                        ast = d
                with engine.begin() as conn:
                    conn.execute("insert into test values('{}','{}',{},{},{})"
                        .format(home_team,each,pts,rb,ast))

            for each in data_dict[away_team].keys():
                pts = 0
                rb = 0
                ast = 0
                for st in data_dict[away_team][each].keys():
                    d = data_dict[away_team][each][st]
                    if st == 'pts':
                        pts = d
                    elif st == 'rb':
                        rb = d
                    else:
                        ast = d
                with engine.begin() as conn:
                    conn.execute("insert into test values('{}','{}',{},{},{})"
                        .format(away_team,each,pts,rb,ast))
            #example finished here

            #import data into database

            flash("insert data success!")
        #return to empty page
        return redirect(url_for('backend'))
    return render_template('cop5725_backend.html', form = form)

# @app.route('/register')
# def register():
#     form = RegisterForm(request.form)
#     return render_template('forms/register.html', form=form)


# @app.route('/forgot')
# def forgot():
#     form = ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
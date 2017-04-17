from sqlalchemy import create_engine
import datetime
import json

class db_conn_utils:
	SQLALCHEMY_DATABASE_URI = "oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl"
	engine = create_engine(SQLALCHEMY_DATABASE_URI)

	@classmethod
	def get_teamabbr(cls, name):
		with cls.engine.begin() as conn:
			res = conn.execute("select team_name_abbr from team where name = '{}'".format(name)).first()
		return res[0]

	@classmethod
	def _get_season_start_end_date(cls, s_id):
		if s_id == '2009-10':
			return ['01-OCT-09', '01-JUL-10']
		elif s_id == '2010-11':
			return ['01-OCT-10', '01-JUL-11']
		elif s_id == '2011-12':
			return ['01-OCT-11', '01-JUL-12']
		elif s_id == '2012-13':
			return ['01-OCT-12', '01-JUL-13']
		elif s_id == '2008-09':
			return ['01-OCT-08', '01-JUL-09']
		else:
			None

	@classmethod
	def get_team_logo(cls, condition):
		with cls.engine.begin() as conn:
			res = conn.execute("select logo from team where name like '{}'".format(condition))
			for row in res:
				if row != None:
					return row

	@classmethod
	def get_player_image(cls, condition):
		with cls.engine.begin() as conn:
			names = condition.split(".")
			new_condition = names[0] + "%" + names[1].lstrip()
			res = conn.execute("select player_headshot from players where name like '{}'".format(new_condition))
			for row in res:
				if row[0] is not None:
					return row

			return ("static/useful_pics/None.jpg\n",)

	@classmethod
	def select_all_where(cls, db, condition):
		with cls.engine.begin() as conn:
			res = conn.execute("select * from {} where s_id = '{}'".format(db, condition))
		return res

	@classmethod
	def insert_data(cls, db, dataList):
		end_index = len(dataList) - 1
		insertData = ""
		for i, data in enumerate(dataList):
			if data.isdigit():
				insertData += data
			else:
				insertData = insertData + "'" + data + "'"
			if i != end_index:
				insertData += ","
		with cls.engine.begin() as conn:
			conn.execute("insert into {} values ({})".format(db, insertData))

	@classmethod
	def team_info(cls):
		with cls.engine.begin() as conn:
			res = conn.execute("select * from team")
			l = []
			d = dict()
			for k in res.keys():
				l.append(k)
			for row in res:
				d1 = dict()
				for i, each in enumerate(row):
					if(i == 0):
						d[each] = d1
					else:
						d1[l[i]] = each
		return d

	@classmethod
	def all_seasons(cls):
		l = [()]
		with cls.engine.begin() as conn:
			res = conn.execute("select s_id from seasons where s_id between '2008-09' and '2012-13'")
		# for each in res:
		# 	l.append(each[0])
		l = [(each[0], each[0]) for each in res]
		l.insert(0, ("empty", "Select"))
		res.close()
		return l

	@classmethod
	def get_alltime_first5_leader(cls, field):
		start_date = "01-OCT-09"
		end_date = "01-JUL-13"

		sql = "select * from (select player_name, ROUND(AVG({}),2) as points_avg from STATS where date_ BETWEEN '{}' and '{}' group by player_id, player_name order by points_avg desc) where rownum <6".format(field, start_date, end_date)

		data = []
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		for each in res:
			d = dict()
			d["name"] = each[0]
			d["stats"] = str(each[1])
			data.append(d)
		res.close()
		return data

	@classmethod
	def get_all_time_best_3point_shooter(cls):
		sql = "select player_name, stats.PLAYER_ID, sum(FG3) as threep_made,ROUND((sum(FG3)/sum(FG3A)),4) as threep_percent, sum(fg3a) as atp from stats, players where STATS.player_id=Players.player_id group by stats.player_id, stats.player_name, players.POS having sum(FG3A)>0 and sum(FG3)>400 and (sum(FG3)/sum(FG3A))> 0.4 order by threep_made desc, threep_percent desc"
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		l = []
		for each in res:
			d = dict()
			d['name'] = each[0]
			d['pid'] = each[1]
			d['fg3'] = str(each[2])
			d['fg3p'] = str(each[3])
			d['fg3a'] = str(each[4])
			l.append(d)
		return json.dumps(l)

	# unused in this project
	@classmethod
	def get_player_top_goal_percentage(cls, g):
		if g == 'fg':
			tol = 1000
			per = 0.55
		elif g == 'ft':
			tol = 1000
			per = 0.85
		elif g == 'fg3':
			tol = 400
			per = 0.4
		a = g + "a"
		p = g + "p"
		sql = "select player_name, stats.PLAYER_ID, sum({g}) as threep_made, ROUND((sum({g})/sum({a})),4) as threep_percent, sum({a}) as atp from stats, players where STATS.player_id=Players.player_id group by stats.player_id, stats.player_name, players.POS having sum({a})>0 and sum({g})>{tol} and (sum({g})/sum({a}))> {per} order by threep_made desc, threep_percent desc".format(a=a,g=g,tol=tol,per=per)
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		l = []
		for each in res:
			d = dict()
			d['name'] = each[0]
			d['pid'] = each[1]
			d['made'] = str(each[2])
			d['per'] = str(each[3])
			d['att'] = str(each[4])
			l.append(d)
		return json.dumps(l)

	@classmethod
	def get_coach_win(cls, sid):
		start_end = cls._get_season_start_end_date(sid)
		if start_end is None:
			return None
		start = start_end[0]
		end = start_end[1]

		sql = "select coach.name as coach, team.name as team, count(games.WIN_TEAM) as win from  games, team, coach where games.gamedate BETWEEN '{}' and '{}' and coach.year='{}' and team.TEAM_NAME_ABBR= games.win_team and coach.TEAM=team.TEAM_NAME_ABBR group by games.WIN_TEAM, team.name, coach.name order by win desc".format(start,end,sid)

		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		l = []
		for each in res:
			d = dict()
			d['coach'] = each[0]
			d['team'] = each[1]
			d['win'] = each[2]
			l.append(d)
		return json.dumps(l)

	@classmethod
	def get_highest_season_score(cls, s_id):
		start_end = cls._get_season_start_end_date(s_id)
		if start_end is None:
			return None
		start = start_end[0]
		end = start_end[1]
		sql = "select * from (select distinct stats.player_name, ROUND(months_between(date_, birthdate )/12,0) as age, max(pts) from stats, players where STATS.player_id=Players.player_id and date_ BETWEEN '{}' and '{}' group by stats.player_id, stats.player_name, ROUND(months_between(date_, birthdate )/12,0) order by max(pts) desc, age asc) where rownum<11".format(start, end)
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		l = []
		for each in res:
			d = dict()
			d['name'] = each[0]
			d['age'] = each[1]
			d['score'] = each[2]
			l.append(d)
		return json.dumps(l)

	@classmethod
	def get_season_first5_score_leader(cls, s_id):
		start_end = cls._get_season_start_end_date(s_id)
		if start_end is None:
			return None
		start_date = start_end[0]
		end_date = start_end[1]

		sql = "select * from (select player_name, ROUND(AVG(pts),2) as points_avg from STATS where date_ BETWEEN '{}' and '{}' group by player_id, player_name order by points_avg desc) where rownum <6".format(start_date, end_date)

		data = []
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		for each in res:
			d = dict()
			d["name"] = each[0]
			d["stats"] = str(each[1])
			data.append(d)
		res.close()
		return data

	@classmethod
	def get_season_first5_rebound_leader(cls, s_id):
		start_end = cls._get_season_start_end_date(s_id)
		if start_end is None:
			return None
		start_date = start_end[0]
		end_date = start_end[1]

		sql = "select * from (select player_name, ROUND(AVG(TRB),2) as rebounds_avg from STATS where  date_ BETWEEN '{}' and '{}' group by player_id, player_name order by rebounds_avg desc) where rownum <6".format(start_date, end_date)

		data = []
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		for each in res:
			d = dict()
			d["name"] = each[0]
			d["stats"] = str(each[1])
			data.append(d)
		res.close()
		return data

	@classmethod
	def get_season_first5_assist_leader(cls, s_id):
		start_end = cls._get_season_start_end_date(s_id)
		if start_end is None:
			return None
		start_date = start_end[0]
		end_date = start_end[1]

		sql = "select * from (select player_name, ROUND(AVG(ast),2) as assists_avg from STATS where  date_ BETWEEN '{}' and '{}' group by player_id, player_name order by assists_avg desc) where rownum <6".format(start_date, end_date)

		data = []
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		for each in res:
			d = dict()
			d["name"] = each[0]
			d["stats"] = str(each[1])
			data.append(d)
		res.close()
		return data

	@classmethod
	def get_player_list(cls, name):
		np = name.split(" ")
		name_pattern = ""

		if(len(np) == 1):
			name_pattern = name_pattern + "%" + np[0].capitalize() + "%"
		else:
			for each in np:
				if each.endswith("."):
					each = each[:-1]
				name_pattern = name_pattern + each.capitalize() + "%"

		sql = "select name, player_id from players where name like '{}' and from_ < 2013 and to_ > 2007".format(name_pattern)
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		#format data to json string(encode json)
		l = []
		for each in res:
			d = dict()
			d["name"] = each[0]
			d["pid"] = each[1]
			l.append(d)
		data = json.dumps(l)

		res.close()
		return data

	@classmethod
	def get_player_info(cls, pid):
		sql = "select * from players where player_id = {}".format(pid)

		with cls.engine.begin() as conn:
			res = conn.execute(sql).first()
		if res is not None:
			d = dict()
			d['pid'] = res[0]
			d['name'] = res[1]
			d['position'] = res[4]
			d['rookie_year'] = res[2]
			d['height'] = res[5]
			d['college'] = res[6]
			d['birthday'] = res[7].isoformat()[:10]
			d['weight'] = res[8]
			d['headshot'] = res[9]
			d['age'] = datetime.datetime.now().year - int(res[7].isoformat()[:4])
			return d
		else:
			return None

	@classmethod
	def get_player_stats(cls, pid):
		sql = "select player_id,player_name,round(avg(ast),2),round(avg(blk),2),round(avg(fg),2),round(avg(fg3),2),round(avg(ft),2),round(avg(fga),2),round(avg(fta),2),round(avg(fg3a),2),round(avg(pf),2),round(avg(pts),2),round(avg(stl),2),round(avg(tov),2),round(avg(orb),2),round(avg(drb),2),round(avg(trb),2)from stats where player_id = {} group by player_id, player_name".format(pid)
		d = dict()
		l = ["pid","pname","ast","blk","fg","fg3","ft","fga","fta","fg3a","pf","pts","stl","tov","orb","drb","trb"]
		with cls.engine.begin() as conn:
			res = conn.execute(sql).first()
		if res is not None:
			for i in range(len(l)):
				d[l[i]] = res[i]
			if d['fga'] != 0:
				d['fgp'] = '{percent:.2%}'.format(percent=d['fg']/d['fga'])
			else:
				d['fgp'] = '0%'
			if d['fg3a'] != 0:
				d["fg3p"] = '{percent:.2%}'.format(percent=d['fg3']/d['fg3a'])
			else:
				d['fg3p'] = '0%'
			if d['fta'] != 0:
				d["ftp"] = '{percent:.2%}'.format(percent=d['ft']/d['fta'])
			else:
				d['ftp'] = '0%'
			return d
		else:
			return None

	@classmethod
	def get_player_eachseason_stats(cls, pid):
		s = ['2008-09', '2009-10', '2010-11', '2011-12', '2012-13']
		l = ["pid","pname","ast","blk","fg","fg3","ft","fga","fta","fg3a","pf","pts","stl","tov","orb","drb","trb"]
		result = []
		with cls.engine.begin() as conn:
			for each_s in s:
				d = dict()
				start_end = cls._get_season_start_end_date(each_s)
				start = start_end[0]
				end = start_end[1]
				sql = "select player_id,player_name,round(avg(ast),2),round(avg(blk),2),round(avg(fg),2),round(avg(fg3),2),round(avg(ft),2),round(avg(fga),2),round(avg(fta),2),round(avg(fg3a),2),round(avg(pf),2),round(avg(pts),2),round(avg(stl),2),round(avg(tov),2),round(avg(orb),2),round(avg(drb),2),round(avg(trb),2)from stats where player_id = {} and date_ BETWEEN '{}' and '{}' group by player_id, player_name".format(pid, start, end)
				res = conn.execute(sql).first()
				if res is not None:
					temp = dict()
					for i in range(len(l)):
						temp[l[i]] = res[i]
					if temp['fga'] != 0:
						temp["fgp"] = '{percent:.2%}'.format(percent=temp["fg"]/temp['fga'])
					else:
						temp['fgp'] = '0%'
					if temp['fg3a'] != 0:
						temp["fg3p"] = '{percent:.2%}'.format(percent=temp['fg3']/temp['fg3a'])
					else:
						temp['fg3a'] = '0%'
					if temp['fta'] != 0:
						temp["ftp"] = '{percent:.2%}'.format(percent=temp['ft']/temp['fta'])
					else:
						temp['fta'] = '0%'
					d["season"] = each_s
					d["data"] = temp
					result.append(d)
		return result

	@classmethod
	def get_tuple_count(cls):
		l = []
		tables = ['team', 'games', 'stats', 'seasons', 'players', 'coach']
		with cls.engine.begin() as conn:
			for table in tables:
				s1 = "select count(*) from {}".format(table)
				res = conn.execute(s1).first()
				d = dict()
				d['table'] = table
				d['data'] = res[0]
				l.append(d)
		return l

	@classmethod
	def get_college_champ_player_list(cls, coll):
		sql = "select distinct players.NAME, team.name as T_name, s_id from players, seasons, team, stats where (((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-08' and '01-JUL-09'and s_id= '2008-09')) or ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-09' and '01-JUL-10'and s_id= '2009-10')) or ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-10' and '01-JUL-11'and s_id= '2010-11')) or ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-11' and '01-JUL-12'and s_id= '2011-12')) or ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-12' and '01-JUL-13'and s_id= '2012-13'))) and Players.college='{}' and players.PLAYER_ID= stats.player_id order by s_id desc".format(coll)
		l = []
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
			for each in res:
				d = dict()
				d['name'] = each[0]
				d['team'] = each[1]
				d['season'] = each[2]
				l.append(d)

		data = json.dumps(l)
		return data

	@classmethod
	def get_colleges(cls):
		sql = "select distinct college from players where college is not null"
		with cls.engine.begin() as conn:
			res = conn.execute(sql)
		l = [()]
		l = [(each[0], each[0]) for each in res]
		l.insert(0, ("empty", "Select"))
		return l
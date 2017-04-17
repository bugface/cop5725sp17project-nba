from sqlalchemy import create_engine
from models import Team
from flask import jsonify
import json
import datetime

def test_dict():
	s1 = "alex(10,5,10);budd(1,2,3);candy(4,5,6);do(8,10,12)"
	s2 = "yao ming(10,5,10);wang zhi(1,2,3);da hua(4,5,6);li si(8,10,12)"

	d1 = dict()
	d2 = dict()
	d = dict()

	list = ["pts", "reb", "ast"]

	d["s1"] = d1
	d["s2"] = d2

	for each in s1.split(";"):
		d11 = dict()
		datas = each.split("(")
		d1[datas[0]] = d11
		i = 0

		for data in datas[1][:-1].split(","):
			d11[list[i]] = int(data)
			i += 1

	for each in s2.split(";"):
		d21 = dict()
		datas = each.split("(")
		d2[datas[0]] = d21
		i = 0

		for data in datas[1][:-1].split(","):
			d21[list[i]] = int(data)
			i += 1
	print(d)

def test_process_data(season):
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute("select * from seasons where s_id = '{}'".format(season))
	print(res)
	print("*"*10)
	print("season\t\tchamp\t\tmvp\t\tscore_leader")
	for row in res:
		print("{}\t\t{}\t\t{}\t\t{}".format(row["s_id"],row["champion"],row["mvp"],row["most_points"]))

def get_player_image(condition):
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		names = condition.split(".")
		new_condition = names[0] + "%" + names[1].lstrip()
		res = conn.execute("select player_headshot from players where name like '{}'".format(new_condition))
	for row in res:
		print(row)
		if row[0] is not None:
			res.close()
			return row
	res.close()
	return ("static/useful_pics/None.jpg\n",)

# def get_team():
# 	# data = Team.query.all()
# 	# result = [d.__dict__ for d in data]
# 	# return jsonify(result=result)
def get_team():
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute("select * from team")
	l = []
	d = dict()
	for k in res.keys():
		l.append(k)
	print(l)
	for row in res:
		d1 = dict()
		for i, each in enumerate(row):
			print(i)
			print(each)
			if(i == 0):
				d[each] = d1
			else:
				d1[l[i]] = each

	print(d)

def all_season():
	l = []
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute("select s_id from seasons")
	l = [(each[0],each[0]) for each in res]
	l.insert(0, ("Select",None))
	res.close()
	return l

def avg(field):
	d = []
	start_date = "01-OCT-09"
	end_date = "01-JUL-10"
	#sql = "select * from (select player_name, ROUND(AVG(pts),2) as points_avg from STATS where date_ BETWEEN '{}' and '{}' group by player_id, player_name order by points_avg desc) where rownum <6".format(start_date, end_date)
	sql = "select * from (select player_name, ROUND(AVG({}),2) as points_avg from STATS where date_ BETWEEN '{}' and '{}' group by player_id, player_name order by points_avg desc) where rownum <6".format(field, start_date, end_date)

	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute(sql)
	for each in res:
		d.append(each)
	res.close()
	return d

def proc():
	name = "James"
	np = name.split(" ")
	name_pattern = ""
	for each in np:
		name_pattern = name_pattern + each + "%"
	# s = [{'Kevin Durant': '28.55'}, {'LeBron James': '27.6'}, {'Kobe Bryant': '26.8'}, {'Carmelo Anthony': '26.45'}, {'Dwyane Wade': '24.1'}]
	# # for each in s:
	# # 	keys = each.keys()
	# # 	for each1 in keys:
	# # 		print(each[each1])
	# j = json.dumps(s)
	# print(j)

	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	l = []
	with engine.begin() as conn:
		res = conn.execute("select name, player_id from PLAYERS where name like '{}'".format(name_pattern))
	print(res)
	for each in res:
		d = dict()
		d["name"] = each[0]
		d["id"] = each[1]
		l.append(d)
	d = json.dumps(l)
	m = json.loads(d)
	print(m[0]["name"])

def test_player1():
	pid = 1907
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	d = dict()
	sql = "select player_id,player_name,round(avg(ast),2),round(avg(blk),2),round(avg(fg),2),round(avg(fg3),2),round(avg(ft),2),round(avg(fga),2),round(avg(fta),2),round(avg(fg3a),2),round(avg(pf),2),round(avg(pts),2),round(avg(stl),2),round(avg(tov),2),round(avg(orb),2),round(avg(drb),2),round(avg(trb),2)from stats where player_id = {} group by player_id, player_name".format(pid)

	with engine.begin() as conn:
		res = conn.execute(sql).first()
	l = ["player_id","player_name","ast","blk","fg","fg3","ft","fga","fta","fg3a","pf","pts","stl","tov","orb","drb","trb"]
	for i in range(len(l)):
		d[l[i]] = res[i]
	print(d)
	print(str(int(round(d["fg3"]/d["fg3a"],2)*100)) + "%")
	print('{percent:.2%}'.format(percent=d['fg3']/d['fg3a']))
	print(d["fg"])

	print('{percent:.2%}'.format(percent=d['fg']/d['fga']))
	print('{percent:.2%}'.format(percent=d['fg3']/d['fg3a']))
	print('{percent:.2%}'.format(percent=d['ft']/d['fta']))
	# print(res[7].isoformat()[:10])
	# age = datetime.datetime.now().year - int(res[7].isoformat()[:4])
	# print(age)
	# #j = json.dumps(res)
	# #print(j)
def _get_season_start_end_date(s_id):
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

def new_test():
	pid = 211
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	s = ['2008-09', '2009-10', '2010-11', '2011-12', '2012-13']
	l = ["pid","pname","ast","blk","fg","fg3","ft","fga","fta","fg3a","pf","pts","stl","tov","orb","drb","trb"]
	#li = []
	d = dict()
	with engine.begin() as conn:
		for each_s in s:
			#d = dict()

			start_end = _get_season_start_end_date(each_s)
			start = start_end[0]
			end = start_end[1]
			sql = "select player_id,player_name,round(avg(ast),2),round(avg(blk),2),round(avg(fg),2),round(avg(fg3),2),round(avg(ft),2),round(avg(fga),2),round(avg(fta),2),round(avg(fg3a),2),round(avg(pf),2),round(avg(pts),2),round(avg(stl),2),round(avg(tov),2),round(avg(orb),2),round(avg(drb),2),round(avg(trb),2)from stats where player_id = {} and date_ BETWEEN '{}' and '{}' group by player_id, player_name".format(pid, start, end)
			res = conn.execute(sql).first()
			if res is not None:
				temp = dict()
				for i in range(len(l)):
					temp[l[i]] = res[i]
				#d["season"] = each_s
				#d["data"] = temp
				d[each_s] = temp
				#li.append(d)
				k = temp['fg']/temp['fga']

	print(d)

def count():
	#s1 = "select count(*) from {}".format()
	l = []
	tables = ['team', 'games', 'stats', 'seasons', 'players', 'coach']
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		for table in tables:
			s1 = "select count(*) from {}".format(table)
			res = conn.execute(s1).first()
			d = dict()
			d['table'] = table
			d['data'] = res[0]
			l.append(d)

	print(l)

def test1(name):
	np = name.split(" ")
	print(len(np))
	name_pattern = ""
	if(len(np) == 1):
		name_pattern = name_pattern + "%" + np[0].capitalize() + "%"
	else:
		for each in np:
			#print(each)
			if each.endswith("."):
				each = each[:-1]
			name_pattern = name_pattern + each.capitalize() + "%"

	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	sql = "select name, player_id from players where name like '{}' and from_ < 2013 and to_ > 2007".format(name_pattern)
	with engine.begin() as conn:
		res = conn.execute(sql)

	l = []
	for each in res:
		d = dict()
		d["name"] = each[0]
		d["pid"] = each[1]
		print(d)
		l.append(d)
	data = json.dumps(l)
	return data


def test2():
	l = []

	sql = "select distinct players.NAME, team.name as T_name, s_id from players, seasons, team, stats where (((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-08' and '01-JUL-09'and s_id= '2008-09')) or ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-09' and '01-JUL-10'and s_id= '2009-10')) or ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-10' and '01-JUL-11'and s_id= '2010-11')) or ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-11' and '01-JUL-12'and s_id= '2011-12')) or ((seasons.champion= team.name and team.team_name_abbr= stats.team) and (date_ BETWEEN '01-OCT-12' and '01-JUL-13'and s_id= '2012-13'))) and Players.college='{}' and players.PLAYER_ID= stats.player_id order by s_id desc".format("University of Florida")

	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute(sql)
	for each in res:
		d = dict()
		d['name'] = each[0]
		d['team'] = each[1]
		d['season'] = each[2]
		l.append(d)
	print(l)

def test3():
	sql = "select distinct college from players where college is not null"
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute(sql)
	for each in res:
		print(each)

def test4():
	start = '01-OCT-09'
	end = '01-JUN-10'
	sql = "select * from (select distinct stats.player_name, ROUND(months_between(date_, birthdate )/12,0) as age, max(pts) from stats, players where STATS.player_id=Players.player_id and date_ BETWEEN '{}' and '{}' group by stats.player_id, stats.player_name, ROUND(months_between(date_, birthdate )/12,0) order by max(pts) desc, age asc) where rownum<11".format(start, end)

	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute(sql)
	l = []
	for each in res:
		d = dict()
		d['name'] = each[0]
		d['age'] = each[1]
		d['score'] = each[2]
		l.append(d)
	return json.dumps(l)

def test5():
	sql = "select player_name, stats.PLAYER_ID, sum(FG3) as threep_made,ROUND((sum(FG3)/sum(FG3A)),4) as threep_percent, sum(fg3a) as atp from stats, players where STATS.player_id=Players.player_id group by stats.player_id, stats.player_name, players.POS having sum(FG3A)>0 and sum(FG3)>400 and (sum(FG3)/sum(FG3A))> 0.4 order by threep_made desc, threep_percent desc"
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
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

def test7():
	g = "ft"
	a = g + "a"
	p = g + "p"
	tol = 1000
	per = 0.85
	sql = "select player_name, stats.PLAYER_ID, sum({g}) as threep_made, ROUND((sum({g})/sum({a})),4) as threep_percent, sum({a}) as atp from stats, players where STATS.player_id=Players.player_id group by stats.player_id, stats.player_name, players.POS having sum({a})>0 and sum({g})>{tol} and (sum({g})/sum({a}))> {per} order by threep_made desc, threep_percent desc".format(a=a,g=g,tol=tol,per=per)
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute(sql)
	l = []
	for each in res:
		d = dict()
		d['name'] = each[0]
		d['pid'] = each[1]
		d[g] = str(each[2])
		d[p] = str(each[3])
		d[a] = str(each[4])
		l.append(d)
	return json.dumps(l)

def test6():
	sid = '2010-11'
	start = '01-OCT-10'
	end = '01-JUN-11'
	sql = "select coach.name as coach, team.name as team, count(games.WIN_TEAM) as win from  games, team, coach where games.gamedate BETWEEN '{}' and '{}' and coach.year='{}' and team.TEAM_NAME_ABBR= games.win_team and coach.TEAM=team.TEAM_NAME_ABBR group by games.WIN_TEAM, team.name, coach.name order by win desc".format(start,end,sid)
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute(sql)
	l = []
	for each in res:
		d = dict()
		d['coach'] = each[0]
		d['team'] = each[1]
		d['win'] = each[2]
		l.append(d)
	return json.dumps(l)

def test8():
	print("{0}{1}{1}{0}".format("a","b"))

def test9():
	engine = create_engine("oracle://xiyang:alex1988@oracle.cise.ufl.edu/orcl")
	with engine.begin() as conn:
		res = conn.execute("select team_name_abbr from team where name = 'Atlanta Hawks'").first()
	print(res[0])

def main():
	#test_dict()
	#test_process_data("2014-15")
	# a = get_player_image("S.Curry")
	# print("/" + a[0])
	#get_team()
	#print(all_season())
	# a = avg("trb")
	# l = []
	# for each in a:
	# 	d = dict()
	# 	d[each[0]] = each[1]
	# 	l.append(d)
	# print(l)
	#proc()
	#test_player1()
	#count()
	# a = json.loads(test1("L. James"))
	# print(a[0]['pid'])
	#test2()
	#new_test()
	#test3()
	#test6()
	# a = json.loads(test7())
	# print(a)
	#test8()
	test9()


if __name__ == '__main__':
	main()

#type 1:
'''
[{'data': {'pname': 'LeBron James', 'fg3': Decimal('1.63'), 'stl': Decimal('1.69'), 'orb': Decimal('1.31'), 'fg3a': Decimal('4.74'), 'fta': Decimal('9.41'), 'drb': Decimal('6.26'), 'blk': Decimal('1.15'), 'pf': Decimal('1.72'), 'tov': Decimal('2.98'), 'ft': Decimal('7.33'), 'pts': Decimal('28.44'), 'pid': 1907, 'fg': Decimal('9.74'), 'trb': Decimal('7.57'), 'ast': Decimal('7.25'), 'fga': Decimal('19.91')}, 'season': '2008-09'},
{'data': {'pname': 'LeBron James', 'fg3': Decimal('1.7'), 'stl': Decimal('1.64'), 'orb': Decimal('0.93'), 'fg3a': Decimal('5.09'), 'fta': Decimal('10.17'), 'drb': Decimal('6.36'), 'blk': Decimal('1.01'), 'pf': Decimal('1.57'), 'tov': Decimal('3.43'), 'ft': Decimal('7.8'), 'pts': Decimal('29.71'), 'pid': 1907, 'fg': Decimal('10.11'), 'trb': Decimal('7.29'), 'ast': Decimal('8.57'), 'fga': Decimal('20.11')}, 'season': '2009-10'},
{'data': {'pname': 'LeBron James', 'fg3': Decimal('1.16'), 'stl': Decimal('1.57'), 'orb': Decimal('1.01'), 'fg3a': Decimal('3.53'), 'fta': Decimal('8.39'), 'drb': Decimal('6.46'), 'blk': Decimal('0.63'), 'pf': Decimal('2.06'), 'tov': Decimal('3.59'), 'ft': Decimal('6.37'), 'pts': Decimal('26.72'), 'pid': 1907, 'fg': Decimal('9.59'), 'trb': Decimal('7.47'), 'ast': Decimal('7.01'), 'fga': Decimal('18.8')}, 'season': '2010-11'},
{'data': {'pname': 'LeBron James', 'fg3': Decimal('0.87'), 'stl': Decimal('1.85'), 'orb': Decimal('1.52'), 'fg3a': Decimal('2.4'), 'fta': Decimal('8.1'), 'drb': Decimal('6.42'), 'blk': Decimal('0.81'), 'pf': Decimal('1.55'), 'tov': Decimal('3.44'), 'ft': Decimal('6.24'), 'pts': Decimal('27.15'), 'pid': 1907, 'fg': Decimal('10.02'), 'trb': Decimal('7.94'), 'ast': Decimal('6.24'), 'fga': Decimal('18.85')}, 'season': '2011-12'},
{'data': {'pname': 'LeBron James', 'fg3': Decimal('1.36'), 'stl': Decimal('1.7'), 'orb': Decimal('1.28'), 'fg3a': Decimal('3.34'), 'fta': Decimal('7.04'), 'drb': Decimal('6.75'), 'blk': Decimal('0.88'), 'pf': Decimal('1.45'), 'tov': Decimal('2.97'), 'ft': Decimal('5.3'), 'pts': Decimal('26.79'), 'pid': 1907, 'fg': Decimal('10.07'), 'trb': Decimal('8.03'), 'ast': Decimal('7.25'), 'fga': Decimal('17.82')}, 'season': '2012-13'}]
'''
#type2:
'''
{'2011-12': {'fg3': Decimal('0.87'), 'pts': Decimal('27.15'), 'tov': Decimal('3.44'), 'fg': Decimal('10.02'), 'blk': Decimal('0.81'), 'drb': Decimal('6.42'), 'pf': Decimal('1.55'), 'stl': Decimal('1.85'), 'pid': 1907, 'fga': Decimal('18.85'), 'fg3a': Decimal('2.4'), 'pname': 'LeBron James', 'fta': Decimal('8.1'), 'ast': Decimal('6.24'), 'orb': Decimal('1.52'), 'ft': Decimal('6.24'), 'trb': Decimal('7.94')},
'2009-10': {'fg3': Decimal('1.7'), 'pts': Decimal('29.71'), 'tov': Decimal('3.43'), 'fg': Decimal('10.11'), 'blk': Decimal('1.01'), 'drb': Decimal('6.36'), 'pf': Decimal('1.57'), 'stl': Decimal('1.64'), 'pid': 1907, 'fga': Decimal('20.11'), 'fg3a': Decimal('5.09'), 'pname': 'LeBron James', 'fta': Decimal('10.17'), 'ast': Decimal('8.57'), 'orb': Decimal('0.93'), 'ft': Decimal('7.8'), 'trb': Decimal('7.29')},
'2008-09': {'fg3': Decimal('1.63'), 'pts': Decimal('28.44'), 'tov': Decimal('2.98'), 'fg': Decimal('9.74'), 'blk': Decimal('1.15'), 'drb': Decimal('6.26'), 'pf': Decimal('1.72'), 'stl': Decimal('1.69'), 'pid': 1907, 'fga': Decimal('19.91'), 'fg3a': Decimal('4.74'), 'pname': 'LeBron James', 'fta': Decimal('9.41'), 'ast': Decimal('7.25'), 'orb': Decimal('1.31'), 'ft': Decimal('7.33'), 'trb': Decimal('7.57')},
'2010-11': {'fg3': Decimal('1.16'), 'pts': Decimal('26.72'), 'tov': Decimal('3.59'), 'fg': Decimal('9.59'), 'blk': Decimal('0.63'), 'drb': Decimal('6.46'), 'pf': Decimal('2.06'), 'stl': Decimal('1.57'), 'pid': 1907, 'fga': Decimal('18.8'), 'fg3a': Decimal('3.53'), 'pname': 'LeBron James', 'fta': Decimal('8.39'), 'ast': Decimal('7.01'), 'orb': Decimal('1.01'), 'ft': Decimal('6.37'), 'trb': Decimal('7.47')},
'2012-13': {'fg3': Decimal('1.36'), 'pts': Decimal('26.79'), 'tov': Decimal('2.97'), 'fg': Decimal('10.07'), 'blk': Decimal('0.88'), 'drb': Decimal('6.75'), 'pf': Decimal('1.45'), 'stl': Decimal('1.7'), 'pid': 1907, 'fga': Decimal('17.82'), 'fg3a': Decimal('3.34'), 'pname': 'LeBron James', 'fta': Decimal('7.04'), 'ast': Decimal('7.25'), 'orb': Decimal('1.28'), 'ft': Decimal('5.3'), 'trb': Decimal('8.03')}}
'''
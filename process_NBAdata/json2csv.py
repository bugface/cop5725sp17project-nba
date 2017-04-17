import json
import csv
from progress.bar import Bar

def getOneRecord(fileName, line_num):
	with open(fileName, "r") as f:
		for index, line in enumerate(f):
			if(index == line_num):
				sample  = f.readline()
	with open("tempData.json","w") as f1:
		f1.writelines(sample)

def load_data(file):
	with open(file, "r") as f:
		data = json.load(f)
	return data

def obtainGameUID(data):
	# #game date
	# d = data["date"]["$date"][:10]
	# #teams' abbreviation
	# ta1 = data["teams"][0]["abbreviation"]
	# ta2 = data["teams"][1]["abbreviation"]
	# return hash(d + ta1 + ta2)
	return data["_id"]["$oid"]

def obtainGameDate(data):
	return data["date"]["$date"][:10]


#this is protocol for process data
# with open("1.csv", "a") as ft:
# 	w = csv.writer(ft)
# 	title_list = ["t_name", "t_abbv", "t_score", "t_home", "t_won", "gameUID"]
# 	w.writerow(title_list)
# 	t = s["teams"]
# 	for each in t:
# 		c = [each["name"],each["abbreviation"],each["score"],each["home"],each["won"], hash(each["name"])]
# 		w.writerow(c)

#not including stats
def process_teams(data, flag, filename):
	gameUID = obtainGameUID(data)
	gameDate = obtainGameDate(data)
	if(flag == 0):
		with open(filename, "a") as ft:
			writer = csv.writer(ft)
			title_list = ["t_name", "t_abbv", "t_score", "t_home", "t_won", "gameUID", "date",
						"t_ast", "t_blk", "t_drb", "t_fg", "t_fg3", "t_fg3a", "t_fga", "t_ft", "t_fta", "t_orb",
						"t_pf", "t_stl", "t_tov", "t_trb"]
			writer.writerow(title_list)

			team_data1 = []
			team_data2 = []
			team1 = data["teams"][0]
			team2 = data["teams"][1]
			ts1 = data["box"][0]["team"]
			ts2 = data["box"][1]["team"]

			team_data1.append(team1["name"])
			team_data1.append(team1["abbreviation"])
			team_data1.append(team1["score"])
			team_data1.append(team1["home"])
			team_data1.append(team1["won"])
			team_data1.append(gameUID)
			team_data1.append(gameDate)
			team_data1.append(ts1["ast"])
			team_data1.append(ts1["blk"])
			team_data1.append(ts1["drb"])
			team_data1.append(ts1["fg"])
			team_data1.append(ts1["fg3"])
			team_data1.append(ts1["fg3a"])
			team_data1.append(ts1["fga"])
			team_data1.append(ts1["ft"])
			team_data1.append(ts1["fta"])
			team_data1.append(ts1["orb"])
			team_data1.append(ts1["pf"])
			team_data1.append(ts1["stl"])
			team_data1.append(ts1["tov"])
			team_data1.append(ts1["trb"])

			writer.writerow(team_data1)

			team_data2.append(team2["name"])
			team_data2.append(team2["abbreviation"])
			team_data2.append(team2["score"])
			team_data2.append(team2["home"])
			team_data2.append(team2["won"])
			team_data2.append(gameUID)
			team_data2.append(gameDate)
			team_data2.append(ts2["ast"])
			team_data2.append(ts2["blk"])
			team_data2.append(ts2["drb"])
			team_data2.append(ts2["fg"])
			team_data2.append(ts2["fg3"])
			team_data2.append(ts2["fg3a"])
			team_data2.append(ts2["fga"])
			team_data2.append(ts2["ft"])
			team_data2.append(ts2["fta"])
			team_data2.append(ts2["orb"])
			team_data2.append(ts2["pf"])
			team_data2.append(ts2["stl"])
			team_data2.append(ts2["tov"])
			team_data2.append(ts2["trb"])

			writer.writerow(team_data2)
	else:
		with open(filename, "a") as ft:
			writer = csv.writer(ft)
			writer = csv.writer(ft)

			team_data1 = []
			team_data2 = []
			team1 = data["teams"][0]
			team2 = data["teams"][1]
			ts1 = data["box"][0]["team"]
			ts2 = data["box"][1]["team"]

			team_data1.append(team1["name"])
			team_data1.append(team1["abbreviation"])
			team_data1.append(team1["score"])
			team_data1.append(team1["home"])
			team_data1.append(team1["won"])
			team_data1.append(gameUID)
			team_data1.append(gameDate)
			team_data1.append(ts1["ast"])
			team_data1.append(ts1["blk"])
			team_data1.append(ts1["drb"])
			team_data1.append(ts1["fg"])
			team_data1.append(ts1["fg3"])
			team_data1.append(ts1["fg3a"])
			team_data1.append(ts1["fga"])
			team_data1.append(ts1["ft"])
			team_data1.append(ts1["fta"])
			team_data1.append(ts1["orb"])
			team_data1.append(ts1["pf"])
			team_data1.append(ts1["stl"])
			team_data1.append(ts1["tov"])
			team_data1.append(ts1["trb"])

			writer.writerow(team_data1)

			team_data2.append(team2["name"])
			team_data2.append(team2["abbreviation"])
			team_data2.append(team2["score"])
			team_data2.append(team2["home"])
			team_data2.append(team2["won"])
			team_data2.append(gameUID)
			team_data2.append(gameDate)
			team_data2.append(ts2["ast"])
			team_data2.append(ts2["blk"])
			team_data2.append(ts2["drb"])
			team_data2.append(ts2["fg"])
			team_data2.append(ts2["fg3"])
			team_data2.append(ts2["fg3a"])
			team_data2.append(ts2["fga"])
			team_data2.append(ts2["ft"])
			team_data2.append(ts2["fta"])
			team_data2.append(ts2["orb"])
			team_data2.append(ts2["pf"])
			team_data2.append(ts2["stl"])
			team_data2.append(ts2["tov"])
			team_data2.append(ts2["trb"])

			writer.writerow(team_data2)

#including stats
def process_players(data, flag, filename):
	gameUID = obtainGameUID(data)
	gameDate = obtainGameDate(data)
	if(flag == 0):
		with open(filename, "a") as ft:
			writer = csv.writer(ft)

			title_list = ["ast", "blk", "drb", "fg", "fg3", "fg3a", "fga", "ft", "fta", "mp",
							"orb", "pf", "player_name", "pts", "stl", "tov", "trb", "gameUID",
							"date", "team"]
			writer.writerow(title_list)

			p1 = data["box"][0]["players"]
			p1_team = data["teams"][0]["name"]
			for p in p1:
				p_data = [p["ast"], p["blk"], p["drb"], p["fg"], p["fg3"],
							p["fg3a"], p["fga"], p["ft"], p["fta"], p["mp"],
							p["orb"], p["pf"], p["player"], p["pts"], p["stl"],
							p["tov"], p["trb"], gameUID, gameDate, p1_team]
				writer.writerow(p_data)

			p2_team = data["teams"][1]["name"]
			p2 = data["box"][1]["players"]
			for p in p2:
				p_data = [p["ast"], p["blk"], p["drb"], p["fg"], p["fg3"],
							p["fg3a"], p["fga"], p["ft"], p["fta"], p["mp"],
							p["orb"], p["pf"], p["player"], p["pts"], p["stl"],
							p["tov"], p["trb"], gameUID, gameDate, p2_team]
				writer.writerow(p_data)
	else:
		with open(filename, "a") as ft:
			writer = csv.writer(ft)

			p1 = data["box"][0]["players"]
			p1_team = data["teams"][0]["name"]
			for p in p1:
				p_data = [p["ast"], p["blk"], p["drb"], p["fg"], p["fg3"],
							p["fg3a"], p["fga"], p["ft"], p["fta"], p["mp"],
							p["orb"], p["pf"], p["player"], p["pts"], p["stl"],
							p["tov"], p["trb"], gameUID, gameDate, p1_team]
				writer.writerow(p_data)

			p2_team = data["teams"][1]["name"]
			p2 = data["box"][1]["players"]
			for p in p2:
				p_data = [p["ast"], p["blk"], p["drb"], p["fg"], p["fg3"],
							p["fg3a"], p["fga"], p["ft"], p["fta"], p["mp"],
							p["orb"], p["pf"], p["player"], p["pts"], p["stl"],
							p["tov"], p["trb"], gameUID, gameDate, p2_team]
				writer.writerow(p_data)

def process_games(data, flag, filename):
	gameUID = obtainGameUID(data)
	gameDate = obtainGameDate(data)
	if(flag == 0):
		with open(filename, "a") as ft:
			writer = csv.writer(ft)
			title_list = ["t_home", "t_away", "t_win", "t_loss", "gameUID", "date"]
			writer.writerow(title_list)
			row = []
			t1 = data["teams"][0]
			t2 = data["teams"][1]
			#home vs away
			if(t1["home"] == True):
				row.append(t1["abbreviation"])
				row.append(t2["abbreviation"])
			else:
				row.append(t2["abbreviation"])
				row.append(t1["abbreviation"])
			#won vs loss
			if(t1["won"] == 1):
				row.append(t1["abbreviation"])
				row.append(t2["abbreviation"])
			else:
				row.append(t2["abbreviation"])
				row.append(t1["abbreviation"])

			row.append(gameUID)
			row.append(gameDate)
			writer.writerow(row)
	else:
		with open(filename, "a") as ft:
			writer = csv.writer(ft)
			row = []
			t1 = data["teams"][0]
			t2 = data["teams"][1]
			#home vs away
			if(t1["home"] == True):
				row.append(t1["abbreviation"])
				row.append(t2["abbreviation"])
			else:
				row.append(t2["abbreviation"])
				row.append(t1["abbreviation"])
			#won vs loss
			if(t1["won"] == 1):
				row.append(t1["abbreviation"])
				row.append(t2["abbreviation"])
			else:
				row.append(t2["abbreviation"])
				row.append(t1["abbreviation"])

			row.append(gameUID)
			row.append(gameDate)
			writer.writerow(row)

def main():
	# the nba file totally has 31686 line of json data
	#dataInput = input("input the file name: ")
	dataInput = "nba.json"
	filename_players = "processed_data/nbadata_players_full.csv"
	filename_teams = "processed_data/nbadata_teams_full.csv"
	filename_games = "processed_data/nbadata_games_full.csv"
	#k=20
	#k =
	k = 31685

	bar = Bar("processing...", max = k)
	i = 0

	while(i < k):
		getOneRecord(dataInput, i)
		jData = load_data("tempData.json")
		process_teams(jData, i, filename_teams)
		process_players(jData, i, filename_players)
		process_games(jData, i, filename_games)
		#print((31684 - i) + " records left to be processed.")
		bar.next()
		i += 1

if __name__ == "__main__":
	main()
	 # data = load_data("sampledata.json")
	 # process_players(data, 0)
	 # process_teams(data, 0)
	 # process_games(data, 0)


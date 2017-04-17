import pandas as pd
from pandas import ExcelWriter
import os

def combine_excel_files():
	i = 97
	sheets = []
	for j in range(26):
		sheets.append(chr(i+j))
	#print(type(sheets[1]))

	#combined_df = pd.DataFrame()
	combined_df = []

	# with open("players.xlsx", "rb") as f:
	# 	for sheet in sheets:
	# 		#print(sheet)
	# 		try:
	# 			df = pd.read_excel(f, sheet)
	# 			print(df)
	# 			if(sheet == "a"):
	# 				combined_df.append(df)
	# 			else:
	# 				combined_df.append(df.iloc[2:])
	# 		except:
	# 			continue
	# print(combined_df)
	for sheet in sheets:
	 	try:
	 		with open("players.xlsx", "rb") as f:
	 			df = pd.read_excel(f, sheet)
	 			#print(df)
	 			# if(sheet == 'a'):
	 			# 	combined_df.append(df)
	 			# else:
	 			# 	combined_df.append(df)
	 			combined_df.append(df)
	 	except:
	 		pass
	#print(combined_df)
	combined_df = pd.concat(combined_df)
	#combined_df.drop(combined_df.columns[[0]], axis = 1, inplace = True)
	combined_df["id"] = [i for i in range(len(combined_df))]
	#with open("combined_players.xlsx", "wb") as f1:
	#print(combined_df)
	writer = ExcelWriter("combined_players.xlsx")
	combined_df.to_excel(writer, "Sheet1")
	writer.save()

def remove_asterisk_from_name():
	df = pd.read_excel("combined_players.xlsx")
	for i, each in enumerate(df["Player"]):
		if(each[-1] == "*"):
			df["Player"][i] = each[:-1]
	writer = ExcelWriter("final_players.xlsx")
	df.to_excel(writer, "Sheet1")
	writer.save()

def add_pic_url_to_player_table():
	url = []
	names = []
	with open("url.txt", "r") as f:
		for each in f:
			url.append(each)
			names.append(each[19:-5])
	dic_name_url = dict(zip(names, url))

	df = pd.read_excel("final_players1.xlsx")
	for i in range(len(df)):
		ident = df["Player"][i]
		if ident in names:
			df["player_headshot"][i] = dic_name_url[ident]

	writer = ExcelWriter("final_players.xlsx")
	df.to_excel(writer, "Sheet2")
	writer.save()

def select_games_after_2009():
	os.chdir(r"D:\pythonproject\cop5725\process_NBAdata\processed_data")
	df = pd.read_csv("nbadata_games_full.csv")
	limit = "2009-10-01"
	index_to_remove = []
	for i in df.index:
		if df["date"][i] < limit:
			index_to_remove.append(i)
	df.drop(df.index[index_to_remove], inplace = True)
	writer = ExcelWriter("nbadata_games_after20091001.xlsx")
	df.to_excel(writer, "Sheet")
	writer.save()

def add_season_to_games():
	os.chdir("D:\\pythonproject\\cop5725\\process_NBAdata\\processed_data")
	df = pd.read_excel("nbadata_games_after20091001.xlsx")
	df["season"] = ""
	for i in range(len(df)):
		date = df["date"][i]
		#print(season)
		if date < "2010-09-30":
			df["season"][i] += "2009-10"
		elif date > "2010-10-01" and date < "2011-09-30":
			df["season"][i] += "2010-11"
		elif date > "2011-10-01" and date < "2012-09-30":
			df["season"][i] += "2011-12"
		elif date > "2012-10-01" and date < "2013-09-30":
			df["season"][i] += "2012-2013"
		#print(season)

	writer = ExcelWriter("nbadata_games_after20091001_withseason.xlsx")
	df.to_excel(writer, "Sheet1")
	writer.save()

def add_abbv_to_team_table():
	dic = create_teamname_teamabbr_dic()
	#print(dic)
	os.chdir("D:\\pythonproject\\cop5725\\process_NBAdata")
	df = pd.read_excel("NBA-Team-pic.xlsx")
	df["teamabbv"] = None
	#print(df)
	for i in range(len(df)):
		#print(df["teamname"][i+1])
		try:
			df["teamabbv"][i+1] = dic[df["teamname"][i+1]]
		except:
			pass

	writer = ExcelWriter("teams.xlsx")
	df.to_excel(writer, "Sheet1")
	writer.save()


def create_teamname_teamabbr_dic():
	os.chdir("D:\\pythonproject\\cop5725\\process_NBAdata\\processed_data")
	df = pd.read_csv("nbadata_teams_full.csv")

	dic_name_abbr = dict()

	for i in range(len(df)):
		if df["t_name"][i] not in dic_name_abbr.keys():
			dic_name_abbr[df["t_name"][i]] = df["t_abbv"][i]

	return dic_name_abbr
	#print(dic_name_abbr.keys())

def add_teamabbv_to_players():
	name_abbv_dic = create_teamname_teamabbr_dic()
	os.chdir("D:\\pythonproject\\cop5725\\process_NBAdata\\processed_data")

	df = pd.read_csv("nbadata_players_full_after_20081001.csv")
	df["h_team"] = None
	for i in range(len(df)):
		df["h_team"][i] = name_abbv_dic[df["team"][i]]
		#print(df["h_team"][i])

	writer = ExcelWriter("nbadata_players_full_after_20081001_addteamabbv.xlsx")
	df.to_excel(writer, "Sheet")
	writer.save()

def insert_player_id():
	dic = create_playername_id_dic()
	miss_list = []
	os.chdir("D:\\pythonproject\\cop5725\\process_NBAdata\\tables_can_insert_to_db")
	df = pd.read_excel("nbadata_stats_full_after_20081001_addteamabbv.xlsx")
	df["player_id"] = None
	for i in range(len(df)):
		try:
			df["player_id"][i] = dic[df["player_name"][i]]
		except:
			miss_list.append(df["player_name"])

	print(miss_list)
	writer = ExcelWriter("nbadata_players_full_after_20081001_addteamabbv1.xlsx")
	df.to_excel(writer, "Sheet")
	writer.save()


def create_playername_id_dic():
	os.chdir("D:\\pythonproject\\cop5725\\process_NBAdata\\tables_can_insert_to_db")
	df = pd.read_excel("players(url added).xlsx")

	dic_name_id = dict()

	for i in range(len(df)):
		if df["Player"][i] not in dic_name_id.keys():
			dic_name_id[df["Player"][i]] = df["player_id"][i]
		else:
			if(df["From"][i] < 2014 and df["To"][i] > 2008):
				dic_name_id[df["Player"][i]] = df["player_id"][i]
			# else:
			# 	print(df["Player"][i])
			#print(df["Player"][i])
	#print(dic_name_id["David Lee"])
	return dic_name_id
	#print(len(dic_name_id))

def add_score_to_gametable():
	os.chdir("D:\\pythonproject\\cop5725\\process_NBAdata\\processed_data")
	df1 = pd.read_excel("nbadata_games_after20091001_withseason.xlsx")
	df = pd.read_csv("nbadata_teams_full.csv")

	dic = dict()
	for i in range(len(df)):
		if df["gameUID"][i] in dic:
			if df["t_home"][i] == True:
				dic[df["gameUID"][i]][0] = df["t_score"][i]
			elif df["t_home"][i] == False:
				dic[df["gameUID"][i]][1] = df["t_score"][i]
		else:
			dic[df["gameUID"][i]] = [None]*2
			if df["t_home"][i] == True:
				dic[df["gameUID"][i]][0] = df["t_score"][i]
			elif df["t_home"][i] == False:
				dic[df["gameUID"][i]][1] = df["t_score"][i]
	#print(dic)
	for i in range(len(df1)):
		df1["home_score"][i] = dic[df1["gameUID"][i]][0]
		df1["away_score"][i] = dic[df1["gameUID"][i]][1]

	writer = ExcelWriter("nbadata_team_after20091001_finished.xlsx")
	df1.to_excel(writer, "Sheet")
	writer.save()



def main():
	print(create_teamname_teamabbr_dic())

if __name__ == '__main__':
	#combined_df()
	#remove_asterisk_from_name()
	#add_pic_url_to_player_table()
	#add_season_to_games()
	#create_teamname_teamabbr_dic()
	#add_teamabbv_to_players()
	#create_playername_id_dic()
	#insert_player_id()
	#add_score_to_gametable()
	#add_abbv_to_team_table()
	main()
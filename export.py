import cx_Oracle


username = 'TESTING'
password = '1111'
databaseName = "localhost/db11g"
 
connection = cx_Oracle.connect (username,password,databaseName)
 
cursor = connection.cursor()

addons_dict = {"Wings of Liberty":"WoL", "Heart of the Swarm":"HotS", "Legacy of the Void":"LotV"}
races_dict = {"Zerg":"Z", "Protoss":"P", "Terran":"T"}



query = '''SELECT match_date, player1_name, victory_status, player2_name, player1_faction, player2_faction, expansion_name
      FROM matches 
      ORDER BY match_id'''


cursor.execute (query)


exported_data = []
data = cursor.fetchone ()
while (data!=None):
  data = list(data)
  data[1] = data[1].replace(' ', '')
  data[3] = data[3].replace(' ', '')
  data[0] = data[0].strftime("%m/%d/%Y")
  for i, j in addons_dict.items():
    data[6] = data[6].replace(i, j)
    data[6] = data[6].replace(' ', '')
  for i, j in races_dict.items():
    data[4] = data[4].replace(i, j)
    data[4] = data[4].replace(' ', '')
    data[5] = data[5].replace(i, j)
    data[5] = data[5].replace(' ', '')
  if data[2] == "1":
  	data[2] = "[winner]"
  	data.append("[loser]")
  else:
  	data[2] = "[loser]"
  	data.append("[winner]")
  exported_data.append(data)
  data = cursor.fetchone ()

with open("sc2-matches-history-exported.csv", "w") as file:
	file.write("match_date,player_1,player_1_match_status,score,player_2,player_2_match_status,player_1_race,player_2_race,addon,tournament_type\n")
	for line in exported_data:
		file_list = [line[0], line[1], line[2], "score placeholder", line[3], line[7], line[4], line[5], line[6], "type placeholder\n"]
		file_line = ",".join(file_list)
		file.write(file_line)

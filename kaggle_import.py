import cx_Oracle
import csv
import codecs

username = 'TESTING'
password = '1111'
databaseName = "localhost/db11g"

connection = cx_Oracle.connect (username,password,databaseName)

cursor = connection.cursor()

tables = ["matches", "faction", "game_expansion", "player"]

for i in tables:
	query = ("DELETE FROM " + i)
	cursor.execute (query)

def transform_csv_data(raw_list):
	addons_dict = {"WoL":"Wings of Liberty", "HotS":"Heart of the Swarm", "LotV":"Legacy of the Void"}
	races_dict = {"Z":"Zerg", "P":"Protoss", "T":"Terran"}
	if (raw_list[2] == "[winner]"):
		raw_list[2] = 1
	else:
		raw_list[2] = 0
	for i, j in addons_dict.items():
		raw_list[3] = raw_list[3].replace(i, j)
	for i, j in races_dict.items():
		raw_list[6] = raw_list[6].replace(i, j)
		raw_list[7] = raw_list[7].replace(i, j)
	try:
		query = '''INSERT INTO matches (match_id, match_date, victory_status, expansion_name, player1_name, player2_name, player1_faction, player2_faction) 
			VALUES (:match_id, TO_DATE(:match_date,'mm-dd-yyyy'), :victory_status, :expansion_name, :player1_name, :player2_name, :player1_faction, :player2_faction)'''
		cursor.execute(query, raw_list)
	except:
		print("err")
	return raw_list 

players = set()
matches_SC = []
factions = ["Zerg", "Protoss", "Terran"]
expansions = ["Wings of Liberty", "Heart of the Swarm", "Legacy of the Void"]


with codecs.open("sc2-matches-history.csv", "r", "utf-8") as file:
    line_count = 0
    converted = csv.reader(file)
    for line in converted:
        try:
            if line_count == 10000:
                break
            if line_count > 0:
            	player1 = line[1]
            	player2 = line[4]
            	single_match = transform_csv_data([line_count, line[0], line[2], line[8], player1, player2, line[6], line[7]])
            	matches_SC.append(single_match)
            	print(single_match)
            	players.add(player1)
            	players.add(player2)
            line_count += 1
        except:
            continue

for i in factions:
	query = ("INSERT INTO faction(faction_name) VALUES (\'" + i + "\')")
	cursor.execute (query)
for i in expansions:
	query = ("INSERT INTO game_expansion(expansion_name) VALUES (\'" + i + "\')")
	cursor.execute (query)
for i in players:
	try:
		query = ("INSERT INTO player(player_name) VALUES (\'" + i + "\')")
		cursor.execute (query)
	except:
		continue



#query = '''INSERT INTO matches (match_id, match_date, victory_status, expansion_name, player1_name, player2_name, player1_faction, player2_faction) 
#        VALUES (:match_id, TO_DATE(:match_date,'mm-dd-yyyy'), :victory_status, :expansion_name, :player1_name, :player2_name, :player1_faction, :player2_faction)'''

#cursor.prepare(query)

#cursor.executemany(query, matches_SC)

#for mtch in matches_SC:
#    try:
#        cursor.execute(query, datum)
#    except:
#     	continue


cursor.close()
connection.commit()
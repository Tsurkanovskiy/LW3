import cx_Oracle
import chart_studio
import plotly.graph_objs as go
import chart_studio.dashboard_objs as dashboard
import chart_studio.plotly as py
 
chart_studio.tools.set_credentials_file(username='Serjo', api_key='k4eWHU3Ubbd13Zr6B8Ad')


username = 'SERGIY'
password = '1111'
databaseName = "localhost/db11g"
 
connection = cx_Oracle.connect (username,password,databaseName)
 
cursor = connection.cursor()
 
query = '''SELECT
    player.player_name, played_matches
FROM
  player LEFT OUTER JOIN     
    (SELECT player_name, count(player_name) AS played_matches
      FROM participant 
     GROUP by player_name) temp
        ON player.player_name = temp.player_name
ORDER BY played_matches'''


cursor.execute (query)

top_players = []
played_games = []

data = cursor.fetchone ()
while (data!=None):
  print (data)
  player = data[0].replace(' ', '')
  top_players.append(player)
  played_games.append(data[1])
  data = cursor.fetchone ()
print("-------------------------------------------------")
 
query = '''SELECT
    faction, faction_victories, ROUND((faction_victories/all_victories * 100),0)
FROM
    (SELECT faction, count(faction) AS faction_victories
      FROM participant 
      WHERE participant.victory_status=\'[winner]\'
     GROUP by faction),
     (SELECT count(participant.victory_status) AS all_victories
      FROM participant
      WHERE participant.victory_status=\'[winner]\') '''
cursor.execute (query)

factions = []
percentage = []
x = 0

data = cursor.fetchone ()
while (data!=None):
  print (data)
  if data[0] == "T ":
    x = "Terran"
  elif data[0] == "Z ":
    x = "Zerg"
  else:
    x = "Protoss"
  factions.append(x)
  percentage.append(data[1])
  data = cursor.fetchone ()


print("-------------------------------------------------")
 
query = 'SELECT match_date, COUNT(match_date) FROM match GROUP BY match_date ORDER BY match_date'
cursor.execute (query)

number_of_games = []
dates = []

data = cursor.fetchone ()
while (data!=None):
  print (data)
  dates.append(data[0])
  number_of_games.append(data[1])
  data = cursor.fetchone ()

print (dates)
print (number_of_games)
 
cursor.close ()
 
connection.close ()

data = [go.Bar(
      x=top_players,
      y=played_games
    )]

layout = go.Layout(
    title='Profesional StarCraft 2 players with most tornament matches participation',
    xaxis=dict(
        title='Profesional player\'s nickname',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
 
customers_orders_sum = py.plot(fig)


pie = go.Pie(labels=factions, values=percentage)
py.plot([pie])


order_date_prices = go.Scatter(
    x=dates,
    y=number_of_games,
    mode='lines+markers'
)
data = [order_date_prices]
py.plot(data)
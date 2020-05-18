import cx_Oracle
import chart_studio
import plotly.graph_objs as go
import chart_studio.dashboard_objs as dashboard
import chart_studio.plotly as py
 
chart_studio.tools.set_credentials_file(username='Serjo', api_key='k4eWHU3Ubbd13Zr6B8Ad')


username = 'TESTING'
password = '1111'
databaseName = "localhost/db11g"
 
connection = cx_Oracle.connect (username,password,databaseName)
 
cursor = connection.cursor()


query = '''SELECT *
    FROM (SELECT player_name, count(player_name) AS played_matches
      FROM work_table 
      GROUP by player_name
      ORDER BY played_matches DESC)
      WHERE rownum <= 20'''


cursor.execute (query)

top_players = []
played_games = []

data = cursor.fetchone ()
while (data!=None):
  player = data[0].replace(' ', '')
  top_players.append(player)
  played_games.append(data[1])
  data = cursor.fetchone ()
#print("-------------------------------------------------")
 
query = '''SELECT
    faction_name, faction_victories
FROM
    (SELECT faction_name, count(faction_name) AS faction_victories
      FROM work_table 
      WHERE (faction_name = player1_faction AND victory_status = 1) OR (faction_name = player2_faction AND victory_status = 0)
     GROUP by faction_name)'''
cursor.execute (query)

factions = []
percentage = []

data = cursor.fetchone ()
while (data!=None):
  factions.append(data[0])
  percentage.append(data[1])
  data = cursor.fetchone ()


#print("-------------------------------------------------")
 
query = 'SELECT match_date, COUNT(match_date) FROM work_table GROUP BY match_date ORDER BY match_date'
cursor.execute (query)

number_of_games = []
dates = []

data = cursor.fetchone ()
while (data!=None):

  dates.append(data[0])
  number_of_games.append(data[1])
  data = cursor.fetchone ()

 
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

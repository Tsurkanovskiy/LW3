CREATE VIEW work_table AS
  SELECT *
  FROM matches 
  JOIN player ON matches.player1_name = player.player_name OR matches.player2_name = player.player_name
  JOIN faction ON faction.faction_name = matches.player1_faction OR faction.faction_name = matches.player2_faction;
-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--To Drop the database if it exists otherwise just skips this command
DROP DATABASE IF EXISTS tournament;

--To Create a new Database named tournament
CREATE DATABASE tournament;

--To connect to the new tournament database
\c tournament;

--To Drop the Tables and View created if it already exists otherwise just skips these commands
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP VIEW IF EXISTS player_rankings;

--To create a new table called players with attributes id and name
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT
);

--To create a new table called matches with attributes match_id, winner and loser
CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	winner INTEGER REFERENCES players(id),
	loser INTEGER REFERENCES players(id)
);

--To create a new view called player_rankings for the current player standings
CREATE VIEW player_rankings AS
	SELECT p.id, p.name,
	(SELECT COUNT(*) FROM matches m WHERE p.id = m.winner) AS won,
	(SELECT COUNT(*) FROM matches m WHERE p.id = m.winner OR p.id = m.loser) AS games
	FROM players p
	GROUP BY p.id
	ORDER BY won DESC;
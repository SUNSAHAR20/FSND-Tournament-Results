#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
import bleach
import psycopg2


def connection():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    swiss = connection()
    cur = swiss.cursor()
    cur.execute("DELETE FROM matches")
    swiss.commit()
    swiss.close()
    return


def deletePlayers():
    """Remove all the player records from the database."""
    swiss = connection()
    cur = swiss.cursor()
    cur.execute("DELETE FROM players")
    swiss.commit()
    swiss.close()
    return


def countPlayers():
    """Returns the number of players currently registered."""
    swiss = connection()
    cur = swiss.cursor()
    cur.execute("SELECT COUNT(*) FROM players")
    no_of_players = cur.fetchone()[0]
    swiss.close()
    return no_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    swiss = connection()
    cur = swiss.cursor()
    contents = bleach.clean(name, tags=['h', 'script', 'br'], strip=True)
    cur.execute("INSERT INTO players (name) VALUES (%s)", (contents,))
    swiss.commit()
    swiss.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    swiss = connection()
    cur = swiss.cursor()
    cur.execute("SELECT * FROM player_rankings")
    array = cur.fetchall()


    if (array[0][2] != 0) and (array[0][2] == array[1][2]):
        cur.execute("SELECT * FROM player_rankings ORDER BY (won/games) DESC")
        array = cur.fetchall()
    swiss.close()

    return array


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    swiss = connection()
    cur = swiss.cursor()
    cur.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser,))
    swiss.commit()
    swiss.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    swiss = connection()
    cur = swiss.cursor()
    cur.execute("SELECT * FROM player_rankings")
    array = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM player_rankings")
    no = cur.fetchone()[0]
    pairs = []

    if(no % 2 == 0):
        for i in range(0, no - 1, 2):
            pairs_value = (array[i][0], array[i][1], array[i+1][0], array[i+1][1])
            pairs.append(pairs_value)

    swiss.close()
    return pairs





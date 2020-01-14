#!/usr/bin/env python3
import datetime
import time
import sys

from sheetwriter import SheetWriter
from dao import GamesDao, PerformancesDao
from dataObjects import Season, Match, CDL

SEASONS = [(1, 10824, "Season1"), (2, 11086, "Season2"),
           (3, 11336, "Season3"), (4, 11560, "Season4")]

# open two cnnection to the Mongo db
gamesColl = GamesDao("games")
performancesColl = PerformancesDao("performances")


def buildDatabaseClean(flag):
    if flag:
        print("clearing data")
        gamesColl.clearData()
        performancesColl.clearData()

    cdl = CDL(SEASONS)
    for season in cdl.seasons:
        gamesColl.writeMany(season.formatMatches())
        performancesColl.writeMany(season.formatPerformances())


buildDatabaseClean("--clean" in sys.argv)

for season in SEASONS:
    writer = SheetWriter(season[2])

    topKills = performancesColl.getData("kills", 10, -1, {"seasonNumber": season[0]})
    writer.writeArray("A2:C11", topKills, "kills", "steamName", "dotabuff")

    topDeaths = performancesColl.getData("deaths", 10, -1, {"seasonNumber": season[0]})
    writer.writeArray("A13:C22", topDeaths, "deaths", "steamName", "dotabuff")

    topAssists = performancesColl.getData("assists", 10, -1, {"seasonNumber": season[0]})
    writer.writeArray("A24:C33", topAssists, "assists", "steamName", "dotabuff")

    topGPM = performancesColl.getData("gold_per_min", 10, -1, {"seasonNumber": season[0]})
    writer.writeArray("A35:C44", topGPM, "gold_per_min", "steamName", "dotabuff")

    longDuration = gamesColl.getData("duration", 10, -1, {"seasonNumber": season[0]})
    writer.writeArray("A46:B55", longDuration, "string_duration", "dotabuff")

    shortDuration = gamesColl.getData("duration", 10, 1, {"seasonNumber": season[0]})
    writer.writeArray("A57:B66", shortDuration, "string_duration", "dotabuff")

    captWins = performancesColl.getWins({"$match": {"captain"+str(season[0]): 1, "seasonNumber": season[0]}})
    writer.writeArray("E2:G11", captWins, "wins", "name", "dotabuff")

writer = SheetWriter("AllTime")

topKills = performancesColl.getData("kills", 10, -1, {})
writer.writeArray("A2:C11", topKills, "kills", "steamName", "dotabuff")

topDeaths = performancesColl.getData("deaths", 10, -1, {})
writer.writeArray("A13:C22", topDeaths, "deaths", "steamName", "dotabuff")

topAssists = performancesColl.getData("assists", 10, -1, {})
writer.writeArray("A24:C33", topAssists, "assists", "steamName", "dotabuff")

topGPM = performancesColl.getData("gold_per_min", 10, -1, {})
writer.writeArray("A35:C44", topGPM, "gold_per_min", "steamName", "dotabuff")

longDuration = gamesColl.getData("duration", 10, -1, {})
writer.writeArray("A46:B55", longDuration, "string_duration", "dotabuff")

shortDuration = gamesColl.getData("duration", 10, 1, {})
writer.writeArray("A57:B66", shortDuration, "string_duration", "dotabuff")

captWins = performancesColl.getWins({"$match": {"seasonCaptain": 1}})
writer.writeArray("E2:G11", captWins, "wins", "name", "dotabuff")

playerWins = performancesColl.getWins({"$match": {}})
writer.writeArray("E13:G22", playerWins, "wins", "name", "dotabuff")
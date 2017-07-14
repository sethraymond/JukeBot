#!/usr/bin/python3
import json
import asyncio
from libs.DiscordController import *
import libs.GooglePlayMusicController as GPMController

with open("../secrets/JukeBot.secret.json", "r") as secretsFile:
    secrets = json.load(secretsFile)

discord_init(secrets)

gpm = GPMController.GpmSession(secrets["gPlayAppUser"], secrets["gPlayAppPass"])
while not gpm.logged_in:
    gpm = GPMController.GpmSession()

run_discord(secrets["botToken"])
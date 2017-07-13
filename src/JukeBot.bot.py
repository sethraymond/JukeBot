#!/usr/bin/python3

import json
import asyncio
import libs.GooglePlayMusicController as GPMController
from libs.DiscordController import DiscordController

with open("../secrets/JukeBot.secret.json", "r") as secretsFile:
    secrets = json.load(secretsFile)

#discord_controller = DiscordController(secrets["botToken"], None)

#discord_controller.run()

gpm = GPMController.GpmSession(secrets["gPlayAppUser"], secrets["gPlayAppPass"])
while not gpm.logged_in:
	gpm = GPMController.GpmSession()


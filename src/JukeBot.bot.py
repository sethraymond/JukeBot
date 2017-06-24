#!/usr/bin/python3

import json
import asyncio
from libs.DiscordController import DiscordController

with open("../secrets/JukeBot.secret.json", "r") as secretsFile:
    secrets = json.load(secretsFile)

discord_controller = DiscordController(secrets["botToken"], None)

discord_controller.run()
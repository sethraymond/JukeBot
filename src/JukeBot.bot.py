#!/usr/bin/python3
import json
import asyncio
from libs.DiscordController import *

with open("../secrets/JukeBot.secret.json", "r") as secretsFile:
    secrets = json.load(secretsFile)

run_discord(secrets["botToken"])
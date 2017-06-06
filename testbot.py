from disco.bot import Bot, Plugin

class SimplePlugin(Plugin):
	@Plugin.command('ping')
	def on_ping_command(self, event):
		event.msg.reply('Pong!')

	@Plugin.command('echo', '<content:str...>')
	def on_echo_command(self, event, content):
		event.msg.reply(content)

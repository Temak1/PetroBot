import discord
import asyncio
import json
import os

client = discord.Client()
BOT_HELP = '''Доступные команды:
**!@help** - выводит это сообщение
**!@add** - добавляет видео в список данного канала
**!@poll** - запускает голосование за видео (пока только среди двух пользователей)
**!@show** - показывает пригодный для копирования список видео данного канала
**!@clear** - очищает список данного канала
'''

def WhichChannel(channel):
	if channel == 'general':
		return 'list_file.txt'
	else:
		return 'test_file.txt'

def EditFile(file, message, flag):
	if not os.path.isfile(file):
		list_file_names = []
	else:
		with open(file, 'r') as list_file:
			list_file_names = json.load(list_file)

	if flag == True:
		list_file_names.append(message) #.split('\n')
	else:
		list_file_names[0] = message

	with open(file, 'w') as list_file:
		json.dump(list_file_names, list_file)

async def CheckPreviousMessages():
	if not os.path.isfile(str('Settings.txt')):
		print('Ошибка! Файл Settings.txt не существует.')
		return
	with open('Settings.txt', 'r') as File:
		LastMessageId = json.load(File)
	counter = 0
	Messages = []
	async for msg in client.logs_from(Server.channel.name('general'), limit=2): #get_channel(358956907517575170)
		#if msg.id < LastMessageId:
		#	break
		if msg.content.startswith('!@add'):
			Messages.append(msg.content[5:].strip())
	EditFile(file_name, msg.reverse(), True)

@client.event
async def on_ready():
	print('Logged in as ' + client.user.name + ' with id ' + client.user.id)
	print('-----')
	#for i in client.get_all_channels():
	#	print(i.id)
	CheckPreviousMessages()

@client.event
async def on_resumed():
	print('Resumed in as ' + client.user.name + ' with id ' + client.user.id)
	print('-----')
	CheckPreviousMessages()

"""@client.event
async def on_message(message):
	print("check 1")
	if message.content.startswith('!@check'):
		print("check 2")
		channel = message.channel
		await channel.send('Send me that reaction, mate')
		def check(reaction, user):
			return user == message.author and str(reaction.emoji) == ''
		try:
			reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await channel.send('')
		else:
			await channel.send('')"""

@client.event
async def on_message(message):
	file_name = WhichChannel(message.channel.name)

	if message.author != client.user:
		EditFile('Settings.txt', message.id, False)

	if message.content.startswith('!@help'):
		await client.send_message(message.channel, BOT_HELP)
		print('Выведена помощь')

	elif message.content.startswith('!@add'):
		EditFile(file_name, message.content[5:].strip(), True)
		await client.add_reaction(message, '✅') #White check mark
		print('В файл ' + file_name + ' добавлено видео ' + message.content[5:].strip())

	elif message.content.startswith('!@show'):
		if not os.path.isfile(str(file_name)):
			await client.send_message(message.channel, 'список ' + file_name + ' пуст')
			return
		with open (str(file_name), 'r') as list_file:
			list_file_names = json.load(list_file)
		i = 0
		string = 'Список видео:\n```\n'
		while i < len(list_file_names):
			#string = string + str(i+1) + '. ' + list_file_names[i]
			string = string  + list_file_names[i]
			i = i + 1
			string = string + '\n'
		string = string + '```'
		await client.send_message(message.channel, string)
		print('Показано содержимое файла ' + file_name)

	elif message.content.startswith('!@poll'):
		await client.add_reaction(message, '✅') #White check mark
		await client.add_reaction(message, '❌') #Cross Mark
		print('Устроено голосование за видео' + message.content[6:].strip())

	elif message.content.startswith('!@clear'):
		os.remove(file_name)
		await client.add_reaction(message, '✅')
		print('Список ' + file_name + ' удалён')
	# elif message.content.startswith('!@clrchannel'):
	# 	counter = 0
	# 	async for msg in client.logs_from(message.channel, limit=1000):
	# 		if msg.author == client.user:
	# 			await client.delete_message(msg)
	# 			counter += 1
	# 	print('You have {} messages.'.format(counter))

@client.event
async def on_reaction_add(reaction, user):
	#print('1')
	if (not reaction.me and reaction.message.author != user):
		if reaction.emoji == '✅': #White check mark
			with open ('list_file.txt', 'r') as list_file:
				list_file_names = json.load(list_file)
			list_file_names.append(message.content[5:].strip())
			with open('list_file.txt', 'w') as list_file:
				json.dump(list_file_names, list_file)
			await client.remove_reaction(reaction.message, '❌', me) #removing Cross Mark
			print('Видео прошло голосование')

		elif reaction.emoji == '❌': #Cross Mark
			await client.remove_reaction(reaction.message, '✅', me) #removing White check mark
			print('Видео не прошло голосование')
'''
pid = os.getpid()
def check_pid(pid):
	print('check_pid')
	""" Check for the existence of a pid. """
	try:
		os.kill(pid, 0)
	except OSError:
		return False
	else:
		return True
check_pid(pid)
'''

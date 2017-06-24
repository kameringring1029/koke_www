#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import timedelta

import os, sys
import MySQLdb
import time
import datetime
import random
import re
import commands

time_format="%Y-%m-%d %H:%M:%S"


import usecv
import usesql


def get_rare(pattern):
	rand = random.randint(0,99)

	if pattern == "alpaca":
		if rand > 90:
			rarity = 2
		else :
			rarity = 1
	else:
		if rand > 95:
			rarity = 4
		elif rand > 93:
			rarity = 3
		elif rand > 84:
			rarity = 2
		else :
			rarity = 1

	return rarity


def get_names(request):

#	unit = str(request.encode('utf-8'))
	unit = str(request)

	if (unit.find('μ') > -1) or (unit.find('muse') > -1) or (unit.find('みゅーず') > -1) or (unit.find('ミューズ') > -1):
		if (unit.find('1年') > -1) or (unit.find('一年') > -1):
			return ('星空凛','西木野真姫','小泉花陽')
		if (unit.find('2年') > -1) or (unit.find('二年') > -1):
			return ('高坂穂乃果','南ことり','園田海未')
		if (unit.find('3年') > -1) or (unit.find('三年') > -1):
			return ('絢瀬絵里','東條希','矢澤にこ')
		return ('高坂穂乃果','絢瀬絵里','南ことり','園田海未','星空凛','西木野真姫','東條希','小泉花陽','矢澤にこ')
	if (unit.find('Printemps') > -1)or(unit.find('printemps') > -1)or(unit.find('プランタン') > -1)or(unit.find('ぷらんたん') > -1):
		return ('高坂穂乃果','南ことり','小泉花陽')
	if (unit.find('lily') > -1)or(unit.find('リリホワ') > -1):
		return ('園田海未','星空凛','東條希')
	if (unit.find('BiBi') > -1)or(unit.find('bibi') > -1)or(unit.find('Bibi') > -1)or(unit.find('ビビ') > -1):
		return ('絢瀬絵里','西木野真姫','矢澤にこ')
	if (unit.find('にこりんぱな') > -1):
		return ('星空凛','小泉花陽','矢澤にこ')

	if (unit.find('Aqours') > -1) or (unit.find('aqours') > -1)or (unit.find('アクア') > -1)or (unit.find('あくあ') > -1):
		if (unit.find('1年') > -1) or (unit.find('一年') > -1):
			return ('津島善子','国木田花丸','黒澤ルビィ')
		if (unit.find('2年') > -1) or (unit.find('二年') > -1):
			return ('高海千歌','桜内梨子','渡辺曜')
		if (unit.find('3年') > -1) or (unit.find('三年') > -1):
			return ('松浦果南','黒澤ダイヤ','小原鞠莉')
		return ('高海千歌','桜内梨子','松浦果南','黒澤ダイヤ','渡辺曜','津島善子','国木田花丸','小原鞠莉','黒澤ルビィ')
	if (unit.find('cyaron') > -1)or(unit.find('CYaRon') > -1)or(unit.find('シャロン') > -1)or(unit.find('しゃろん') > -1):
		return ('高海千歌','渡辺曜','黒澤ルビィ')
	if (unit.find('AZALEA') > -1)or(unit.find('azalea') > -1)or(unit.find('アゼリア') > -1)or(unit.find('あぜりあ') > -1):
		return ('松浦果南','黒澤ダイヤ','国木田花丸')
	if (unit.find('Kiss') > -1)or(unit.find('kiss') > -1)or(unit.find('キス') > -1)or(unit.find('きす') > -1):
		return ('桜内梨子','津島善子','小原鞠莉')

	if (unit.find('穂乃果') > -1)or(unit.find('ほのか') > -1):
		return ('高坂穂乃果')
	if (unit.find('絵里') > -1)or(unit.find('えり') > -1)or(unit.find('エリーチカ') > -1)or(unit.find('エリチカ') > -1):
		return ('絢瀬絵里')
	if (unit.find('ことり') > -1)or(unit.find('(・8・)') > -1)or(unit.find('（・8・）') > -1)or(unit.find('(・８・)') > -1)or(unit.find('（・８・）') > -1):
		return ('南ことり')
	if (unit.find('海未') > -1)or(unit.find('うみ') > -1):
		return ('園田海未')
	if (unit.find('凛') > -1)or(unit.find('りん') > -1):
		return ('星空凛')
	if (unit.find('真姫') > -1)or(unit.find('まき') > -1)or(unit.find('マッキー') > -1):
		return ('西木野真姫')
	if (unit.find('希') > -1)or(unit.find('のぞみ') > -1)or(unit.find('ノゾー') > -1)or(unit.find('のんたん') > -1):
		return ('東條希')
	if (unit.find('花陽') > -1)or(unit.find('はなよ') > -1)or(unit.find('ぱな') > -1):
		return ('小泉花陽')
	if (unit.find('にこ') > -1):
		return ('矢澤にこ')

	if (unit.find('千歌') > -1)or(unit.find('ちか') > -1)or(unit.find('チカ') > -1):
		return ('高海千歌')
	if (unit.find('梨子') > -1)or(unit.find('りこ') > -1):
		return ('桜内梨子')
	if (unit.find('果南') > -1)or(unit.find('かなん') > -1):
		return ('松浦果南')
	if (unit.find('ダイヤ') > -1)or(unit.find('だいや') > -1):
		return ('黒澤ダイヤ')
	if (unit.find('曜') > -1)or(unit.find('よう') > -1):
		return ('渡辺曜')
	if (unit.find('善子') > -1)or(unit.find('よしこ') > -1)or(unit.find('ヨハネ') > -1):
		return ('津島善子')
	if (unit.find('花丸') > -1)or(unit.find('まる') > -1)or(unit.find('マル') > -1):
		return ('国木田花丸')
	if (unit.find('鞠莉') > -1)or(unit.find('まり') > -1)or(unit.find('マリー') > -1):
		return ('小原鞠莉')
	if (unit.find('ルビィ') > -1)or(unit.find('るびぃ') > -1):
		return ('黒澤ルビィ')

	if (unit.find('アルパカ') > -1):
		return ('アルパカ')

	if (unit.find('all') > -1)or(unit.find('All') > -1)or(unit.find('みんな') > -1)or(unit.find('全') > -1):
		return ('高坂穂乃果','絢瀬絵里','南ことり','園田海未','星空凛','西木野真姫','東條希','小泉花陽','矢澤にこ','高海千歌','桜内梨子','松浦果南','黒澤ダイヤ','渡辺曜','津島善子','国木田花丸','小原鞠莉','黒澤ルビィ')

	return ('高坂穂乃果','絢瀬絵里','南ことり','園田海未','星空凛','西木野真姫','東條希','小泉花陽','矢澤にこ','高海千歌','桜内梨子','松浦果南','黒澤ダイヤ','渡辺曜','津島善子','国木田花丸','小原鞠莉','黒澤ルビィ')
	#return ('高坂穂乃果','絢瀬絵里','南ことり','園田海未','星空凛','西木野真姫','東條希','小泉花陽','矢澤にこ')
	#return ('高海千歌','桜内梨子','松浦果南','黒澤ダイヤ','渡辺曜','津島善子','国木田花丸','小原鞠莉','黒澤ルビィ')




def gatcha(text):
	""" Let's stare abstractedly at the User Streams ! """
	# インスタンス生成
	useCV = usecv.UseCV()
	useSQL = usesql.UseSQL()

	dobu = 1
	UR_flug = 1
	SR_flug = 1


	icons = []
	tweet = ""


	print text


	for num in range(0,11):

		text = text.replace("'","")

		names = get_names(text)
		if isinstance(names, str):
			if names.find("アルパカ"):
				rarity = get_rare("alpaca")
		else:
			rarity = get_rare("normal")

		if (text.find('UR') > -1)and(rarity==1)and(random.randint(0,1)):
			rarity = 4
		if (text.find('SR') > -1)and(rarity==1)and(random.randint(0,1)):
			rarity = 3

		if rarity > 1:
			dobu = 0
		elif (dobu == 1) and (num == 10):
		## SR確定
			rarity = 2
			dobu = 0


		member_id = 30
		while member_id > 27 and member_id < 52:

			series = 0
			if rarity > 1 and len(text.rsplit(' ',1)) > 1:
			#	print str(text.rsplit(' ',1)[1].encode('utf-8'))
				series = str(text.rsplit(' ',1)[1])
				if not('編' in series):
					series = 0

			member_id = useSQL.rand_member(rarity,names,series)
		(member_info, member_url) = useSQL.get_member(member_id)

		tweet = tweet + str(member_info)
		if rarity > 1:
			tweet = tweet + '*'
		tweet = tweet + '\r'

		filename = '/var/www/callback/img/icon'+str(num)+'.png'
		command = "wget '"+str(member_url)+"' -O "+filename
		check = commands.getoutput(command)
		print check

#			print check
		icons.insert(num,filename+" "+str(rarity))


#	if dobu == 1:
#		tweet = tweet + 'ﾄﾞ(・8・)ﾌﾞ'
#	tweet = tweet + "#スクフェス"
	print tweet
	
	base_dir = '../img/'
	icons.insert(11, base_dir)
	useCV.create_gacha_image(icons)




if __name__ == '__main__':

	gatcha(sys.argv[1])


#	print "gatcha.py end\n"





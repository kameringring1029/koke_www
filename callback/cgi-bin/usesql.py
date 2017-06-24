#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, sys
import MySQLdb
import time
import random
import datetime


time_format="%Y-%m-%d %H:%M:%S"


class UseSQL:


	def openDB(self):
		#print "openDB."
		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		return cursor



	########################
	## ユーザ情報更新関数 ##
	########################
	def old_update_statusTable(self, time_status, username):
		#print "update_statusTable"

		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		try:
	
			## point情報読み込みとDB更新
			f = open('/var/www/up/rank.txt')
			rank = f.readline().strip() # 1行を読み込む
			rank = rank.replace(" ","")
			f.close	
			f = open('/var/www/up/lp.txt')
			lp = f.readline().strip() # 1行を読み込む
			lpnow,lpmax = lp.split(" ")
			f.close	
			notice_flag = "FALSE"
			f = open('/var/www/up/exp.txt')
			exp = f.readline().strip() # 1行を読み込む
			expnow,expmax = exp.split(" ")
			f.close	

			sql = "insert into status_multiuser values('"+time_status+"',"+rank+","+lpnow+","+lpmax+","+expnow+","+expmax+","+notice_flag+",'"+username+"')"
			#print "[SQL]"+ sql 
			
			cursor.execute(sql)

			## DB commit 
			connector.commit()
			#print " DB updated." 


		except MySQLdb.Error, e:
			test = 0
#			try:
				#print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
#			except IndexError:
				#print "MySQL Error: %s" % str(e)



	##############################
	## イベントポイント更新関数 ##
	##############################
	def update_eventTable(self, points ,event):
		print "update_eventTable"
		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()
	
		try:

			event_name = event

			#現在時刻の取得と整形
			localtime = time.strftime(time_format)
			localtime = time.strftime(time_format, time.localtime())

			mine = points.getEventpoint()

#			sql = "insert into "+event_name+" values('"+useTwitter.time_tweet+"',"+str(nowpoint)+","+str(nowitem)+","+str(double)+","+str(single)+")"
			sql = "insert into "+event_name+" values('"+localtime+"',"+str(mine)+")"
			#print "[SQL]"+ sql 
			
			cursor.execute(sql)


			## DB commit and close
			connector.commit()
			#print " DB updated." 


		except MySQLdb.Error, e:
			test = 0
#			try:
				#print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
#			except IndexError:
				#print "MySQL Error: %s" % str(e)





	##############################
	## ユーザ情報更新関数 ##
	##############################
	def update_statusTable(self, points):
		#print "update_statusTable"
		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()
	
		try:

			#現在時刻の取得と整形
			localtime = time.strftime(time_format)
			localtime = time.strftime(time_format, time.localtime())

			rank = points.getRank()
			lp_now = points.getLpnow()
			lp_max = points.getLpmax()
			exp_now = points.getExpnow()
			exp_max = points.getExpmax()

#			sql = "insert into "+event_name+" values('"+useTwitter.time_tweet+"',"+str(nowpoint)+","+str(nowitem)+","+str(double)+","+str(single)+")"
			sql = "insert into status values('"+localtime+"',"+str(rank)\
					+","+str(lp_now)+","+str(lp_max)+","+str(exp_now)\
					+","+str(exp_max)+","+str(0)+")"
			#print "[SQL]"+ sql 
			
			cursor.execute(sql)


			## DB commit and close
			connector.commit()
			#print " DB updated." 


		except MySQLdb.Error, e:
			test = 0
			#try:
				#print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			#except IndexError:
				#print "MySQL Error: %s" % str(e)




	##############################
	## イベントポイント更新関数 ##
	##############################
	def update_borderTable(self, useTwitter,event):
		#print "update_eventTable"
		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()
	
		try:

			event_name = event

			#現在時刻の取得と整形
			localtime = time.strftime(time_format)
			localtime = time.strftime(time_format, time.localtime())
		
			## point情報読み込みとDB更新
			f = open('/var/www/up/now.txt')
			nowpoint = f.readline().strip() # 1行を読み込む
			f.close	
			f = open('/var/www/up/item.txt')
			nowitem = f.readline().strip() # 1行を読み込む
			f.close	

			border_time, T1, T2, T3 = useTwitter.get_border()
			#print border_time+" "+T1+" "+T2+" "+T3
	
			if useTwitter.time_tweet=='':
				useTwitter.time_tweet = "2016/"+border_time+":00"

			if nowitem=='':
				nowitem = 0

#			sql = "insert into "+event_name+" values('"+useTwitter.time_tweet+"',"+str(nowpoint)+","+str(nowitem)+","+str(double)+","+str(single)+")"
			sql = "insert into "+event_name+"_border values('"+useTwitter.time_tweet+"',"+str(T1)+","+str(T2)+","+str(T3)+")"
			#print "[SQL]"+ sql 
			
			cursor.execute(sql)


			## DB commit and close
			connector.commit()
			#print " DB updated." 


		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)



	##############################
	## イベントボーダー ##
	##############################
	def get_points(self, event):
		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		points_list = []

		try:
	
			event_name = event
	
 			##select
			sql = "select * from " + event_name
			#print "[SQL]"+sql
			cursor.execute(sql)
			result = cursor.fetchall()
			for row in result:
				item_list = []
				col = 0
				for item in row:
					if col == 0:
						item = item.strftime("%Y/%m/%d %H:%M:%S")
						col = 1
					item_list.append(item)
				points_list.append(item_list)
	
			## DB commit and close
			connector.commit()
	

		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)


		#print "+-----------------------+"
		#print points_list
		#print "+-----------------------+"

		return points_list


	##############################
	## 最新Status取得 ##
	##############################
	def get_latest_status(self):
		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		status_list = []

		try:
	
 			##select
			sql = "select * from status" 
			#print "[SQL]"+sql
			cursor.execute(sql)
			result = cursor.fetchall()
			for row in result:
				item_list = []
				col = 0
				for item in row:
					if col == 0:
						#item = item.strftime("%Y/%m/%d %H:%M:%S")
						col = 1
					item_list.append(item)
				status_list=item_list
	
			## DB commit and close
			connector.commit()
	

			## 現在LPの更新 ##
			time = datetime.datetime.now()
			delta = time - status_list[0]
			lpnow = status_list[2] + (delta.seconds / 60 / 6)
			if(lpnow > status_list[3]):
				status_list[2] = status_list[3]
			else:
				status_list[2] = lpnow



		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)


		#print "+-----------------------+"
		#print status_list
		#print "+-----------------------+"

		return status_list



	##############################
	## イベントポイント参照関数 ##
	##############################
	def show_Table(self, event):

		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		try:
	
			event_name = event
	
	
 			##select
			sql = "select * from " + event_name
			#print "[SQL]"+sql
			cursor.execute(sql)
			result = cursor.fetchall()
			#print "+-----------------------+"
			for row in result:
				if event == "status":
					print "| "+str(row[0])+", RANK:"+str(row[1])+", LP:"+str(row[2])+"/"+str(row[3])+", EXP:"+str(row[4])+"/"+str(row[5])+", POP:"+str(row[6])+" |"
				else:
					print "| "+str(row[0])+", "+str(row[1])+", "+str(row[2])+", "+str(row[3])+", "+str(row[4])+" |"
			#print "+-----------------------+"
	
			## DB commit and close
			connector.commit()
	

		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)





	################
	## DB終了関数 ##
	################
	def closeDB(self,cursor,connector):
		cursor.close()
		connector.close()



	##################
	## 部員参照関数 ##
	##################
	def get_member(self, member_id):

		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		try:
 			##select
			sql = "select name, series, rarity, S_0, P_0, C_0, type, image_url, fullimg_0, newicon from carddata where id="+str(member_id) 
	#		#print "[SQL]"+sql
			cursor.execute(sql)
			result = cursor.fetchall()[0]
			name = result[0].encode('utf-8')

			if name == '高坂穂乃果':
				name = '穂乃果'
			if name == '絢瀬絵里':
				name = '絵里'
			if name == '南ことり':
				name = 'ことり'
			if name == '園田海未':
				name = '海未'
			if name == '星空凛':
				name = '凛'
			if name == '西木野真姫':
				name = '真姫'
			if name == '東條希':
				name = '希'
			if name == '小泉花陽':
				name = '花陽'
			if name == '矢澤にこ':
				name = 'にこ'

			if name == '高海千歌':
				name = '千歌'
			if name == '桜内梨子':
				name = '梨子'
			if name == '松浦果南':
				name = '果南'
			if name == '黒澤ダイヤ':
				name = 'ダイヤ'
			if name == '渡辺曜':
				name = '曜'
			if name == '津島善子':
				name = '善子'
			if name == '国木田花丸':
				name = '花丸'
			if name == '小原鞠莉':
				name = '鞠莉'
			if name == '黒澤ルビィ':
				name = 'ルビィ'


#			if max(result[3], result[4], result[5]) == result[3]:
#				spc = "スマイル"
#			if max(result[3], result[4], result[5]) == result[4]:
#				spc = "ピュア"
#			if max(result[3], result[4], result[5]) == result[5]:
#				spc = "クール"
			spc = result[6].encode('utf-8')


			series = result[1].encode('utf-8')
			if series=='':
				series = '初期'
			if result[2] == 1:
				series = spc

			if name == 'アルパカ':
				if result[2] > 2:
					result[2] = 1
				if result[2] == 1:
					series = result[1].encode('utf-8')

			if result[2] == 0:
				rare = 'N'
			if result[2] == 1:
				rare = 'R'
			if result[2] == 2:
				rare = 'SR'
			if result[2] == 3:
				rare = 'SSR'
			if result[2] == 4:
				rare = 'UR'

		#	member_url = result[7].encode('utf-8')
			member_fullimgurl = result[8].encode('utf-8')
			member_url = result[9].encode('utf-8')
	
			## DB commit and close
			connector.commit()
			cursor.close()
			connector.close()
	
		#	return (rare + name + "(" + series + ")", member_url)

			if (name != 'アルパカ' and rare == 'R') or (name == 'アルパカ' and rare == 'SR'):
				return (rare + name, member_url)
			else:
				return (rare + name + "(" + series + ")", member_url)
				
		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)



	##################
	## 任意のレアリティ部員からランダムで一つのIDを返す ##
	##################
	def rand_member(self, rarity, names, series):
		#print "rand_member"
		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		try:
			now_pool_id = 794

 			##select
			sql = "select id, name, series from carddata where rarity="+str(rarity)
			sql = sql + " AND ("


			if isinstance(names, str):
				sql = sql + "name='" + names + "')"
			else:
				cnt = 0
				for name in names:
					cnt = cnt + 1
					sql = sql + "name='" + name + "'"
					if cnt != len(names):
						sql = sql + " OR "
				sql = sql + ")"

			if series != 0:
				sql = sql + " AND series='" + series + "' "
				now_pool_id = 0


			## μ's勧誘 排出メンバ限定
			if names == ('高坂穂乃果','絢瀬絵里','南ことり','園田海未','星空凛','西木野真姫','東條希','小泉花陽','矢澤にこ') and rarity > 1:
				sql = sql + "AND id>" + str(now_pool_id)


			#print "[SQL]"+sql
			cursor.execute(sql)
			result = cursor.fetchall()
	
			## DB commit and close
			connector.commit()
			cursor.close()
			connector.close()

			member_id = result[random.randint(0,len(result)-1)][0]

			## 確率UP
			if names == ('高坂穂乃果','絢瀬絵里','南ことり','園田海未','星空凛','西木野真姫','東條希','小泉花陽','矢澤にこ'):
				add_UR_member_num = 1
				add_SSR_member_num = 0
				add_SR_member_num = 2
				rand = random.randint(0,100)

				if rarity == 4:
					if rand>50:
						member_id = result[random.randint(len(result)-add_UR_member_num,len(result)-1)][0]
				if rarity == 3:
					if rand>100:
						member_id = result[random.randint(len(result)-add_SSR_member_num,len(result)-1)][0]
				if rarity == 2:
					if rand>85:
						member_id = result[random.randint(len(result)-add_SR_member_num,len(result)-1)][0]




			if names == ('高海千歌','桜内梨子','松浦果南','黒澤ダイヤ','渡辺曜','津島善子','国木田花丸','小原鞠莉','黒澤ルビィ'):
				add_UR_member_num = 1
				add_SSR_member_num = 1
				add_SR_member_num = 3

				if rarity == 4:
					if random.randint(0,1):
						member_id = result[random.randint(len(result)-add_UR_member_num,len(result)-1)][0]
				if rarity == 3:
					if random.randint(0,1):
						member_id = result[random.randint(len(result)-add_SSR_member_num,len(result)-1)][0]
				if rarity == 2:
					if random.randint(0,1):
						member_id = result[random.randint(len(result)-add_SR_member_num,len(result)-1)][0]




			return member_id


	
		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)



	##################
	## 部員参照関数 today_card##
	##################
	def get_member_info(self, member_id):

		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		try:
 			##select
			sql = "select name, series, rarity, S_1, P_1, C_1, type, unit_skill, imple_info, fullimg_0, fullimg_1 from carddata where id="+str(member_id) 
	#		#print "[SQL]"+sql
			cursor.execute(sql)
			result = cursor.fetchall()[0]
			name = result[0].encode('utf-8')

			spc = result[6].encode('utf-8')
			unit_skill = result[7].encode('utf-8')
			imple_info = result[8].encode('utf-8')


			series = result[1].encode('utf-8')
			if series=='':
				series = '初期'
			if result[2] == 1:
				series = spc

			if result[2] == 0:
				rare = 'N'
			if result[2] == 1:
				rare = 'R'
			if result[2] == 2:
				rare = 'SR'
			if result[2] == 3:
				rare = 'SSR'
			if result[2] == 4:
				rare = 'UR'

			S_0 = str(result[3])
			P_0 = str(result[4])
			C_0 = str(result[5])

			fullimg_0 = result[9].encode('utf-8')
			fullimg_1 = result[10].encode('utf-8')
	
			## DB commit and close
			connector.commit()
			cursor.close()
			connector.close()

			member_info = rare + name + "(" + series + ")\n" + imple_info + "\n" \
							+ "[LV MAX]" + S_0 + "/" + P_0 + "/" + C_0 + "\n[特技]" + unit_skill

			return (member_info, fullimg_0, fullimg_1)
				
		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)



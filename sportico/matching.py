import psycopg2
from datetime import datetime ,timedelta
from collections import defaultdict

alpha_friend=200
alpha_level=50
alpha_time=20
alpha_time_start=100




conn = psycopg2.connect(dbname="postgres", user="manas", password="",host="127.0.0.1",port="5057")
cur = conn.cursor()
time=datetime.now() + timedelta(hours=200)
time=time.timetuple()
startTime=str(time[3])+":"+str(time[4])
print(startTime)
startDate=str(time[0])+"-"+str(time[1])+"-"+str(time[2])
print(startDate)

cur.execute("select * from \"singlesRequest\"  natural join \"userSport\" where status =\'Waiting\' and ((\"startDate\"<\'"+startDate+"\') or (\"startTime\"<\'"+startTime+"\' and \"startDate\"=\'"+startDate+"\')) order by \"startDate\",\"startTime\"")
p=cur.fetchall()

groups = defaultdict(list)

for obj in p:
    groups[obj[8]].append(obj)

a=groups.items()
a=list(a)

req=[]
for i in a:
	groups = defaultdict(list)

	for obj in i[1]:
	    groups[obj[1]].append(obj)
	new_list = groups.values()
	b=list(groups.items())
	ith=[]
	for j in b:
		ith.append(j[1])
	req.append(ith)



for i in req:
	for j in i:

		mm=[]
		l=[]
		startEnd=datetime.combine(j[0][6],j[0][4])
		print(startEnd)
		l.append(j[0])
		for k in range(1,len(j)):
			if datetime.combine(j[k][5],j[k][3])+timedelta(hours=1)<startEnd:
				l.append(j[k])
				if startEnd<datetime.combine(j[k][6],j[k][4]):
					startEnd=datetime.combine(j[k][6],j[k][4])
			else:
				mm.append(l)
				l=[]
				l.append(j[k])
				startEnd=datetime.combine(j[k][6],j[k][4])
		mm.append(l)
		print(mm)
		print("\n")


		for timeslots in mm:
			mat = [[-1 for i in range(len(timeslots))] for j in range(len(timeslots))]
			# print(mat)
			for t in range(len(timeslots)):
				cur.execute("select * from \"userBlacklist\" where uid1_id="+str(timeslots[t][0]))
				p=cur.fetchall()
				blacklist=[]
				for b in p:
					blacklist.append(b[2])
				cur.execute("select * from \"userBlacklist\" where uid2_id="+str(timeslots[t][0]))
				p=cur.fetchall()
				for b in p:
					blacklist.append(b[1])

				levelTop_t=timeslots[t][10]
				levelBottom_t=timeslots[t][9]
				level_t=timeslots[t][12]/300
				timeStart_t=datetime.combine(timeslots[t][5],timeslots[t][3])
				timeEnd_t=datetime.combine(timeslots[t][6],timeslots[t][4])

				for q in range(t+1,len(timeslots)):
					timeStart_q=datetime.combine(timeslots[q][5],timeslots[q][3])
					timeEnd_q=datetime.combine(timeslots[q][6],timeslots[q][4])
					if timeslots[q][0] in blacklist or timeslots[q][0]==timeslots[t][0]:
						mat[t][q]=-1
					else:
						levelTop_q=timeslots[q][10]
						levelBottom_q=timeslots[q][9]
						level_q=timeslots[q][12]/300
						if level_q>levelTop_t or level_q<levelBottom_t or level_t>levelTop_q or level_t<levelBottom_q:
							mat[t][q]=-1
						else:
							if timeStart_q+timedelta(hours=1)>timeEnd_t or timeStart_t + timedelta(hours=1) >timeEnd_q:
								mat[t][q]=-1
							else:
								cur.execute("select * from \"userFriend\" where (uid1_id="+str(timeslots[t][0])+" and uid2_id="+str(timeslots[q][0])+") or (uid2_id="+str(timeslots[t][0])+" and uid1_id="+str(timeslots[q][0])+")")
								p=cur.fetchall()
								isFriend=0
								if len(p)!=0:
									isFriend=1
								
								timeoverlap=min(timeEnd_q,timeEnd_t)-max(timeStart_t,timeStart_q)
								timestart=min(timeStart_t,timeStart_q)-datetime.now()
								mat[t][q]=alpha_friend*isFriend + alpha_level*(1/(1+abs(level_t-level_q))) + alpha_time*(timeoverlap.seconds/3600) + alpha_time_start*(3600/timestart.seconds)


			print(mat)
			matching=[]
			for x in range(0,len(mat[0])):
				maxValue=-1
				maxIndex=x
				for y in range(x+1,len(mat[0])):
					if mat[x][y]>maxValue:
						maxIndex=y
						maxValue=mat[x][y]

				if maxValue>0:
					matching.append((x,maxIndex))
					mat[x]=[-1 for i in range(len(mat[0]))]
					mat[maxIndex]=[-1 for i in range(len(mat[0]))]
					for i in range(0,len(mat[0])):
						mat[i][maxIndex]=-1
					#match x and maxIndex
					timeStart_x=datetime.combine(timeslots[x][5],timeslots[x][3])
					timeEnd_x=datetime.combine(timeslots[x][6],timeslots[x][4])
					timeStart_max=datetime.combine(timeslots[maxIndex][5],timeslots[maxIndex][3])
					timeEnd_max=datetime.combine(timeslots[maxIndex][6],timeslots[maxIndex][4])

					time_start=max(timeStart_x,timeStart_max)
					time_end=min(timeEnd_x,timeEnd_max)

					cur.execute("insert into \"singlesMatching\" values(DEFAULT,\'"+time_start.strftime('%H:%M:%S')+"\',\'"+time_end.strftime('%H:%M:%S')+"\',\'"+time_start.strftime('%Y-%m-%d')+"\',\'"+time_end.strftime('%Y-%m-%d')+"\',"+str(timeslots[x][8])+","+str(timeslots[x][2])+","+str(timeslots[maxIndex][2])+",'Accepted');")
					cur.execute("update \"singlesRequest\" set status=\'Accepted\' where \"singlesRequestId\"="+str(timeslots[x][2]))
					cur.execute("update \"singlesRequest\" set status=\'Accepted\' where \"singlesRequestId\"="+str(timeslots[maxIndex][2]))
					conn.commit()

			print("\n")
			print(matching)














time=datetime.now() + timedelta(hours=200)
time=time.timetuple()
startTime=str(time[3])+":"+str(time[4])
print(startTime)
startDate=str(time[0])+"-"+str(time[1])+"-"+str(time[2])
print(startDate)

cur.execute("select * from \"doublesRequest\", \"doubles\" where \"doublesId\"=\"doublesId_id\" and status =\'Waiting\'and ((\"startDate\"<\'"+startDate+"\') or (\"startTime\"<\'"+startTime+"\' and \"startDate\"=\'"+startDate+"\')) order by \"startDate\",\"startTime\"")
p=cur.fetchall()

groups = defaultdict(list)

for obj in p:
    groups[obj[7]].append(obj)

a=groups.items()
a=list(a)

req=[]
for i in a:
	groups = defaultdict(list)

	for obj in i[1]:
	    groups[obj[8]].append(obj)
	new_list = groups.values()
	b=list(groups.items())
	ith=[]
	for j in b:
		ith.append(j[1])
	req.append(ith)



for i in req:
	for j in i:

		mm=[]
		l=[]
		startEnd=datetime.combine(j[0][4],j[0][2])
		print(startEnd)
		l.append(j[0])
		for k in range(1,len(j)):
			if datetime.combine(j[k][3],j[k][1])+timedelta(hours=1)<startEnd:
				l.append(j[k])
				if startEnd<datetime.combine(j[k][4],j[k][2]):
					startEnd=datetime.combine(j[k][4],j[k][2])
			else:
				mm.append(l)
				l=[]
				l.append(j[k])
				startEnd=datetime.combine(j[k][4],j[k][2])
		mm.append(l)
		print(mm)
		print("\n")


		for timeslots in mm:
			mat = [[-1 for i in range(len(timeslots))] for j in range(len(timeslots))]
			# print(mat)
			for t in range(len(timeslots)):
				cur.execute("select * from \"doublesBlacklist\" where \"doublesId1_id\"="+str(timeslots[t][6]))
				p=cur.fetchall()
				blacklist=[]
				for b in p:
					blacklist.append(b[2])
				cur.execute("select * from \"doublesBlacklist\" where \"doublesId2_id\"="+str(timeslots[t][6]))
				p=cur.fetchall()
				for b in p:
					blacklist.append(b[1])

				levelTop_t=timeslots[t][10]
				levelBottom_t=timeslots[t][9]
				level_t=timeslots[t][17]/300
				timeStart_t=datetime.combine(timeslots[t][3],timeslots[t][1])
				timeEnd_t=datetime.combine(timeslots[t][4],timeslots[t][2])

				for q in range(t+1,len(timeslots)):
					timeStart_q=datetime.combine(timeslots[q][3],timeslots[q][1])
					timeEnd_q=datetime.combine(timeslots[q][4],timeslots[q][2])
					if timeslots[q][6] in blacklist or timeslots[q][6]==timeslots[t][6]:
						mat[t][q]=-1
					else:
						levelTop_q=timeslots[q][10]
						levelBottom_q=timeslots[q][9]
						level_q=timeslots[q][17]/300
						if level_q>levelTop_t or level_q<levelBottom_t or level_t>levelTop_q or level_t<levelBottom_q:
							mat[t][q]=-1
						else:
							if timeStart_q+timedelta(hours=1)>timeEnd_t or timeStart_t + timedelta(hours=1) >timeEnd_q:
								mat[t][q]=-1
							else:
								
								timeoverlap=min(timeEnd_q,timeEnd_t)-max(timeStart_t,timeStart_q)
								timestart=min(timeStart_t,timeStart_q)-datetime.now()
								mat[t][q]=alpha_level*(1/(1+abs(level_t-level_q))) + alpha_time*(timeoverlap.seconds/3600) + alpha_time_start*(3600/timestart.seconds)


			print(mat)
			matching=[]
			for x in range(0,len(mat[0])):
				maxValue=-1
				maxIndex=x
				for y in range(x+1,len(mat[0])):
					if mat[x][y]>maxValue:
						maxIndex=y
						maxValue=mat[x][y]

				if maxValue>0:
					matching.append((x,maxIndex))
					mat[x]=[-1 for i in range(len(mat[0]))]
					mat[maxIndex]=[-1 for i in range(len(mat[0]))]
					for i in range(0,len(mat[0])):
						mat[i][maxIndex]=-1
					#match x and maxIndex
					timeStart_x=datetime.combine(timeslots[x][3],timeslots[x][1])
					timeEnd_x=datetime.combine(timeslots[x][4],timeslots[x][2])
					timeStart_max=datetime.combine(timeslots[maxIndex][3],timeslots[maxIndex][1])
					timeEnd_max=datetime.combine(timeslots[maxIndex][4],timeslots[maxIndex][2])

					time_start=max(timeStart_x,timeStart_max)
					time_end=min(timeEnd_x,timeEnd_max)

					cur.execute("insert into \"doublesMatching\" values(DEFAULT,\'"+time_start.strftime('%H:%M:%S')+"\',\'"+time_end.strftime('%H:%M:%S')+"\',\'"+time_start.strftime('%Y-%m-%d')+"\',\'"+time_end.strftime('%Y-%m-%d')+"\',"+str(timeslots[x][0])+","+str(timeslots[maxIndex][0])+","+str(timeslots[x][7])+");")
					cur.execute("update \"doublesRequest\" set status=\'Accepted\' where \"doublesRequestId\"="+str(timeslots[x][0]))
					cur.execute("update \"doublesRequest\" set status=\'Accepted\' where \"doublesRequestId\"="+str(timeslots[maxIndex][0]))
					conn.commit()

			print("\n")
			print(matching)





time=datetime.now() + timedelta(hours=203)
time=time.timetuple()
startTime=str(time[3])+":"+str(time[4])
print(startTime)
startDate=str(time[0])+"-"+str(time[1])+"-"+str(time[2])
print(startDate)

cur.execute("select * from \"teamRequest\" , team where \"teamId_id\" = \"teamId\" and status =\'Waiting\' and ((\"startDate\"<\'"+startDate+"\') or (\"startTime\"<\'"+startTime+"\' and \"startDate\"=\'"+startDate+"\')) order by \"startDate\",\"startTime\"")
p=cur.fetchall()

groups = defaultdict(list)

for obj in p:
    groups[obj[6]].append(obj)

a=groups.items()
a=list(a)

req=[]
for i in a:
	groups = defaultdict(list)

	for obj in i[1]:
	    groups[obj[24]].append(obj)
	new_list = groups.values()
	b=list(groups.items())
	ith=[]
	for j in b:
		ith.append(j[1])
	req.append(ith)

print(req)

for i in req:
	for j in i:

		mm=[]
		l=[]
		startEnd=datetime.combine(j[0][4],j[0][2])
		print(startEnd)
		l.append(j[0])
		for k in range(1,len(j)):
			if datetime.combine(j[k][3],j[k][1])+timedelta(hours=1)<startEnd:
				l.append(j[k])
				if startEnd<datetime.combine(j[k][4],j[k][2]):
					startEnd=datetime.combine(j[k][4],j[k][2])
			else:
				mm.append(l)
				l=[]
				l.append(j[k])
				startEnd=datetime.combine(j[k][4],j[k][2])
		mm.append(l)
		print(mm)
		print("\n")


		for timeslots in mm:
			mat = [[-1 for i in range(len(timeslots))] for j in range(len(timeslots))]
			# print(mat)
			for t in range(len(timeslots)):
				cur.execute("select * from \"teamBlacklist\" where \"teamId1_id\"="+str(timeslots[t][7]))
				p=cur.fetchall()
				blacklist=[]
				for b in p:
					blacklist.append(b[2])
				cur.execute("select * from \"teamBlacklist\" where \"teamId2_id\"="+str(timeslots[t][7]))
				p=cur.fetchall()
				for b in p:
					blacklist.append(b[1])

				levelTop_t=timeslots[t][9]
				levelBottom_t=timeslots[t][8]
				level_t=timeslots[t][17]/300
				timeStart_t=datetime.combine(timeslots[t][3],timeslots[t][1])
				timeEnd_t=datetime.combine(timeslots[t][4],timeslots[t][2])

				for q in range(t+1,len(timeslots)):
					timeStart_q=datetime.combine(timeslots[q][3],timeslots[q][1])
					timeEnd_q=datetime.combine(timeslots[q][4],timeslots[q][2])
					if timeslots[q][7] in blacklist or timeslots[q][7]==timeslots[t][7]:
						mat[t][q]=-1
					else:
						levelTop_q=timeslots[q][9]
						levelBottom_q=timeslots[q][8]
						level_q=timeslots[q][17]/300
						if level_q>levelTop_t or level_q<levelBottom_t or level_t>levelTop_q or level_t<levelBottom_q:
							mat[t][q]=-1
						else:
							if timeStart_q+timedelta(hours=1)>timeEnd_t or timeStart_t + timedelta(hours=1) >timeEnd_q:
								mat[t][q]=-1
							else:
								
								timeoverlap=min(timeEnd_q,timeEnd_t)-max(timeStart_t,timeStart_q)
								timestart=min(timeStart_t,timeStart_q)-datetime.now()
								mat[t][q]=alpha_level*(1/(1+abs(level_t-level_q))) + alpha_time*(timeoverlap.seconds/3600) + alpha_time_start*(3600/timestart.seconds)


			print(mat)
			matching=[]
			for x in range(0,len(mat[0])):
				maxValue=-1
				maxIndex=x
				for y in range(x+1,len(mat[0])):
					if mat[x][y]>maxValue:
						maxIndex=y
						maxValue=mat[x][y]

				if maxValue>0:
					matching.append((x,maxIndex))
					mat[x]=[-1 for i in range(len(mat[0]))]
					mat[maxIndex]=[-1 for i in range(len(mat[0]))]
					for i in range(0,len(mat[0])):
						mat[i][maxIndex]=-1
					#match x and maxIndex
					timeStart_x=datetime.combine(timeslots[x][3],timeslots[x][1])
					timeEnd_x=datetime.combine(timeslots[x][4],timeslots[x][2])
					timeStart_max=datetime.combine(timeslots[maxIndex][3],timeslots[maxIndex][1])
					timeEnd_max=datetime.combine(timeslots[maxIndex][4],timeslots[maxIndex][2])

					time_start=max(timeStart_x,timeStart_max)
					time_end=min(timeEnd_x,timeEnd_max)

					cur.execute("insert into \"teamMatching\" values(DEFAULT,\'"+time_start.strftime('%H:%M:%S')+"\',\'"+time_end.strftime('%H:%M:%S')+"\',\'"+time_start.strftime('%Y-%m-%d')+"\',\'"+time_end.strftime('%Y-%m-%d')+"\',"+str(timeslots[x][6])+","+str(timeslots[x][0])+","+str(timeslots[maxIndex][0])+",'Accepted');")
					cur.execute("update \"teamRequest\" set status=\'Accepted\' where \"teamRequestId\"="+str(timeslots[x][0]))
					cur.execute("update \"teamRequest\" set status=\'Accepted\' where \"teamRequestId\"="+str(timeslots[maxIndex][0]))
					conn.commit()

			print("\n")
			print(matching)







cur.close()
conn.close()	
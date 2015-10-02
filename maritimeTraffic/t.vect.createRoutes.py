#!/usr/bin/env python
#
############################################################################
#
# MODULE:	v.createRoutes.py
# AUTHOR(S):	Annalisa Minelli
# PURPOSE:	Creates synthetic routes starting from semaphorists recordings
# COPYRIGHT:	(C) 2014 by the GRASS Development Team
#
#		This program is free software under the GNU General Public
#		License (>=v2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################
#%Module
#%  description: Creates synthetic routes starting from semaphorists recordings
#%  keywords: net
#%  keywords: routes
#%  keywords: semaphores
#%End
#%option
#% key: abbreviation
#% type: string
#% description: Semaphore's abbreviated name
#% required: yes
#%end
#%option G_OPT_F_INPUT
#% key: data
#% description: Input .csv file of the semaphorist's recording
#% required: yes
#%end
#%option G_OPT_F_INPUT
#% key: dict
#% description: Input file, dictionary of gates coordinates
#% required: yes
#%end
#%option G_OPT_V_INPUT
#% key: land
#% description: Input vector map of the land zones
#% required: yes
#%end
#%option
#% key: moment
#% description: Date to perform the analysis
#% required: no
#%end
#%option
#% key: period
#% description: Period to perform the analysis
#% required: no
#%end
#%option
#% key: grain
#% description: Granularity at which to perform the period analysis
#% required: no
#%end
#%option G_OPT_V_OUTPUT
#% key: gates
#% description: Output point vector map (or map prefix) recording gates frequentation
#% required: yes
#%end
#%option G_OPT_V_OUTPUT
#% key: grid
#% description: Output line vector map (or map prefix) recording routes
#% required: yes
#%end
#%flag
#% key: a
#% description: Flag if you want to perform an animation (using period mode maps)
#% required: no
#%end

import sys
import os
import re
import math
from collections import OrderedDict
import datetime
import grass.script as grass

def calculateMaps(nomi,abbreviation,coordDict,land,start,end):
	all=[]
	for i in nomi:
		all.append(i.split(' > '))
	for i in all:
		for g in i:
			if g=='':
				all[all.index(i)][i.index(g)]='EXIT'
			elif g=='VIEUX MOINES':
				all[all.index(i)][i.index(g)]='LES_VIEUX_MOINES'
			elif g=='CONQUET':
				all[all.index(i)][i.index(g)]='LE_CONQUET'
			elif g=='FOUR':
				all[all.index(i)][i.index(g)]='LE_FOUR'
			elif g=='SUD':
				all[all.index(i)][i.index(g)]='SUD_'+abbreviation
			elif g=='OUEST':
				all[all.index(i)][i.index(g)]='OUEST_'+abbreviation
			elif g=='NORD':
				all[all.index(i)][i.index(g)]='NORD_'+abbreviation
			elif g=='NORD_OUEST':
				all[all.index(i)][i.index(g)]='NORD_OUEST_'+abbreviation
			elif g==' CAMARET':
				all[all.index(i)][i.index(g)]=g.split(' ')[1]
	all2=[]
	for i in all:
		tmp=[]
		for g in i:
			tmp.append(g.replace(' ','_'))
		all2.append(tmp)
	for i in all2:
		for g in i:
			if g=='NORD_OUEST':
				all2[all2.index(i)][i.index(g)]='NORD_OUEST_'+abbreviation
			elif g=='TOULINGUET_':
				all2[all2.index(i)][i.index(g)]='TOULINGUET'
	fAll=[]
	for i in all2:
		for g in i:
			fAll.append(g)
	postiOc=list(OrderedDict.fromkeys(fAll))
	for i in postiOc:
		if i=='':
			postiOc.pop(postiOc.index(i))
		elif i=='VIEUX MOINES':
			postiOc[postiOc.index(i)]='LES_VIEUX_MOINES'
		elif i=='CONQUET':
			postiOc[postiOc.index(i)]='LE_CONQUET'
		elif i=='FOUR':
			postiOc[postiOc.index(i)]='LE_FOUR'
		elif i=='SUD':
			postiOc[postiOc.index(i)]='SUD_'+abbreviation
		elif i=='OUEST':
			postiOc[postiOc.index(i)]='OUEST_'+abbreviation
		elif i=='NORD':
			postiOc[postiOc.index(i)]='NORD_'+abbreviation
		elif i=='NORD_OUEST':
			postiOc[postiOc.index(i)]='NORD_OUEST_'+abbreviation
	for i in postiOc:
		if i==' CAMARET':
			postiOc[postiOc.index(i)]=i.split(' ')[1]
	postiOk=list(OrderedDict.fromkeys(postiOc))
	ab=[]
	for i in postiOk:
		ab.append(i.replace(' ','_'))
	for i in ab:
		if i=='TOULINGUET_':
			ab[ab.index(i)]='TOULINGUET'
	postiOk=list(OrderedDict.fromkeys(ab))
	s=open(coordDict,'r')
	c=s.readlines()
	coordD=[]
	tc=open('tmpCoord.csv','w')
	for i in postiOk:
		for g in c:
			if re.search(i,g):
				tc.writelines(g)
				coordD.append(g)
	tc.close()
	grass.run_command('g.gisenv',set='OVERWRITE=1')
	grass.run_command('v.in.ascii',input='tmpCoord.csv',x=2,y=3,flags='n',separator='|',output='gates')
	grass.run_command('g.region',vect='gates',n='n+10000',s='s-10000',e='e+10000',w='w-10000')
	grass.run_command('g.region',save='gates')
	lin1=grass.read_command('g.region',flags='pgc')
	north=float((lin1.split('\n')[0]).split('=')[1])
	south=float((lin1.split('\n')[1]).split('=')[1])
	west=float((lin1.split('\n')[2]).split('=')[1])
	east=float((lin1.split('\n')[3]).split('=')[1])
	eastc=float((lin1.split('\n')[-3]).split('=')[1])
	northc=float((lin1.split('\n')[-2]).split('=')[1])
	res=1500
	he=round((north-south)/res)+1
	wi=round((east-west)/res)+1
	ncells=str(he)+','+str(wi)
	posit=str(west)+','+str(south)
	box1=str(res)+','+str(res)
	grass.run_command('v.mkgrid',map='grid1',grid=ncells,position='coor',coor=posit,box=box1)
	l=math.sqrt(2*res**2)
	#commented as posit2 calculation has been simplified
	#px=round(((wi-1)/2),0)
	#py=round(((he+1)/2))
	#if px % 2 == 0:
		#addx=px
	#else:
		#addx=px+1
	#if py % 2 == 0:
		#addy=py
	#else:
		#addy=py+1	
	#simplification of posit2 calculation
	posit2=str(west)+','+str(south)
	#posit2=str(west-(addx*res)+res*(wi))+','+str(south+(addy*res)-res*(he))
	box2=str(l)+","+str(l)
	ncells2=str(he+1)+','+str(wi-1)
	grass.run_command('v.mkgrid',map='grid2',grid=ncells2,position='coor',coor=posit2,box=box2,angle=45)
	grass.run_command('v.type',input='grid1',output='grid1l',from_type='boundary',to_type='line')
	grass.run_command('v.type',input='grid2',output='grid2l',from_type='boundary',to_type='line')
	grass.run_command('v.patch',input='grid1l,grid2l',output='gridl')
	#snapping the vertex of the grid since they superpose exactly
	grass.run_command('v.edit',map='gridl',tool='snap',threshold='-1,'+str((res/2)+(res/4))+',0',ids='1-9999999999',snap='node')
	#grass.run_command('v.clean',input='gridl',type='line',output='gridl2',tool='snap',thresh=res/2)
	grass.run_command('v.overlay',ainput='gridl',binput=land,atype='line',btype='area',operator='not',output='gridOk')
	grass.write_command('r.mapcalc', stdin = "%s = 1" % ('region1'))
	grass.run_command('r.to.vect',input='region1',output='region1',type='area')
	grass.run_command('v.overlay',ainput='gridOk',binput='region1',atype='line',btype='area',operator='and',output='gridRegion')
	grass.run_command('v.clean',input='gridRegion',type='line',output='gridPruned',tool='rmdangle',thresh='400')
	mdist=(l/2)/(math.cos(math.radians(22.5)))
	grass.run_command('v.net',input='gridPruned',points='gates',output='gridPoints',operation='connect',thresh=mdist+1)
	grass.run_command('v.clean',input='gridPoints',type='line',output='gridSegments',tool='break')
	grass.run_command('v.db.droptable',map='gridSegments',flags='f')
	grass.run_command('v.category',input='gridSegments',output='gridNocat',option='del',cat='-1')
	grass.run_command('v.category',input='gridNocat',output='gridCat',option='add')
	grass.run_command('v.db.addtable',map='gridCat',columns='cat integer,npass integer,nameboat varchar(30)')
	grass.run_command('v.db.addcolumn',map='gates',columns='npass integer,nameboat varchar(30)')
	grass.run_command('v.db.update',map='gates',column='npass',value='0')
	grass.run_command('v.db.update',map='gridCat',column='npass',value='0')
	#create or connect to the temporal databse - vedi un try/except
	#grass.run_command('t.create',output='traffic',type='stvds',title='request',description='request')
	grass.run_command('t.connect',database='traffic')
	ind=0
	for i in all2:
		if len(i) == 1:
			ind += 1
			gate=i[0]
			ngates=int((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate))).split('|')[-2])
			ngates=ngates+1
			grass.run_command('v.db.update',map='gates',column='npass',value=ngates,where='str_1="%s"' % (gate))
		elif len(i) == 2:
			ind += 1
			gate1=i[0]
			gate2=i[1]
			g1E=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate1))).split('|')[2])
			g1N=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate1))).split('|')[3])
			g2E=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate2))).split('|')[2])
			g2N=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate2))).split('|')[3])
			p=open('tmpCoord2','w')
			p.writelines("1 "+str(g1E)+" "+str(g1N)+" "+str(g2E)+" "+str(g2N))
			p.close()
			#l'informazione temporale va messa su path2 e path3
			#che vanno in qualche modo salvate TUTTE (inventarsi qualcosa per i nomi) per poter visualizzare tutto insieme
			#e quando esistono sia un path2 che un path3 va fatto un vettoriale unico che abbia la durata dell'evento in questione
			grass.run_command('v.net.path',input='gridCat',output='path_'+str(ind),file='tmpCoord2',flags='s')
			grass.run_command('v.db.droptable',map='path_'+str(ind),flags='f')
			grass.run_command('v.category',input='path_'+str(ind),output='tmpPath4a',option='del')
			grass.run_command('v.category',input='tmpPath4a',output='path_'+str(ind),option='add')
			grass.run_command('v.db.addtable',map='path_'+str(ind))
			alls,alle,partcoor,listcoor,listcat=[],[],[],[],[]
			alls=(grass.read_command('v.to.db',map='path_'+str(ind),type='line',option='start',flags='p')).split('\n')[1:-1]
			alle=(grass.read_command('v.to.db',map='path_'+str(ind),type='line',option='end',flags='p')).split('\n')[1:-1]
			#register the map in the stvds trafic
			startP=start[ind-1]
			endP=end[ind-1]
			#grass.run_command('t.register',input='traffic',maps='path_'+str(ind),type='vect',start=startP,end=endP)
			allse=[]
			e=0
			for i in alls:
				allse.append(i)
				allse.append(alle[e])
				e=e+1
			s=0
			for i in range(0,len(allse)):
				try:
					if s==0:
						sx1=round(float(allse[s].split('|')[1]),0)
						sy1=round(float(allse[s].split('|')[2]),0)
						s=s+1
					else:
						sx2=round(float(allse[s].split('|')[1]),0)
						sy2=round(float(allse[s].split('|')[2]),0)
						if sx1==sx2 and sy1==sy2:
							allse.pop(s)
						else:
							sx1,sy1=sx2,sy2
							s=s+1
				except IndexError:
					break
			s=0
			for i in allse:
				if s==0:
					sx1=round(float(allse[s].split('|')[1]),4)
					sy1=round(float(allse[s].split('|')[2]),4)
					s=s+1
				else:
					sx2=round(float(allse[s].split('|')[1]),4)
					sy2=round(float(allse[s].split('|')[2]),4)
					if sx1==sx2 and sy1==sy2:
						allse.pop(s)
						s=s+1
					else:
						sx1,sy1=sx2,sy2
						s=s+1
			for i in range(0,len(allse)-1):
				listcoor.append(str((float(allse[i].split('|')[1])+float(allse[i+1].split('|')[1]))/2)+","+str((float(allse[i].split('|')[2])+float(allse[i+1].split('|')[2]))/2))
			for i in listcoor:
				cat=int((grass.read_command('v.what',map='gridCat',type='line',coordinates=i,distance='2',flags='g').split('\n')[-2]).split('=')[1])
				nlines=int((grass.read_command('db.select',flags='c',sql='select * from gridCat where cat="%s"' % (cat))).split('|')[-2])
				nlines=nlines+1
				grass.run_command('v.db.update',map='gridCat',column='npass',value=nlines,where='cat="%s"' % (cat))
		elif len(i) == 3:
			ind += 1
			gate1=i[0]
			gate2=i[1]
			gate3=i[2]
			g1E=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate1))).split('|')[2])
			g1N=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate1))).split('|')[3])
			g2E=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate2))).split('|')[2])
			g2N=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate2))).split('|')[3])
			p=open('tmpCoord2','w')
			p.writelines("1 "+str(g1E)+" "+str(g1N)+" "+str(g2E)+" "+str(g2N))
			p.close()
			#l'informazione temporale va messa su path2 e path3
			#che vanno in qualche modo salvate TUTTE (inventarsi qualcosa per i nomi) per poter visualizzare tutto insieme
			#e quando esistono sia un path2 che un path3 va fatto un vettoriale unico che abbia la durata dell'evento in questione
			grass.run_command('v.net.path',input='gridCat',output='path_'+str(ind),file='tmpCoord2',flags='s')
			grass.run_command('v.db.droptable',map='path_'+str(ind),flags='f')
			grass.run_command('v.category',input='path_'+str(ind),output='tmpPath4a',option='del')
			grass.run_command('v.category',input='tmpPath4a',output='path_'+str(ind),option='add')
			grass.run_command('v.db.addtable',map='path_'+str(ind))
			alls,alle,partcoor,listcoor,listcat=[],[],[],[],[]
			alls=(grass.read_command('v.to.db',map='path_'+str(ind),type='line',option='start',flags='p')).split('\n')[1:-1]
			alle=(grass.read_command('v.to.db',map='path_'+str(ind),type='line',option='end',flags='p')).split('\n')[1:-1]
			allse=[]
			e=0
			for i in alls:
				allse.append(i)
				allse.append(alle[e])
				e=e+1
			s=0
			for i in range(0,len(allse)):
				try:
					if s==0:
						sx1=round(float(allse[s].split('|')[1]),0)
						sy1=round(float(allse[s].split('|')[2]),0)
						s=s+1
					else:
						sx2=round(float(allse[s].split('|')[1]),0)
						sy2=round(float(allse[s].split('|')[2]),0)
						if sx1==sx2 and sy1==sy2:
							allse.pop(s)
						else:
							sx1,sy1=sx2,sy2
							s=s+1
				except IndexError:
					break
			s=0
			for i in allse:
				if s==0:
					sx1=round(float(allse[s].split('|')[1]),4)
					sy1=round(float(allse[s].split('|')[2]),4)
					s=s+1
				else:
					sx2=round(float(allse[s].split('|')[1]),4)
					sy2=round(float(allse[s].split('|')[2]),4)
					if sx1==sx2 and sy1==sy2:
						allse.pop(s)
						s=s+1
					else:
						sx1,sy1=sx2,sy2
						s=s+1
			for i in range(0,len(allse)-1):
				listcoor.append(str((float(allse[i].split('|')[1])+float(allse[i+1].split('|')[1]))/2)+","+str((float(allse[i].split('|')[2])+float(allse[i+1].split('|')[2]))/2))
			for i in listcoor:
				cat=int((grass.read_command('v.what',map='gridCat',type='line',coordinates=i,distance='2',flags='g').split('\n')[-2]).split('=')[1])
				nlines=int((grass.read_command('db.select',flags='c',sql='select * from gridCat where cat="%s"' % (cat))).split('|')[-2])
				nlines=nlines+1
				grass.run_command('v.db.update',map='gridCat',column='npass',value=nlines,where='cat="%s"' % (cat))
	
			g3E=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate3))).split('|')[2])
			g3N=float((grass.read_command('db.select',flags='c',sql='select * from gates where str_1="%s"' % (gate3))).split('|')[3])
			p=open('tmpCoord3','w')
			p.writelines("1 "+str(g2E)+" "+str(g2N)+" "+str(g3E)+" "+str(g3N))
			p.close()
			grass.run_command('v.net.path',input='gridCat',output='path2_'+str(ind),file='tmpCoord3',flags='s')
			grass.run_command('v.db.droptable',map='path2_'+str(ind),flags='f')
			grass.run_command('v.category',input='path2_'+str(ind),output='tmpPath6a',option='del')
			grass.run_command('v.category',input='tmpPath6a',output='path2_'+str(ind),option='add')
			grass.run_command('v.db.addtable',map='path2_'+str(ind))
			alls,alle,partcoor,listcoor,listcat=[],[],[],[],[]
			alls=(grass.read_command('v.to.db',map='path2_'+str(ind),type='line',option='start',flags='p')).split('\n')[1:-1]
			alle=(grass.read_command('v.to.db',map='path2_'+str(ind),type='line',option='end',flags='p')).split('\n')[1:-1]
			allse=[]
			e=0
			for i in alls:
				allse.append(i)
				allse.append(alle[e])
				e=e+1
			s=0
			for i in range(0,len(allse)):
				try:
					if s==0:
						sx1=round(float(allse[s].split('|')[1]),0)
						sy1=round(float(allse[s].split('|')[2]),0)
						s=s+1
					else:
						sx2=round(float(allse[s].split('|')[1]),0)
						sy2=round(float(allse[s].split('|')[2]),0)
						if sx1==sx2 and sy1==sy2:
							allse.pop(s)
						else:
							sx1,sy1=sx2,sy2
							s=s+1
				except IndexError:
					break
			s=0
			for i in allse:
				if s==0:
					sx1=round(float(allse[s].split('|')[1]),4)
					sy1=round(float(allse[s].split('|')[2]),4)
					s=s+1
				else:
					sx2=round(float(allse[s].split('|')[1]),4)
					sy2=round(float(allse[s].split('|')[2]),4)
					if sx1==sx2 and sy1==sy2:
						allse.pop(s)
						s=s+1
					else:
						sx1,sy1=sx2,sy2
						s=s+1
			for i in range(0,len(allse)-1):
				listcoor.append(str((float(allse[i].split('|')[1])+float(allse[i+1].split('|')[1]))/2)+","+str((float(allse[i].split('|')[2])+float(allse[i+1].split('|')[2]))/2))
			for i in listcoor:
				cat=int((grass.read_command('v.what',map='gridCat',type='line',coordinates=i,distance='2',flags='g').split('\n')[-2]).split('=')[1])
				nlines=int((grass.read_command('db.select',flags='c',sql='select * from gridCat where cat="%s"' % (cat))).split('|')[-2])
				nlines=nlines+1
				grass.run_command('v.db.update',map='gridCat',column='npass',value=nlines,where='cat="%s"' % (cat))
			#unisco path_ind e path2_ind in un unico path_ind per poi potergli assegnare un'unica informazione temporale
			grass.run_command('v.patch',input='path_'+str(ind)+',path2_'+str(ind),output='path_tmp')
			grass.run_command('g.rename',vect='path_tmp,path_'+str(ind))
			#register the map in the stvds traffic
			startPo=start[ind-1]
			endPo=end[ind-1]
			#grass.run_command('t.register',input='traffic',maps='path_'+str(ind),type='vect',start=startPo,end=endPo)
	
	grass.run_command('g.remove',flags='f',type='vector', name='grid1,grid1l,gridl,grid2,grid2l,gridNocat,gridPoints,gridPruned,gridRegion,region1,gridOk,gridSegments,tmpPath2,tmpPath3,tmpPath4a,tmpPath6a')
	for i in grass.read_command('g.list',type='vect').split('\n')[2:]:
		for j in i.split(' '):
			if re.match('path2_',j):
				grass.run_command('g.remove',flags='f',type='vector',name=j)

def main():
	if not os.environ.has_key("GISBASE"):
		print "You must be in GRASS GIS to run this program."
		sys.exit(1)
	abbreviation = options['abbreviation']
	inputFile = options['data']
	coordDict = options['dict']
	land = options['land']
	outputGates = options['gates']
	outputGrid = options['grid']
	#added references options for temporal analyses
	period = options['period']
	moment = options['moment']
	#granularity in minutes
	granularity = options['grain']
	animation = flags['a']
	if moment and period:
		print "You must choose which kind of analysis to perform: if istantaneous or continue over a period"
		sys.exit(1)
	if moment and granularity:
		print "Granularity must be specified only for period analysis"
		sys.exit(1)
	if moment and animation:
		print "Animation can be performed only for period analysis"
		sys.exit(1)
	#start calculations
	r=open(inputFile,'r')
	d=r.readlines()
	d=d[2:]
	#extrapolate start and end in order to subset in reason of time moment/period
	startI=[]
	endI=[]
	for i in d:
		startI.append(i.split(';')[8])
		endI.append((i.split(';')[9]).split('\n')[0])
	#subset the initial database in reason of the analysis
	#istantaneous - I obtain a list, subset of d
	if moment:
		idxs=[]
		n=0
		for i in startI:
			if moment >= i and moment <= endI[n]:
				idxs.append(startI.index(i))
			n=n+1
		d=d[min(idxs):max(idxs)+1]
		nomi=[]
		start=[]
		end=[]
		for i in d:
			nomi.append(i.split(';')[7])
			start.append(i.split(';')[8])
			end.append((i.split(';')[9]).split('\n')[0])
		all=[]
		calculateMaps(nomi,abbreviation,coordDict,land,start,end)
		grass.run_command('g.copy',vect='gates,%s' % (outputGates))
		grass.run_command('g.copy',vect='gridCat,%s' % (outputGrid))
		grass.run_command('g.remove',flags='f',type='vector',name='gates,gridCat')
	#continuous - I obtain a list of lists, subsets of d
	if period:
		moments=[]
		st,en=period.split(',')
		startP = datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")
		endP = datetime.datetime.strptime(en, "%Y-%m-%d %H:%M:%S")
		curr = startP
		moments.append(st)
		while curr < endP:
			curr += datetime.timedelta(minutes=int(granularity))
			moments.append(str(curr))
		print "all the moments considered are:"
		print moments
		idxs=[]
		di=[]
		di2=[]
		for m in moments:
			tlist=[]
			n=0
			for i in startI:
				if m >= i and m <= endI[n]:
					idxs.append(startI.index(i))
				n=n+1
			tlist=d[min(idxs):max(idxs)+1]
			di.append(tlist)
		#didn't work because each time it summed up the previous partial lists too
		#it is necessary to subtract these elements from each partial list
		for i in range(len(di)):
			if i==0:
				di2.append(di[i])
			else:
				di2.append(list(set(di[i])-set(di[i-1])))
		#in di2 the records for each month are shuffled but correct
		frame=0
		for d in di2:
			nomi=[]
			start=[]
			end=[]
			for i in d:
				nomi.append(i.split(';')[7])
				start.append(i.split(';')[8])
				end.append((i.split(';')[9]).split('\n')[0])
			frame = frame + 1
			print '----------------------------------'
			print '                                  '
			print 'Elaborating frame nr. '+str(frame)
			print '                                  '
			print '----------------------------------'
			all=[]
			calculateMaps(nomi,abbreviation,coordDict,land,start,end)
			#NB. ho sempre il problema dei percorsi che si sdoppiano		
			grass.run_command('g.copy',vect='gates,%s' % (outputGates+'_'+str(frame)))
			grass.run_command('g.copy',vect='gridCat,%s' % (outputGrid+'_'+str(frame)))
			grass.run_command('g.remove',flags='f',type='vector',name='gates,gridCat')
	#if animation: ...
		
		

if __name__ == "__main__":
    options, flags = grass.parser()
    sys.exit(main())

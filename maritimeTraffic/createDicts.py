#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015, Annalisa Minelli
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details <http://www.gnu.org/licenses/>.
#
#importo sotto forma di csv (codifica utf-8 separatore=";") ed esporto in xcel
#importo il file originale dei semaforisti e lo spezzetto in una lista di liste
from collections import OrderedDict
import re,sys,xlwt
def main(dirty,modelf):
	p=open(dirty,'r')
	r=p.readlines()
	semaf=[]
	for i in r:
		semaf.append(i.split(";"))
	semaf=semaf[2:]
	#importo il file elaborato per farmi i vari dizionari
	f=open(modelf,'r')
	g=f.readlines()
	finale=[]
	types=[]
	routesr=[]
	routesraw=[]
	routescl=[]
	routesclean=[]
	t=[]
	for i in g:
		finale.append(i.split(";"))
	finale=finale[2:]
	for i in finale:
		types.append(i[9])
		routesr.append(re.split("> |vers |VERS |Vers |>",i[13]))
		routescl.append(i[19].split("\n")[0])
	for i in routesr:
		for g in i:
			t.append(((g.replace("-","")).strip()).upper())
		routesraw.append(filter(None,t))
		t=[]
	for i in routescl:
		routesclean.append(i.strip())
	typesoccurrences=list(OrderedDict.fromkeys(types))
	#creo il dizionario dei tipi di navi semplificati (typesdict)
	typentp=[]
	typesdict={}
	for g in typesoccurrences:
		for i in finale:
			if i[9]==g:
				typentp.append(i[10])
		ntpoccurrences=list(OrderedDict.fromkeys(typentp))
		typesdict[g]=ntpoccurrences
		typentp=[]
	#creo il dizionario dell'uso delle navi (usesdict) provo ad evincere l'uso dal nome della nave
	uses=[]
	for i in finale:
		uses.append(i[6])
	usesoccurrences=list(OrderedDict.fromkeys(uses))
	usentp=[]
	usesdict={}
	for g in usesoccurrences:
		for i in finale:
			if i[6]==g:
				usentp.append(i[3])
		uoccurrences=list(OrderedDict.fromkeys(usentp))
		usesdict[g]=uoccurrences
		usentp=[]
	#creo la lista delle routes possibili (ora parto dal file dei semaforisti, poi confronto con quello corretto)
#	routes=[]
#	for i in semaf:
#		routes.append(re.split("> |vers |VERS |Vers |>",i[5]))
#	routesc=[]
#	t=[]
#	for i in routes:
#		for g in i:
#			t.append(((g.replace("-","")).strip()).upper())
#		routesc.append(filter(None,t))
#		t=[]
#	routelist=[]
#	for i in routesc:
#		if i not in routelist:
#			routelist.append(i)
	#creo la stessa lista da quello corretto, la confronto con quella dei semaforisti e creo il dizionario delle routes in relazione a quelle individuate dagli studenti
	#già prodotte sopra le liste sono routesraw e routesclean
	#riduco routesclean per ottenere le sole routes che hanno identificato gli studenti:
	routecode=[]
	for i in routesclean:
		if i not in routecode:
			routecode.append(i)
	#questo mi sarà utile quando dovro' analizzare un file ex novo
	#ora occorre associare le routesraw ai routescode, uso routesclean perché é già indicizzato
	k=0
	routesall=[]
	for i in routesclean:
		b=[i,routesraw[k]]
		routesall.append(b)
		k=k+1
	routp=[]
	rouoccurrences=[]
	routedict={}
	for g in routecode:
		for i in routesall:
			if i[0]==g:
				routp.append(i[1])
		for f in routp:
			if f not in rouoccurrences:
				rouoccurrences.append(f)
		routedict[g]=rouoccurrences
		routp=[]
		rouoccurrences=[]
	return typesdict,usesdict,routedict

if __name__ == "__main__":
	dirty=sys.argv[1]
	modelf=sys.argv[2]
	tocleanf=sys.argv[3]
	a=main()
	typesdict,usesdict,routedict=a[0],a[1],a[2]
	p=open(toclean,'r')
	r=p.readlines()
	semaf=[]
	for i in r:
		semaf.append(i.split(";"))
	semaf=semaf[2:]
	mname=['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
	mois=[]
	date=[]
	heure=[]
	nom=[]
	matr=[]
	typeraw=[]
	routeraw2=[]
	for i in semaf:
		nr=int(i[0].split('/')[1])
		mois.append(mname[nr-1])
		date.append(i[0])
		heure.append(i[1])
		nom.append(i[2])
		matr.append(i[3])
		typeraw.append(i[4])
		routeraw2.append(re.split("> |vers |VERS |Vers |>",i[5]))
	router2=[]
	t=[]
	for i in routeraw2:
		for g in i:
			t.append(((g.replace("-","")).strip()).upper())
		router2.append(filter(None,t))
		t=[]
	finalroutes=[]
	for i in router2:
		for simp,raw in routedict.iteritems():
			if i in raw:
				finalroutes.append(simp)
#			else:
#				answer=raw_input("what is the route propre of "+i+str("? chose between: ")+(l for l in routecode))
#				finalroutes.append(answer)

	

	sys.exit(typesdict['voilier'])

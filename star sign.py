import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("D:/Work/MIS/finall-report/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

import requests as req
from bs4 import BeautifulSoup
import urllib.request as urequest
#import os
#import pyrebase
local_path="D:/Work/MIS/finall-report"

id=["牡羊座","金牛座","雙子座","巨蟹座","獅子座","處女座","天秤座","天蠍座","射手座","魔羯座","水瓶座","雙魚座"]
pics=[]
for i in range(12):
	url="https://astro.click108.com.tw/daily_"+str(i)+".php?iAstro=0"+str(i)
	request=urequest.Request(url,headers={
	"User-Agent":"Mozilla/5.0 (windows NT 16.0; Nin64; x64) ApplewebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.119 Safari/537.36"
	})
	Data = req.get(url)
	Data.encoding = "utf—8"
	sp = BeautifulSoup(Data.text, "html.parser")
	pic=sp.find_all("div",class_="TODAY_CONTENT")
	cont=sp.select("div.TODAY_CONTENT p")
	contt=sp.find_all("div",class_="TODAY_CONTENT")
	for i in pic:
		pics.append(i.find("h3").text+" ")
		for h in cont:
			pics.append(h.text)
title=[]
all_about_today=[]
explain_today=[]
love=[]
about_love=[]
bus=[]
about_bus=[]
money=[]
about_money=[]

for i in range(len(pics)):
	if i%9==0:
		title.append(pics[i])
	elif i%9==1:
		all_about_today.append(pics[i])
	elif i%9==2:
		explain_today.append(pics[i])
	elif i%9==3:
		love.append(pics[i])
	elif i%9==4:
		about_love.append(pics[i])
	elif i%9==5:
		bus.append(pics[i])
	elif i%9==6:
		about_bus.append(pics[i])
	elif i%9==7:
		money.append(pics[i])
	elif i%9==8:
		about_money.append(pics[i])
for i in range(len(id)):
	doc = {
	"id":i,
	"星座":id[i],
	"主題":title[i],
	"整體運勢":all_about_today[i],
	"整體運勢解析":explain_today[i],
	"愛情運勢":love[i],
	"愛情運勢解析":about_love[i],
	"事業運勢":bus[i],
	"事業運勢解析":about_bus[i] ,
	"財運運勢":money[i],
	"財運運勢解析":about_money[i]
	}
	doc_ref = db.collection("star sign") .document(str(i))
	doc_ref.set(doc)
import firebase_admin
from firebase_admin import credentials, firestore
import requests as req, json
import requests
from bs4 import BeautifulSoup
import urllib.request as urequest
from flask import Flask, render_template, request, make_response, jsonify

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>星座爬蟲資料庫存取，提供webhook</h1>"
    homepage += "<a href=/star_sign>讀取星座爬蟲資料庫，寫入Firestore</a><br><br>"
    homepage += "<a href=/query>星座資料庫查詢</a><br>"
    return homepage

@app.route("/star_sign")
def star_sign():
    id=["牡羊座","金牛座","雙子座","巨蟹座","獅子座","處女座","天秤座","天蠍座","射手座","魔羯座","水瓶座","雙魚座"]
    pics=[]
    for i in range(12):
        url="https://astro.click108.com.tw/daily_"+str(i)+".php?iAstro=0"+str(i)
        request=urequest.Request(url,headers={"User-Agent":"Mozilla/5.0 (windows NT 16.0; Nin64; x64) ApplewebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.119 Safari/537.36"})
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
    return "今日星座已爬蟲及存檔完畢" 

@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "POST":
        course = request.form["keyword"]

        collection_ref = db.collection("star sign")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if course in dict["星座"]:
                result += "星座名：<a href=" + dict["hyperlink"] + ">" + dict["星座"] + "</a><br>"
                result += "整體運勢：" + dict["整體運勢"] + "<br><br>"
                result += "愛情運勢：" + dict["愛情運勢"] + "<br><br>"
                result += "事業運勢：" + dict["事業運勢"] + "<br><br>"
                result += "財運運勢：" + dict["財運運勢"] + "<br><br>"
        if result == "":
            result = "抱歉，查無相關條件的星座資訊<br><br>"
        return result
    else:
        return render_template("query.html")

@app.route("/webhook1", methods=["POST"])
def webhook1():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req["queryResult"]["action"]
    msg =  req["queryResult"]["queryText"]
    info = "動作：" + action + "； 查詢內容：" + msg
    return make_response(jsonify({"fulfillmentText": info}))

@app.route("/webhook2", methods=["POST"])
def webhook2():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "rateChoice"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        info = "您選擇的電影分級是：" + rate
    return make_response(jsonify({"fulfillmentText": info}))

@app.route("/webhook3", methods=["POST"])
def webhook3():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "rateChoice"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        if (rate == "輔12級"):
            rate = "輔導級(未滿十二歲之兒童不得觀賞)"
        elif (rate == "輔15級"):
            rate = "輔導級(未滿十五歲之人不得觀賞)"
        info = "您選擇的電影分級是：" + rate + "，相關電影：\n"

        collection_ref = db.collection("子青電影")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["title"] + "\n"
                result += "介紹：" + dict["hyperlink"] + "\n\n"
        info += result
    return make_response(jsonify({"fulfillmentText": info}))

@app.route("/webhook4", methods=["POST"])
def webhook4():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "rateChoice"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        if (rate == "輔12級"):
            rate = "輔導級(未滿十二歲之兒童不得觀賞)"
        elif (rate == "輔15級"):
            rate = "輔導級(未滿十五歲之人不得觀賞)"
        info = "您選擇的電影分級是：" + rate + "，相關電影：\n"

        collection_ref = db.collection("子青電影")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["title"] + "\n"
                result += "介紹：" + dict["hyperlink"] + "\n\n"
        info += result
    elif (action == "MovieDetail"): 
        cond =  req.get("queryResult").get("parameters").get("FilmQ")
        keyword =  req.get("queryResult").get("parameters").get("any")
        info = "您要查詢電影的" + cond + "，關鍵字是：" + keyword + "\n\n"
    return make_response(jsonify({"fulfillmentText": info}))

@app.route("/webhook5", methods=["POST"])
def webhook5():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "rateChoice"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        if (rate == "輔12級"):
            rate = "輔導級(未滿十二歲之兒童不得觀賞)"
        elif (rate == "輔15級"):
            rate = "輔導級(未滿十五歲之人不得觀賞)"
        info = "您選擇的電影分級是：" + rate + "，相關電影：\n"

        collection_ref = db.collection("子青電影")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["title"] + "\n"
                result += "介紹：" + dict["hyperlink"] + "\n\n"
        info += result
    elif (action == "MovieDetail"): 
        cond =  req.get("queryResult").get("parameters").get("FilmQ")
        keyword =  req.get("queryResult").get("parameters").get("any")
        info = "您要查詢電影的" + cond + "，關鍵字是：" + keyword + "\n\n"
        if (cond == "片名"):
            collection_ref = db.collection("子青電影")
            docs = collection_ref.get()
            found = False
            for doc in docs:
                dict = doc.to_dict()
                if keyword in dict["title"]:
                    found = True 
                    info += "片名：" + dict["title"] + "\n"
                    info += "海報：" + dict["picture"] + "\n"
                    info += "影片介紹：" + dict["hyperlink"] + "\n"
                    info += "片長：" + dict["showLength"] + " 分鐘\n"
                    info += "分級：" + dict["rate"] + "\n" 
                    info += "上映日期：" + dict["showDate"] + "\n\n"
            if not found:
                info += "很抱歉，目前無符合這個關鍵字的相關電影喔"

    elif (action == "CityWeather"):
        city =  req.get("queryResult").get("parameters").get("city")
        token = "rdec-key-123-45678-011121314"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=" + token + "&format=JSON&locationName=" + str(city)
        Data = requests.get(url)
        Weather = json.loads(Data.text)["records"]["location"][0]["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
        Rain = json.loads(Data.text)["records"]["location"][0]["weatherElement"][1]["time"][0]["parameter"]["parameterName"]
        MinT = json.loads(Data.text)["records"]["location"][0]["weatherElement"][2]["time"][0]["parameter"]["parameterName"]
        MaxT = json.loads(Data.text)["records"]["location"][0]["weatherElement"][4]["time"][0]["parameter"]["parameterName"]
        info = city + "的天氣是" + Weather + "，降雨機率：" + Rain + "%"
        info += "，溫度：" + MinT + "-" + MaxT + "度"

    return make_response(jsonify({"fulfillmentText": info}))


if __name__ == "__main__":
    app.run()
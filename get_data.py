import json
import datetime


dinnerFood = dict()
def getFood():
    for i in range(1,4):
        with open('./data/eateries{num}.json'.format(num=i)) as f:
            data = json.load(f)

        eateries = data["data"]["eateries"]
        for i in range(len(eateries)):
            if "Dining Room" in eateries[i]["name"] or "Robert" in eateries[i]["name"] or "Oken" in eateries[i]["name"]:
                for j in range(len(eateries[i]["operatingHours"])):
                    date = eateries[i]["operatingHours"][j]["date"] 
                    dateArr = date.split("-")
                    dayOfWeek = datetime.date(day = int(dateArr[2]), month = int(dateArr[1]), year = int(dateArr[0])).strftime('%A %d %B %Y').split()[0]
                    dateHelper = eateries[i]["operatingHours"][j]
                    dinnerFood[(eateries[i]["name"], date, dayOfWeek)] = []
                    for k in range(len(dateHelper["events"])):
                        if dateHelper["events"][k]["descr"] ==  "Dinner":
                            dinnerMenu = dateHelper["events"][k]
                            for j in range(len(dinnerMenu["menu"])):
                                if dinnerMenu["menu"][j]["category"] == "Hot Traditional Station - Entrees" or \
                                dinnerMenu["menu"][j]["category"] == "Hot Traditional Station - Sides":
                                    for l in range(len(dinnerMenu["menu"][j]["items"])):
                                        addFood = dinnerFood[(eateries[i]["name"], date, dayOfWeek)]
                                        addFood.append(dinnerMenu["menu"][j]["items"][l]["item"].strip())
                                        dinnerFood[(eateries[i]["name"], date, dayOfWeek)] = addFood
    return dinnerFood


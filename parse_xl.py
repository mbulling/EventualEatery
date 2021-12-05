import pandas as pd
import datetime

xl = pd.ExcelFile('./data/becker menus.xlsx')
dinnerFood = dict()

for sheet in xl.sheet_names:
  df = xl.parse(sheet)
  head = df.columns[0]
  if head == "Breakfast" or head == "Brunch" or head == "Lunch":
    parseNext = False
    for index in range(len(df[head])):
      entry = df[head][index]
      if parseNext:
        addFood = [item.strip() for item in entry.split("*")]
        parseNext = False
      if entry == "Hot Traditional Station - Entrees" or entry == "Hot Traditional Station - Sides":
          parseNext = True
  else:
    parseNext = False
    addFood = []
    for index in range(len(df[head])):
      entry = df[head][index]
      if entry == "Specialty Station" or entry == "Beverage Station":
          parseNext = False
          break
      if parseNext and entry != "Hot Traditional Station - Sides":
        addFood.append(entry.strip())
      if entry == "Hot Traditional Station - Entrees" or entry == "Hot Traditional Station - Sides":
          parseNext = True
  date = sheet[-4:] + "-" + "-".join((sheet[:2], sheet[2: 4]))
  dateArr = date.split("-")
  dayOfWeek = datetime.date(day = int(dateArr[2]), month = int(dateArr[1]), year = int(dateArr[0])).strftime('%A %d %B %Y').split()[0]
  dinnerFood[(date, dayOfWeek)] = addFood
      

print(dinnerFood.keys())
print(dinnerFood)
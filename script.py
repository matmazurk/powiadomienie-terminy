import os
import time
import urllib.request
import json
import sys

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

locs = {
    "Kraków_wnioski": 129,
    "Kraków_odbior": 134,
    "Nowy Sącz": 253,
    "Tarnów": 252,
    "Gorlice": 251,
    "Limanowa": 250,
    "Olkusz": 249,
    "Oświęcim": 248,
    "Wadowice": 247
}

if len(sys.argv) < 2:
    print("Podaj miasto:")
    print(locs.keys())
    sys.exit(1)

id = locs.get(sys.argv[1])
if id is None:
    print("Miasto '{}' niedostępne".format(sys.argv[1]))
    print("Dostępne miasta:{}".format(list(locs.keys())))
    sys.exit(0)

print("====================================")

url = "https://bezkolejki.eu/api/Operation/GetFirstAvailableSlot?ids[0]={}".format(id)

while True:
    body = urllib.request.urlopen(url).read().decode('utf-8')
    j = json.loads(body)

    # print current timestamp
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(sys.argv[1])

    notification = ""
    for op in j[0]['operationSlots']:
        if op["dateTime"] is not None:
            print("{}- {}".format(op["operationName"], op["dateTime"]))
            notification += "{}- {}\n".format(op["operationName"], op["dateTime"])

    # notify if notification is not empty 
    if notification != "":
        notify("Nowe terminy paszportowe w {}".format(sys.argv[1]), notification)

    print("====================================")
    time.sleep(20 + (time.time() % 20 - 10))
    
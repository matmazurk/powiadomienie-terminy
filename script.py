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
    "Kraków": 129,
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

while True:
    body = urllib.request.urlopen("https://bezkolejki.eu/api/Operation/GetFirstAvailableSlot?ids[0]={}".format(id)).read().decode('utf-8')
    j = json.loads(body)

    # print current timestamp
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(sys.argv[1])
    wnioski = j[0]['operationSlots'][0]['dateTime']
    if wnioski is None:
        print("Wnioski- Brak terminów")
    else :
        print("Wnioski- {}".format(wnioski))

    odbior = j[0]['operationSlots'][1]['dateTime']
    if odbior is None:
        print("Odbiór- Brak terminów")
    else:
        notify("Termin odbioru {}".format(sys.argv[1]), "Odbiór- {}".format(odbior))
        print("Odbiór- {}".format(odbior))

    print("====================================")
    # sleep 1 minute +/- 10 seconds
    time.sleep(60 + (time.time() % 20 - 10))
    
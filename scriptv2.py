"""ScripV2"""
import json
from pickletools import long1


# from urllib import request, parse
import requests


def vulnerabilites():
    """ouais"""
    tab = []
    with open("vmoex-framework/bom.json", encoding="utf-8") as bom_datas:
        data = json.load(bom_datas)
    if "components" in data:
        if data["components"] is not None:
            for item in data["components"]:
                if "purl" in item and (item["purl"]).count("@") == 1:
                    if "?" in item["purl"]:
                        tmp = str(item["purl"]).split("?")
                        tab.append(tmp[0])
                    else:
                        tab.append(item["purl"])
    headers = {
        "accept": "application/vnd.ossindex.component-report.v1+json",
        "Content-Type": "application/vnd.ossindex.component-report-request.v1+json",
        "authorization": "Basic bG9hbi5kZS12b3NAYXZpc3RvLmNvbTp5enZtREh0WGRrMjAwMiQ=",
    }
    tab2 = []
    tab2.append("[")
    longueur_init=len(tab)
    limite_a_128_composants_par_requete(tab, tab2, headers,longueur_init)


def limite_a_128_composants_par_requete(tab, tab2, headers,longueur_init):
    """ouais2"""
    length = len(tab)
    print(length)
    tab2 = []
    tab2.append("[")
    final = []
    i = 0
    for purl in tab[0 : min(128, length)]:
        if i < min(127, length - 1):
            tab2.append('\n   "' + purl + '"')
            tab2.append(",")
            i += 1
        else:
            print("ok1")
            tab2.append('\n   "' + purl + '"\n  ')
            tab2.append("]")
    out = "".join(tab2)
    data = '{\n  "coordinates": ' + out + "\n}"
    print(data)
    response = requests.post(
        "https://ossindex.sonatype.org/api/v3/component-report",
        headers=headers,
        data=data,
    )
    print(response)
    dictresponse = response.json()
    for item in dictresponse:
        if item["vulnerabilities"] != []:
            for value in item["vulnerabilities"]:
                final.append(value["displayName"])
    if length > 128:
        limite_a_128_composants_par_requete(tab[128:], tab2, headers,longueur_init)
    for value in final:
        print(value)
    print(longueur_init)


vulnerabilites()

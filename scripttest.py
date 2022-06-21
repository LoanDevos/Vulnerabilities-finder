"""script"""
import json

# from urllib import request, parse
import time
import sys
import requests



def test_nbre_requetes():
    """ouais"""
    tab = []
    with open("vmoex-framework/bom.json", encoding="utf-8") as bom_datas:
        data = json.load(bom_datas)
    for k in range(len(data["components"])):
        for valeur in data["components"][k]:
            if valeur == "purl":
                if "@" in data["components"][k][valeur]:
                    tab.append(data["components"][k][valeur])
    # print(tab)
    headers = {
        "accept": "application/vnd.ossindex.component-report.v1+json",
        "Content-Type": "application/vnd.ossindex.component-report-request.v1+json",
        "authorization": "Basic bG9hbi5kZS12b3NAYXZpc3RvLmNvbTp5enZtREh0WGRrMjAwMiQ=",
    }
    for purl in tab:
        data = '{\n  "coordinates": [\n    "' + purl + '"\n  ]\n}'
        for i in range(500):
            response = requests.post(
                "https://ossindex.sonatype.org/api/v3/component-report",
                headers=headers,
                data=data,
            )
            if response.status_code != 200:
                print(i)
                sys.exit()

def test_temps_pour_recuperer_requete():
    """ouais"""
    tab = []
    tab1 = []
    tab2 = []
    tab3 = []
    with open("vmoex-framework/bom.json", encoding="utf-8") as bom_datas:
        data = json.load(bom_datas)
    for k in range(len(data["components"])):
        for valeur in data["components"][k]:
            if valeur == "purl":
                if "@" in data["components"][k][valeur]:
                    tab.append(data["components"][k][valeur])
    # print(tab)
    headers = {
        "accept": "application/vnd.ossindex.component-report.v1+json",
        "Content-Type": "application/vnd.ossindex.component-report-request.v1+json",
        "authorization": "Basic bG9hbi5kZS12b3NAYXZpc3RvLmNvbTp5enZtREh0WGRrMjAwMiQ=",
    }
    i = 0
    k = 0
    res = 0
    for purl in tab:
        data = '{\n  "coordinates": [\n    "' + purl + '"\n  ]\n}'
        for i in range(500):
            response = requests.post(
                "https://ossindex.sonatype.org/api/v3/component-report",
                headers=headers,
                data=data,
            )
            if response.status_code != 200:
                print(k)
                tab1.append(time.time())
                k += 1
                while response.status_code != 200:
                    response = requests.post(
                        "https://ossindex.sonatype.org/api/v3/component-report",
                        headers=headers,
                        data=data,
                    )
                    print(k)
                    k += 1
                tab2.append(time.time())
            print(k)
            print("i=" + str(i))
            k += 1
        print(tab1)
        print(tab2)
        for i, temps2 in enumerate(tab2):
            tab3.append(temps2 - tab1[i])
            res += temps2 - tab1[i]
        res = res / (len(tab2) - 1)
        print(tab3)
        print(res)
        sys.exit()


test_temps_pour_recuperer_requete()


# test_nbre_requetes()

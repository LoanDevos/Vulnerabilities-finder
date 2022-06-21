"""ScripV2"""
import json
# from urllib import request, parse
import requests


def vulnerabilites(string):
    """ouais"""
    tab = []
    with open(string, encoding="utf-8") as bom_datas:
        data = json.load(bom_datas)
    for k in range(len(data["components"])):
        for valeur in data["components"][k]:
            if valeur == "purl":
                if "@" in data["components"][k][valeur]:
                    if "?" in data["components"][k][valeur]:
                        tmp = str(data["components"][k][valeur]).split("?")
                        tab.append(tmp[0])
                    else:
                        tab.append(data["components"][k][valeur])
    headers = {
        "accept": "application/vnd.ossindex.component-report.v1+json",
        "Content-Type": "application/vnd.ossindex.component-report-request.v1+json",
        "authorization": "Basic bG9hbi5kZS12b3NAYXZpc3RvLmNvbTp5enZtREh0WGRrMjAwMiQ=",
    }
    tab2 = []
    tab2.append("[")
    tab_init = tab
    outfin = []
    return limite_a_128_composants_par_requete(
        tab, tab2, headers, tab_init, outfin
    )


def limite_a_128_composants_par_requete(
    tab, tab2, headers, tab_init, outfin
):
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
        limite_a_128_composants_par_requete(
            tab[128:], tab2, headers, tab_init, outfin
        )
    for value in final:
        print(value)
        outfin.append(value)
    print(len(final))

    return tab_init, outfin


BOMCDXGEN = "jib/bom.json"
BOMAUTRE = "bomtrivyjib.json"
purl1, vuln1 = vulnerabilites(BOMCDXGEN)
purl2, vuln2 = vulnerabilites(BOMAUTRE)

print("Nombre de composants cdxgen : ", len(purl1))
print("Nombre de composants Trivy : ", len(purl2))
print("Nombre de vulnérabilités cdxgen : ", len(vuln1))
print("Nombre de vulnérabilités Trivy : ", len(vuln2))
# print("Common Elements", set(purl1) & set(purl2))
#for purl in purl1:
 #   if purl not in purl2:
  #      print("composant de cdxgen",purl)
#for purl in purl2:
 #   if purl not in purl1:
  #      print("composant de trivy",purl)
print("Nombre de composants en commun : ", len(set(purl1) & set(purl2)))
# print("Common Elements", set(vuln1) & set(vuln2))
print("Nombre de vulnérabilités en commun : ", len(set(vuln1) & set(vuln2)))

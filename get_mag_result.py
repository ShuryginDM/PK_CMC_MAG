import requests

CMC_LINK_1 = "http://pk.cs.msu.ru/node/1415"
CMC_LINK_2 = "http://pk.cs.msu.ru/node/1428"

def crop(t, s, m):
    return t[t.find(s)+len(s):] if m else t[:t.find(s)]

def get_admittion_table(LINK):
    q = ""
    try:
        request_result = requests.get(LINK)
        request_result.raise_for_status()
        q = request_result.text
        q = crop(q, "<table", 1)
        q = crop(q, "</table>", 0)

    except requests.exceptions.ConnectTimeout:
        fail = 2
    except requests.exceptions.ReadTimeout:
        fail = 3
    except requests.exceptions.ConnectionError:
        fail = 1
    except requests.exceptions.HTTPError as err:
        fail = 4
        HTTPErrNum = err
    return q

def get_mark_list(q):
    lst = {}
    q = crop(q, "<tr", 1)
    while(q.find("<tr") != -1):
        q = crop(q, "<tr", 1)
        q = crop(q, "<td", 1)
        q = crop(q, "<td", 1)
        q = crop(q, ">", 1)
        itm = int(crop(q, "<", 0))
        if(lst.get(itm) == None):
            lst[itm] = 1
        else:
            lst[itm] = lst[itm] + 1
    return lst


q = get_admittion_table(CMC_LINK_1)
lst1 = get_mark_list(q)
q = get_admittion_table(CMC_LINK_2)
lst2 = get_mark_list(q)
lst = {}
sum = 0
for i in lst1.keys():
    lst[i] = lst1[i]
for i in lst2.keys():
    if(lst.get(i) == None):
        lst[i] = lst2[i]
    else:
        lst[i] = lst[i] + lst2[i]
for i in sorted(lst.keys()):
    print(str(i) + " : " + str(lst[i]))
    if i != 2:
        sum += lst[i]
print("-------------------")
print("SUM = " + str(sum))




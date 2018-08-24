from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import json
from elasticsearch import Elasticsearch
reg_url = "https://health.usnews.com/doctors/city-index/new-jersey"
#Extracting the cities


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'

print("This is happening.")

#Elastic stuff

es=Elasticsearch()
id1=1


def Merged(a, b):
    c = ""

    for good in range(0, len(a)):
        c = c + "," + a[good]+" " + b[good]
    return c




def Elastic_Search(search_dict):
    global id1
    r=es.index(index="doctorsus", doc_type="info", id=id1, body=search_dict)
    id1=id1+1
    print(r)
    return

#City names
def City_Names_Function():
    request = urlopen(Request(str(reg_url), data=None, headers={
        'User-Agent': user_agent}))  # send an HTTP request to the url, along with the headers sent: user agent.

    soup=BeautifulSoup(request,"html.parser")     #parses the data received so that it is readable to beautiful soup
    city_name = soup.findAll("li", attrs={"class": "List__ListItem-dl3d8e-1 kfaWAY"})       #the findAll() method takes 2 parameters: One, which defines the tag
    i=0                                                                                #2nd, which defines the attributes of the specific tag.
    city=[]
    for a in city_name:
        city.insert(i, a.text.strip())
        i=i+1
    #print(city[0])
    return city



#print the specific city's name.


def Zipcode_extract(address):
    string_address = str(address)
    length = len(string_address)
    zipcode = string_address[length-8:length-2]
    return zipcode

def Remove_special_stuff(string):
    string_value = str(string)
    if(string_value.__contains__("\n")):
        string_value.replace("\n", " : ")
    return string_value





spec_url = "https://health.usnews.com/doctors/specialists-index/new-jersey"
extreme=0
city=City_Names_Function()
for city_name in city[0:1]:
    if (str(city_name).__contains__(" ")):
            city_name = str(city_name).replace(" ", "-")
    updated_url=spec_url+"/"+city_name.lower()
    #print(updated_url)
    request = urlopen(Request(str(updated_url), data=None, headers={'User-Agent': user_agent}))
    soup=BeautifulSoup(request,"html.parser")
    spec_name = soup.findAll("li", attrs={"class": "List__ListItem-dl3d8e-1 kfaWAY"})
    list2=[]
    i=0
    for link in spec_name:
        list2.insert(i, link.a.get("href"))
        i=i+1
    print(list2[0])
    outer=0
    for doctor_spec_name in list2[0:1]:
        if (str(doctor_spec_name).__contains__(" ")):
            doctor_name = str(doctor_spec_name).replace(" ", "-")
        toReachDoctor_url = "https://health.usnews.com"+doctor_spec_name.lower()
        print(toReachDoctor_url)
        request = urlopen(Request(str(toReachDoctor_url), data=None, headers={'User-Agent': user_agent}))
        soup = BeautifulSoup(request, "html.parser")
        doctor_real_url = []
        i = 0
        for abc in soup.findAll("a", {"class": "search-result-link bar-tighter", "href": True}):
                doctor_real_url.insert(i, abc.get("href"))     #url extraction
                i=i+1
                print(doctor_real_url)

        the_doctors_loop_it = 0
        for the_doctors_loop in doctor_real_url[0:10]:
            print("THIS IS THE DOCTOR : "+the_doctors_loop)
            #The name and opening the page of the doctor
            try:
                new_url = "https://health.usnews.com"+the_doctors_loop
                print("This is the doctor url now !!!"+new_url)
                print("Doctor's city : "+city_name)
                request = urlopen(Request(str(new_url), data=None, headers={'User-Agent': user_agent}))
                soup = BeautifulSoup(request, "html.parser")
                i = 0

                #Doctors name

                hello = soup.findAll("h1", attrs={"class": "hero-heading flex-media-heading block-tight doctor-name "})
                name = []
                i=0
                for x in hello:
                    name.insert(i, x.text.strip())
                    i=i+1
                print("The NAME of the doctor is : "+name[0])


                #The Overview

                hello1 = soup.findAll("div", attrs={"class": "block-normal clearfix"})
                over = []
                i=0
                for x in hello1:
                    over.insert(i, x.text.strip())
                    i=i+1
                #print("The OVERVIEW of the doctor is : "+over[0])

                #The number of years in practice
                i=0
                hello2 = soup.findAll("span", attrs={"class": "text-large heading-normal-for-small-only right-for-medium-up"})
                years = []
                for x in hello2:
                    years.insert(i, x.text.strip())
                    i=i+1
                #print("YEARS IN PRACTICE : "+years[1])

                #The language


                hello3 = soup.findAll("span", attrs={"class": "text-large heading-normal-for-small-only right-for-medium-up text-right showmore"})
                lang = []
                zip = []
                i=0
                for x in hello3:
                    lang.insert(i, x.text.strip())
                    i = i+1
                #print("The LANGUAGE IS : "+lang[0])

                #Office in location

                hello4 = soup.findAll("span", attrs={"class": "text-strong", "data-js-id": True})
                office = []
                j=0
                for x in hello4:
                    office.insert(i, x.text.strip())
                    zip.insert(j, Zipcode_extract(office))
                    i=i+1
                    j=j+1
                #print("The LOCATION OF THE OFFICE : "+office[0])

                #print("The zipcode is : "+zip[0])




                #Hospital Affiliation

                hello5 = soup.findAll("a", {"class": "heading-larger block-tight", "href": True})
                hello6 = soup.findAll("section", {"class": "doctors-hospitals block-loosest"})
                HA = []
                i=0
                for x in hello6:
                    HA.insert(i, x.text.strip())
                    i=i+1
                #print("The HOSPITAL AFFILIATION IS : "+HA[0])

                #HA link
                for a in hello5:
                        affiliation = a["href"]     #url extraction
                        #print("The AFFILIATION LINK IS : "+affiliation)

                #Specialties and sub specialities

                hello7 = soup.findAll("a", {"class": "text-large", "href": True})
                speciality = []
                i=0
                for x in hello7:
                    speciality.insert(i, x.text.strip())
                    i=i+1
                #print("The SPECIALITY is : "+speciality[0])

                hello8 = soup.findAll("p", {"class": "text-large block-tight"})
                subs=[]
                i=0
                for x in hello8:
                    subs.insert(i, x.text.strip())
                    i=i+1
                #print("The SUB SPECIALITY IS : "+subs[0])

                #Education and medical training
                c=5
                i = 0
                edu=[]
                #print("The eduction is : ")
                hello9 = soup.findAll("section", {"class": "block-loosest"})
                if len(hello9[5].findChildren("ul", recursive=False))==0:
                    c+=1

                    hello9 = hello9[c].findChildren("ul", recursive=False)
                    hello9 = hello9[0].findChildren("li", recursive=True)

                else:
                    hello9 = hello9[c].findChildren("ul", recursive=False)
                    hello9 = hello9[0].findChildren("li", recursive=True)

                for x in hello9:
                    edu.insert(i, str(x.text.strip()).strip())
                    i=i+1
                education = Remove_special_stuff(edu)
                #print(education)

                #The certifications are

                hello10 = soup.findAll("section", {"class": "block-loosest"})
                hello10 = hello10[6].findChildren("ul", recursive=False)
                hello10 = hello10[0].findChildren("li", recursive=True)
                certs=[]
                i=0

                for x in hello10:
                    certs.insert(i, str(x.text.strip()).strip())
                    i=i+1
                #print(certs)
                #print("The NEW CITY: "+city_name)
                search_dict = {
                    "city": city_name,
                    "zipcode": zip,
                    "years": years,
                    "specialization": speciality
                    }
                Elastic_Search(search_dict)

            except:
                certs=None
                edu=None


            the_doctors_loop_it = the_doctors_loop_it + 1

        outer=outer+1


    extreme = extreme + 1



def City_Search():
    key=[]
    values=[]
    one = 0
    response = es.search(
            index="doctorsus",
            body={
                "aggs": {
                    "genres": {
                        "terms": {"field": "city.keyword"
                                  }
                    }
                }
            }

        )

    response = response['aggregations']['genres']['buckets']
    for i in response:
        j = str(i)
        x = j.find(',')
        j = j[0:x]
        y = j.find(':')
        ans = j[y + 1:x]
        key.insert(one, str(ans.strip()))
        one = one + 1
        print key
    one = 0
    for i in response:
        j = str(i)
        x = j.find(',')
        j = j[x:len(j)]
        y = j.find(':')
        ans = j[y + 1:len(j) - 1]
        values.insert(one, str(ans.strip()))
        one = one + 1
        print(values)

    return Merged(key, values)



def Specialization_Search():
    key = []
    values = []
    one = 0
    response = es.search(
        index="doctorsus",
        body={
            "aggs": {
                "genres": {
                    "terms": {"field": "specialization.keyword"
                              }
                }
            }
        }

    )

    response = response['aggregations']['genres']['buckets']
    for i in response:
        j = str(i)
        x = j.find(',')
        j = j[0:x]
        y = j.find(':')
        ans = j[y + 1:x]
        key.insert(one, str(ans.strip()))
        one = one + 1
        print key
    one = 0
    for i in response:
        j = str(i)
        x = j.find(',')
        j = j[x:len(j)]
        y = j.find(':')
        ans = j[y + 1:len(j) - 1]
        values.insert(one, str(ans.strip()))
        one = one + 1
        print(values)

    return Merged(key, values)



def Zipcode_Search():
    key = []
    values = []
    one = 0
    response = es.search(
        index="doctorsus",
        body={
            "aggs": {
                "genres": {
                    "terms": {"field": "zipcode.keyword"
                              }
                }
            }
        }

    )

    response = response['aggregations']['genres']['buckets']
    for i in response:
        j = str(i)
        x = j.find(',')
        j = j[0:x]
        y = j.find(':')
        ans = j[y + 1:x]
        key.insert(one, str(ans.strip()))
        one = one + 1
        print key
    one = 0
    for i in response:
        j = str(i)
        x = j.find(',')
        j = j[x:len(j)]
        y = j.find(':')
        ans = j[y + 1:len(j) - 1]
        values.insert(one, str(ans.strip()))
        one = one + 1
        print(values)

    return Merged(key, values)





def Years_Search():
    key = []
    values = []
    one = 0
    response = es.search(
        index="doctorsus",
        body={
            "aggs": {
                "genres": {
                    "terms": {"field": "years.keyword"
                              }
                }
            }
        }

    )

    response = response['aggregations']['genres']['buckets']
    for i in response:
        j = str(i)
        x = j.find(',')
        j = j[0:x]
        y = j.find(':')
        ans = j[y + 1:x]
        key.insert(one, str(ans.strip()))
        one = one + 1
        print key
    one = 0
    for i in response:
        j = str(i)
        x = j.find(',')
        j = j[x:len(j)]
        y = j.find(':')
        ans = j[y + 1:len(j) - 1]
        values.insert(one, str(ans.strip()))
        one = one + 1
        print(values)

    return Merged(key, values)


def Output():
    city_out = City_Search()
    spec_out = Specialization_Search()
    zipcode_out = Zipcode_Search()
    years_out = Years_Search()

    output_dict = {
        "city_output":  city_out,
        "special_out": spec_out,
        "zipcode_out": zipcode_out,
        "years_out": years_out
}

    with open(".analysis_result.json", "w") as write_file:
        json.dump(output_dict, write_file)

Output()













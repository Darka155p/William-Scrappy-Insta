# -*- coding: utf-8 -*-
# William

import time
import random
import csv
import re 
import bs4
from random import randint
import datetime as dt
import pandas as pd
import sys
import requests
import json

def getDataframe(valuesSettings):
    df = pd.DataFrame.from_records(valuesSettings)
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    #df['Division']=df['Division'].str.title()
    return df.reset_index(drop=True)

def loginInstagram(usernameD,paswordD):
    baseUrl='https://www.instagram.com/'
    loginUrl=baseUrl+'accounts/login/ajax/'
    username=usernameD
    pasword=paswordD
    session = requests.Session()
    head = {'Content-type':'application/json','Accept':'application/json'}
    userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    session.headers={'user-agent':userAgent}
    session.headers.update({'Referer':baseUrl})
    req=session.get(baseUrl)
    session.headers.update({'X-CSRFToken':req.cookies['csrftoken']})
    login_data={'username':username,'password':pasword}
    login=session.post(loginUrl,data=login_data,allow_redirects=True)
    session.headers.update({'X-CSRFToken':login.cookies['csrftoken']})
    cookies=login.cookies
    return session,head

def nombre(usernameD):
    userName = usernameD
    base = 'https://www.instagram.com/'
    user = base + userName
    return(user)
    
    
    
#resp = requests.get('https://www.instagram.com/traficocpanama/')
#resp = requests.get('https://www.prensa.com/')
#soup = bs4.BeautifulSoup(resp.text, 'html5lib')
#print(soup)
#for tag in soup.find_all(True):
  #  print(tag.name)
#Linksarticul = soup.find_all("text")
#print(Linksarticul)


def main(username,pwd,TIPO,PARAMQUERY):
    session,head=loginInstagram(username,pwd)
    prueba = nombre(username)
    #print(prueba)
    try:


        urlScraping='https://www.instagram.com/web/search/topsearch/?context=TIPO&query=PARAMQUERY'
        for rowPARAMQUERY in PARAMQUERY:
            baseUrl='https://www.instagram.com/'
            link = baseUrl + username
            has_next_page = 'true'
            usuariosARRAY=[]
            usersARRAY=[]
            hashtagARRAY=[]
            placesARRAY=[]
            try:
                url=urlScraping.replace('PARAMQUERY',rowPARAMQUERY).replace('TIPO',TIPO)
                print(url)
                response=session.get(url,headers=head)
                if(TIPO=='user'):
                    users=response.json()['users']
                    for xusers in users:
                        position=xusers['position']
                        infoUser=xusers['user']
                        pk=infoUser['pk']
                        username=infoUser['username']
                        usuariosARRAY.append(['https://www.instagram.com/'+username,username])
                       # print(username)
                        full_name=infoUser['full_name']
                        usersARRAY.append([position,pk,username,full_name,'https://www.instagram.com/'+username])
                    df = getDataframe([['position','pk','username','full_name','link_de_user']]+usersARRAY) 
                    df.to_csv(TIPO+rowPARAMQUERY+'.csv',  index=False, sep=',', encoding='utf-8' )
                    
                    #df = getDataframe(['links','usermane']+usuariosARRAY)
                    #df.to_csv(TIPO+rowPARAMQUERY+'.csv',  index=False, sep=',', encoding='utf-8' )
                    
                elif(TIPO=='hashtag'):
                    hashtags=response.json()['hashtags']
                    for xhashtags in hashtags:
                        position=xhashtags['position']
                        infohashtag=xhashtags['hashtag']
                        name=infohashtag['name']
                        id=infohashtag['id']
                        media_count=infohashtag['media_count']
                        hashtagARRAY.append([position,name,id,media_count,'https://www.instagram.com/explore/tags/'+name])
                    df = getDataframe([['position','name','id','media_count','links']]+hashtagARRAY)   
                    df.to_csv(TIPO+rowPARAMQUERY+'.csv',  index=False, sep=',', encoding='utf-8' )
                    
                elif(TIPO=='place'):
                    places=response.json()['places']
                    for xplaces in places:
                        position=xplaces['position']
                        infoplaces=xplaces['place']['location']
                        try:
                            lng=infoplaces['lng']
                        except Exception as e:
                            lng=''
                        try:
                            lat=infoplaces['lat']
                        except Exception as e:
                            lat=''
                        pk=infoplaces['pk']
                        name=infoplaces['name']
                        address=infoplaces['address']
                        city=infoplaces['city']
                        placesARRAY.append([position,pk,lng,lat,name,address,city])
                    df = getDataframe([['position','pk','lng','lat','address','city']]+placesARRAY)   
                    df.to_csv(TIPO+rowPARAMQUERY+'.csv',  index=False, sep=',', encoding='utf-8' )
                    
            except Exception as e:
                print("Main Exception: "+str(e))

    except Exception as e:
        print("Main Exception: "+str(e))




if __name__ == '__main__':
    username=''
    pwd=''
#------------------------------------------------------------------------
    # Usuarios 
    
    typo='users'
    queries=['diaadiapa']
    main(username,pwd,typo,queries)
    
    typo='users'
    queries=['criticapa']
    main(username,pwd,typo,queries)
    
    typo='users'
    queries=['prensacom']
    main(username,pwd,typo,queries)

    typo='users'
    queries=['elsiglodigital']
    main(username,pwd,typo,queries)
    
    typo='users'
    queries=['traficocpanama']
    main(username,pwd,typo,queries)
    
#------------------------------------------------------------------------- 
    # Hasgtag
    
    typo='hashtag'
    queries=['panama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['SARSCoV2panama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['SARSCoV2panamá']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['SARS-CoV-2panama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['SARS-CoV-2panamá']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['coronaviruspanama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['coronaviruspanamá']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['coronavíruspanama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['coronavirusenpanama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['coronaviruspanama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['coronaviruspanamá2020']
    main(username,pwd,typo,queries)
        
    typo='hashtag'
    queries=['2019-nCoVpanama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['2019-nCoVpanamá']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['2019 Novel Coronaviruspanama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['2019 Novel Coronaviruspanamá']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['pandemiapanama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['pandemiapanamá']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['covid19panama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['covid19panamá']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['covidpanama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['covidpanamá']
    main(username,pwd,typo,queries)
    
    # Hasta aqui es las busqueda relacionado con panama
    
    typo='hashtag'
    queries=['covid19']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['SARSCoV2']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['traficopanama']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['SARS-CoV-2']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['Coronavirus']
    main(username,pwd,typo,queries)

    typo='hashtag'
    queries=['2019-nCoV']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['2019 Novel Coronavirus']
    main(username,pwd,typo,queries)
        
    typo='hashtag'
    queries=['pandemic']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['social distancing']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['outbreak']
    main(username,pwd,typo,queries)
    
    typo='hashtag'
    queries=['covid19panama']
    main(username,pwd,typo,queries)
    
#-------------------------------------------------------------------------
    # Lugares
    
    typo='place'
    queries=['Panama. San Miguelito']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['panama']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['panamá']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital Santo Tomás']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital Del Niño Dr. José Renàn Esquivel']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital San Miguel Arcángel']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital Punta Pacífica']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital Nacional De Panama']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital Nacional De Panamá']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital San Fernando']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital Santa Fe']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital Paitilla']
    main(username,pwd,typo,queries)
    
    typo='place'
    queries=['Hospital De Especialidades Pediatricas']
    main(username,pwd,typo,queries)
    

# coding:utf-8

import requests
import getpass
import time
from bs4 import BeautifulSoup

#menuURL='http://4m3.tongji.edu.cn/eams/home!submenus.action?menu.id='
#welcomeURL='http://4m3.tongji.edu.cn/eams/home!welcome.action'

def login(username,password,header,s):

    startURL='http://4m3.tongji.edu.cn/eams/login.action'
    href='http://4m3.tongji.edu.cn/eams/samlCheck'
    res=s.get(startURL)
    header['Upgrade-Insecure-Requests']='1'
    res=s.get(href,headers=header)
    soup=BeautifulSoup(res.content,'html.parser')
    jumpURL=soup.meta['content'][6:].encode('utf-8')
    header['Accept-Encoding']='gzip, deflate, sdch, br'
    res=s.get(jumpURL,headers=header,verify=False)

    soup=BeautifulSoup(res.content,'html.parser')
    logPageURL='https://ids.tongji.edu.cn:8443'+soup.form['action'].encode('utf-8')
    res=s.get(logPageURL,headers=header)

    data={'option':'credential','Ecom_User_ID':username,'Ecom_Password':password,'submit':'%E7%99%BB%E5%BD%95'}
    soup=BeautifulSoup(res.content,'html.parser')
    loginURL=soup.form['action'].encode('utf-8')
    res=s.post(loginURL,headers=header,data=data)

    soup=BeautifulSoup(res.content,'html.parser')
    str=soup.script.string.encode('utf-8')
    str=str.replace('<!--',' ')
    str=str.replace('-->',' ')
    str=str.replace('top.location.href=\'',' ')
    str=str.replace('\';',' ')
    jumpPage2=str.strip()
    res=s.get(jumpPage2,headers=header)

    soup=BeautifulSoup(res.content,'html.parser')
    message={}
    messURL=soup.form['action'].encode('utf-8')
    message['SAMLResponse']=soup.input['value'].encode('utf-8')
    message['RelayState']=soup.input.next_sibling.next_sibling['value'].encode('utf-8')
    res=s.post(messURL,headers=header,data=message)

def getTablet(header,s):

    tableURL='http://4m3.tongji.edu.cn/eams/courseTableForStd!index.action'
    data={'ignoreHead':'1','setting.kind':'std','startWeek':'1','semester.id':'103','ids':''}
    res=s.post(tableURL,headers=header,data=data)
    soup=BeautifulSoup(res.content,'html.parser')
    for str in soup.find_all(name='script',language='JavaScript'):
        string=str.get_text()
        pos=string.find('ids')
        data['ids']=string[pos+6:pos+15]

    courseURL='http://4m3.tongji.edu.cn/eams/courseTableForStd!courseTable.action'
    res=s.post(courseURL,headers=header,data=data)

def getTime():#时间戳

    timeCode=str(int(time.time()*1000))
    return timeCode

def getCourse(header,s,course):

    courseURL='http://4m3.tongji.edu.cn/eams/doorOfStdElectCourse.action?_='+getTime()
    res=s.get(courseURL,headers=header)

    soup=BeautifulSoup(res.content,'html.parser')
    str=soup.a['href']
    pos=str.find('id')
    turnId=str[pos+3:pos+7]
    
    enterURL='http://4m3.tongji.edu.cn/eams/sJStdElectCourse!defaultPage.action?electionProfile.id='+turnId;
    res=s.get(enterURL,headers=header)

    readCourseURL='http://4m3.tongji.edu.cn/eams/sJStdElectCourse!data.action?profileId='+turnId
    res=s.get(readCourseURL,headers=header)
    string=res.content.decode('utf-8')
    pos=string.find(course)
    courseID=string[pos-20:pos-5]

    stdNumURL='http://4m3.tongji.edu.cn/eams/sJStdElectCourse!queryStdCount.action?profileId='+turnId;
    while True:
        res=s.get(stdNumURL,headers=header)
        string=res.content.decode('utf-8')
        pos=string.find(courseID)
        scstr=str(string[pos+21:pos+25])
        scstr=filter(str.isdigit,scstr)
        scnum=int(scstr)#获得当前人数
        lcstr=str(string[pos+25:pos+30])
        lcstr=filter(str.isdigit,lcstr)
        lcnum=int(lcstr)#获得容量上限
    
        if scnum<lcnum:
            catchCourseURL='http://4m3.tongji.edu.cn/eams/sJStdElectCourse!batchOperator.action'
            data='?electLessonIds='+courseID
            catchCourseURL+=data
            catchCourseURL=catchCourseURL+'&_='+getTime()
            res=s.get(catchCourseURL,headers=header)
            string=res.content.decode('utf-8')

            sign=unicode('选课成功','utf-8')
            if string.find(sign)!=-1:
                print 'succeeded to catch your course.'
                break

def main():
        username=input('Please enter your username: ')
        password=getpass.getpass('Please enter your password: ')
        header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        s=requests.session()
        course=input('Please enter the id of the course you want: ')

        try:
            login(username,password,header,s)
        except:
            print 'failed to login, please try again!'

        try:
            getCourse(header,s,str(course))
        except:
            print 'failed to catch the course!'

if __name__=='__main__':
    main()
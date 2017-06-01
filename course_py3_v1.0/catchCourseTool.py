# coding:utf-8

import requests
import getpass
import time
import re
from bs4 import BeautifulSoup

import mail

#menuURL='http://4m3.tongji.edu.cn/eams/home!submenus.action?menu.id='
#welcomeURL='http://4m3.tongji.edu.cn/eams/home!welcome.action'

def login(username,password,header,s):

    startURL='http://4m3.tongji.edu.cn/eams/login.action'
    href='http://4m3.tongji.edu.cn/eams/samlCheck'
    res=s.get(startURL)
    header['Upgrade-Insecure-Requests']='1'
    res=s.get(href,headers=header)
    soup=BeautifulSoup(res.content,'html.parser')
    jumpURL=soup.meta['content'][6:]
    header['Accept-Encoding']='gzip, deflate, sdch, br'
    res=s.get(jumpURL,headers=header,verify=False)

    soup=BeautifulSoup(res.content,'html.parser')
    logPageURL='https://ids.tongji.edu.cn:8443'+soup.form['action']
    res=s.get(logPageURL,headers=header)

    data={'option':'credential','Ecom_User_ID':username,'Ecom_Password':password,'submit':'登录'}
    soup=BeautifulSoup(res.content,'html.parser')
    loginURL=soup.form['action']
    res=s.post(loginURL,headers=header,data=data)

    soup=BeautifulSoup(res.content,'html.parser')
    str=soup.script.string
    str=str.replace('<!--',' ')
    str=str.replace('-->',' ')
    str=str.replace('top.location.href=\'',' ')
    str=str.replace('\';',' ')
    jumpPage2=str.strip()
    res=s.get(jumpPage2,headers=header)

    soup=BeautifulSoup(res.content,'html.parser')
    message={}
    messURL=soup.form['action']
    message['SAMLResponse']=soup.input['value']
    message['RelayState']=soup.input.next_sibling.next_sibling['value']
    res=s.post(messURL,headers=header,data=message)
    #print res.content.decode('utf-8')

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

    print (res.content)

def getTime():#时间戳

    timeCode=str(int(time.time()*1000))
    return timeCode

def getCourse(header,s,course):

    courseURL='http://4m3.tongji.edu.cn/eams/doorOfStdElectCourse.action?_='+getTime()
    res=s.get(courseURL,headers=header)


    enterURL='http://4m3.tongji.edu.cn/eams/sJStdElectCourse!defaultPage.action?electionProfile.id=3883'
    res=s.get(enterURL,headers=header)

    readCourseURL='http://4m3.tongji.edu.cn/eams/sJStdElectCourse!data.action?profileId=3883'
    res=s.get(readCourseURL,headers=header)
    string=res.content.decode('utf-8')
    pos=string.find(course)
    courseID=string[pos-20:pos-5]
    
    stdNumURL='http://4m3.tongji.edu.cn/eams/sJStdElectCourse!queryStdCount.action?profileId=3883'
    while True:
        time.sleep(1)
        res=s.get(stdNumURL,headers=header)
        string=res.content.decode('utf-8')
        pos=string.find(courseID)
        scstr=str(string[pos+21:pos+25])
        scnum=int(re.sub('\D','',scstr))#获得当前人数
        lcstr=str(string[pos+25:pos+30])
        lcnum=int(re.sub('\D','',lcstr))#获得容量
    
        if scnum<lcnum:
            catchCourseURL='http://4m3.tongji.edu.cn/eams/sJStdElectCourse!batchOperator.action'
            data='?electLessonIds='+courseID
            catchCourseURL+=data
            catchCourseURL=catchCourseURL+'&_='+getTime()
            res=s.get(catchCourseURL,headers=header)
            string=res.content.decode('utf-8')

            if string.find('选课成功')!=-1:
                return True

def main():
        username=input('Please enter your username: ')
        password=getpass.getpass('Please enter your password: ')
        header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        s=requests.session()
        course=input('Please enter the id of the course you want: ')

        success=False
        sender=input('Please enter your e-mail address: ')
        mailPassword=getpass.getpass('Please enter the password: ')
        sucSubject='Congratulations!'
        falSubject='Sorry'
        sucBody='I have caught your course.'
        falBody='I can not catch your course.'
        
        try:
            login(username,password,header,s)
        except:
            print('failed to login, please try again!')

        try:
            success=getCourse(header,s,str(course))
        except:
            print('failed to catch the course!')

        try:
            if success:
                mail.sendMail(sender,mailPassword,sender,sucSubject,sucBody)
            else:
                mail.sendMail(sender,mailPassword,sender,falSubject,falBody)
        except:
            print('failed to send the mail.')

if __name__=='__main__':
    main()

#2021年8月16日  8点11分
import os
import time
import random
import datetime
import requests
#from captcha import captchaget
from fake_useragent import UserAgent

#关闭安全验证请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


di = {}
path1 = os.getcwd()
ua = UserAgent()
agent = ua.random

login = 'http://jwxt.imu.edu.cn/login'
yzmurl = 'http://jwxt.imu.edu.cn/img/captcha.jpg?'
checkurl = 'http://jwxt.imu.edu.cn/j_spring_security_check'
kcurl = 'http://jwxt.imu.edu.cn/student/courseSelect/freeCourse/courseList'

url = 'http://jwxt.imu.edu.cn/student/courseSelect/courseSelect/index'

s=requests.session()
cookie = 'abcp3d6mFM8CFTba5S41Ux'

headers={
    'accept-language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'User-Agent': agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://jwxt.imu.edu.cn/index.jsp',
    'Accept-Encoding': 'gzip, deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'sec-ch-ua': '''"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"''',
    'Cookie': 'JSESSIONID=' + cookie
    }

def tokenget(s):
    url = 'http://jwxt.imu.edu.cn/student/courseSelect/courseSelect/index'
    rs=s.get(url,headers=headers,verify=False)
    ui = rs.text
    shun = ui.index('type="hidden" id="tokenValue" value=') + 37
    valuetoken = ui[shun:shun+32]
    return valuetoken


def dicturn(ui):
    ui = ui.replace('false','False')
    ui = ui.replace('true','True')
    ui = ui.replace('null','')
    ui = ui.replace('\/','')
    return ui

def loginandcookie(login,yzmurl,s):
    ok = False
    rs00=s.get(login,headers=headers,verify=False)
    ui00 = rs00.content.decode('utf-8')

    while True and not ok:
        rs0=s.get(yzmurl,headers=headers,verify=False)
        ui0 = rs0.content
        with open('captcha.jpg','wb')as f:
            f.write(ui0)
        try:
            yzm,json = captchaget('captcha.jpg')
            yzm = yzm.replace(' ','')
            print(yzm)
        except:
            pass
        yzmy = input('验证码（参看该程序存放文件夹中图片文件）:')
        #下面填入学号和密码的md5的32位小写哈希值
        datalogin = {'j_username': '学号','j_password': '密码md5值','j_captcha': yzmy}
        rs1=s.post(checkurl, headers=headers, data = datalogin, verify=False)
        ui1 = rs1.content.decode('utf-8')
        if '验证码错误' in ui1:
            print(yzm,'验证码错误')
            continue
        else:
            ok = True
    return s


ok = False
jishu = 1
while 1:
    rs=s.get(url,headers=headers,verify=False)
    ui = rs.text
    if rs.ok:
        t1 = datetime.datetime.now()
        t1 = str(t1)
        if '对不起，当前选课阶段将在' in ui:
            print(str(jishu) + '.-----未开放---- ' + t1)
            jishu += 1
            
        elif '当前为非选课阶段！' in ui:
            print('非选课阶段')
            break
        
        elif '欢迎登录内蒙古大' in ui:
            print('cookie已过期,请重新登录')
            s = loginandcookie(login,yzmurl,s)
            continue
            
        elif '星期' in ui:
            print('教务系统已开放 ' + t1)
            timetr = str(t1)[:-7].replace(':','-')
            if os.path.exists('成功样本库'):
                pass
            else:
                os.mkdir('成功样本库')
                
            with open(path1 + '\成功样本库\\'+ timetr +' .txt','w',encoding = 'utf-8')as f:
                f.write(ui)
            try:
                shun = ui.index('type="hidden" id="tokenValue" value=') + 37
                valuetoken = ui[shun:shun+32]
                print(valuetoken)
                ok = True  #为下一个选课做好准备
            except:
                print('选课接口未开放')
            break
        
        else:
            print('未知错误')
            timetr = str(t1)[:-7].replace(':','-')
            if os.path.exists('失败样本库'):
                pass
            else:
                os.mkdir('失败样本库')
                
            with open(path1 + '\失败样本库\\'+ timetr +' .txt','w',encoding = 'utf-8')as f:
                f.write(ui)
            break



            
#选课区
kcid = []#['130320110','130120210','1912410014','110140060','1912560050']
urlxuan = 'http://jwxt.imu.edu.cn/student/courseSelect/selectCourse/checkInputCodeAndSubmit'

for ids in kcid:
    valuetoken = tokenget(s)
    dataxuan = {'dealType': '5','kcIds': ids +' @01@2021-2022-1-2','fajhh': '35885',
    'sj': '0_0','tokenValue': valuetoken}
    rs2 = s.post(url = urlxuan,headers = headers,data = dataxuan)
    ui2 = rs2.content.decode('utf-8')
    if 'ok' in ui2:
        print('选课成功！')

#课程查询区域
kcdata = {'xq':'0','jc':'0'}
rs3 = s.post(url = kcurl,headers = headers,data = kcdata)
ui3 = rs3.content.decode('utf-8')
dic = eval(ui3)
dic2 = dic['rwRxkZlList']
dic2 = eval(dic2)
for i in dic2:
    if '数字信号处理' in dic2[dic2.index(i)]['kcm']:
        print(dic2[dic2.index(i)]['kch'],dic2[dic2.index(i)]['kcm'])














#120330051


##Request URL: http://jwxt.imu.edu.cn/student/courseSelect/freeCourse/courseList
##Request Method: POST
##Status Code: 200 OK
##Remote Address: 222.31.220.1:80
##Referrer Policy: strict-origin-when-cross-origin
##Accept: */*
##Accept-Encoding: gzip, deflate
##Accept-Language: zh-CN,zh;q=0.9
##Connection: keep-alive
##Content-Length: 45
##Content-Type: application/x-www-form-urlencoded; charset=UTF-8
##Cookie: JSESSIONID=abchWqnSK3qgh8TAlEmTx; selectionBar=1293218
##DNT: 1
##Host: jwxt.imu.edu.cn
##Origin: http://jwxt.imu.edu.cn
##Referer: http://jwxt.imu.edu.cn/student/courseSelect/freeCourse/index?fajhh=35885
##User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36
##X-Requested-With: XMLHttpRequest
##searchtj: 性之
##xq: 0
##jc: 0
##kclbdm: 
##validCaptcha()





##idli = []
##num = '5687575639'
##xurl = 'https://m.weibo.cn/profile/info?uid=' + num
##xrs=s.get(xurl,headers=headers,verify=False)
##xrss = xrs.text
##xrss = dicturn(xrss)
##xrss = xrss.encode('utf-8','ignore').decode('unicode_escape','ignore')
##xrss = xrss.encode('utf-8','ignore').decode('utf-8','ignore')
##xrssli = xrss.split('"')
##for i in range(len(xrssli)):
##    if xrssli[i] == 'screen_name':
##        print(xrssli[i+2])
##        hostname = xrssli[i+2]
##        break
##cf = 0
##fg = 1
##ids = 20
##urlj = 0
##try :
##    
##    for idss in range(20,10000,20):
##        if urlj == 1:
##            url1 = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_' + str(num) + '&since_id=' + str(ids)
##        else:
##            url1 = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_' + str(num)
##            urlj = 1
##        rs=s.get(url1,headers=headers,verify=False)
##        print(url1)
##        qingqiu += 1
##        ui = rs.text
##        ui = dicturn(ui)
##        ui = ui.encode('utf-8','ignore').decode('unicode_escape','ignore')
##        ui = ui.encode('utf-8','ignore').decode('utf-8','ignore')
##        if len(ui) < 100:
##            break
##        else:
##            
##            #break
##            if rs.ok:
##
##                with open(r'E:\2020地大学习\python小项目\微博\个性签名爬取\存放\\' + num + '--' +  str(ids) + ' .txt','w',encoding = 'utf-8')as f:
##                    f.write(ui)
##                uili = ui.split('"')
##
##                try:
##                    for i in range(len(uili)):
##                        if uili[i] == 'since_id':
##                            ids = int(uili[i + 1][1:-1])
##                            break
##                except:
##                    ids += 20
##                    print('id wrong')
##                for i in range(len(uili)):
##                    
##                    if uili[i] == 'id':
##                        idd = uili[i+1][1:-1]
##                        if idd in idli:
##                            cf += 1
##                            fg = 0
##                        else:
##                            fg = 1
##                            idli.append(idd)
##                    if uili[i] == 'screen_name':
##                        xjishu += 1
##                        name = uili[i+2]   
##                    if uili[i] == 'description':
##                        words = uili[i+2]
##                        if words != '' and fg:
##                            ws['A' + str(jishu)] = idd
##                            print(idd,end = '    -->')
##                            ws['B' + str(jishu)] = name
##                            print(name)
##                            ws['C' + str(jishu)] = words
##                            jishu += 1
##                            print('\t' + words)
##                            print('---   ---   ---   ---   ---   ---' + str(jishu) + '   ---   ---   ---   ---   ---   ---')
##                print('重复率：'  + str(cf/20) + ' ' + str(cf))
##                cf = 0
##except Exception as e:
##    wb1.save(hostname + ' sid ' + str(jishu) + '.xlsx')
##    print(e)
##ws['A' + str(jishu + 3)] = '请求 ' + str(qingqiu) + ' 次，收到 ' + str(xjishu) + ' 人，有效 ' + str(jishu) + ' 人，有效率' + str(jishu/xjishu*100) + '%'
##ws['A' + str(jishu + 4)] = hostname + '     ' + num  + '-- 粉丝：' + fans +  + ' -- 关注：' + follow  + ' -- 微博动态 ：' + statues
##wb1.save(hostname + ' sid ' + str(jishu) + '.xlsx')
##print('请求 ' + str(qingqiu) + ' 次')
##print('收到 ' + str(xjishu) + ' 人')
##print('有效 ' + str(jishu) + ' 人，有效率' + str(jishu/xjishu*100) + '%')
##
####
####import json
####with open("test.json", "w", encoding='utf-8') as f:
####	
####    # indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
####    #f.write(json.dumps(dict, indent=4))
####    json.dump(idli, f, indent=4)  # 传入文件描述符，和dumps一样的结果
##

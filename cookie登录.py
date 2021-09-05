#2021年8月16日  8点11分
import os
import time
import random
import datetime
import requests
from fake_useragent import UserAgent

#关闭安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

di = {}
path1 = os.getcwd()
ua = UserAgent()
agent = ua.random
s=requests.session()
cookie = 'abcRepyFaMDyy4IL9KxUx' #--->->->-此处填入cookie--->->->---
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
    'Cookie': cookie
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


login = 'http://jwxt.imu.edu.cn/login'  #登陆页面
yzmurl = 'http://jwxt.imu.edu.cn/img/captcha.jpg?'  #获取验证码
checkurl = 'http://jwxt.imu.edu.cn/j_spring_security_check'   #post请求
kcurl = 'http://jwxt.imu.edu.cn/student/courseSelect/freeCourse/courseList'  #自由选课，可以获得所有课程
url = 'http://jwxt.imu.edu.cn/student/courseSelect/courseSelect/index'  #tokenvalue 获取url

ok = False
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
            print('cookie已过期,请更换')
            timetr = str(t1)[:-7].replace(':','-')
            if os.path.exists('失败样本库'):
                pass
            else:
                os.mkdir('失败样本库')
                
            with open(path1 + '\失败样本库\\'+ timetr +' .txt','w',encoding = 'utf-8')as f:
                f.write(ui)
            break
            
        elif '星期' in ui:
            print('教务系统已开放 ' + t1)
            timetr = str(t1)[:-7].replace(':','-')
            if os.path.exists('成功样本库'):
                pass
            else:
                os.mkdir('成功样本库')
                
            with open(path1 + '\成功样本库\\'+ timetr +' .txt','w',encoding = 'utf-8')as f:
                f.write(ui)
            shun = ui.index('type="hidden" id="tokenValue" value=') + 37
            valuetoken = ui[shun:shun+32]
            print(valuetoken)
            ok = True  #为下一个选课做好准备
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
if ok:
    kcid = ['130320110','130120210','1912410014','110140060','1912560050']
    urlxuan = 'http://jwxt.imu.edu.cn/student/courseSelect/selectCourse/checkInputCodeAndSubmit' #课程提交url  POST

    for ids in kcid:
        valuetoken = tokenget(s)
        dataxuan = {'dealType': '5','kcIds': ids +' @01@2021-2022-1-2','fajhh': '35885',
        'sj': '0_0','tokenValue': valuetoken}  #post 参数，仅仅课程号为变量（其实@之后课程类型应该也是变量）
        rs2 = s.post(url = urlxuan,headers = headers,data = dataxuan)
        ui2 = rs2.content.decode('utf-8')
        if 'ok' in ui2:  #会返回一个哈希值，但是不知道有何用，没有试过是不是可以当作下一次的tokenvalue
            print('选课成功！')

    #获取所有课程名
    kcdata = {'xq':'0','jc':'0'}
    rs3 = s.post(url = kcurl,headers = headers,data = kcdata)
    ui3 = rs3.content.decode('utf-8')
    dic = eval(ui3)
    dic2 = dic['rwRxkZlList']  #此处化为字典，可以索引查询信息
    dic2 = eval(dic2)
    for i in dic2:
        if '数字信号处理' in dic2[dic2.index(i)]['kcm']:
            print(dic2[dic2.index(i)]['kch'],dic2[dic2.index(i)]['kcm'])




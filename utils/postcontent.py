# coding:utf-8
import re
import requests,os,json
from utils.handleexcel import write_excle
from utils.config import contents,savefile
import json


class ProjectContent(object):


    def __init__(self,cityid,jsessionid):
        self.url = "http://59.207.104.9:8062/hd/app/module/default/jsp/view/view.action"
        self.headers ={
                    'Connection': 'keep-alive',
                    'Content-Length': '138',
                    'Host': '59.207.104.4:8060 ' , 
                    'Origin':'http://59.207.104.4:8060',
                    'Upgrade-Insecure-Requests':'1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9', 
                    'Cookie': f'JSESSIONID={jsessionid}',  
                    }
        self.cityid=cityid
        self.cookie_path='./source'
        self.cookie_name = 'cookies_pjxxk.txt'


    def get_pro_total(self):
        cookies = self.get_cookies()
        payload = {
                'fn': 'grid_list',
                'sysMenuId': '8FCE1CFE6FE34A1328D547E398C43DB4',
                'viewId': 'B3E884EFADCE823956080778FA5B937A',
                'sysUnid': '2CAA2C792CF1C85A91A8DE67D1FAFA40',
                'ID': f'{self.cityid}',
                'TYPE': 'dept',
                'SERIALNUMBER':'4108',
                'fn': 'grid_list',
                'page': '-1',
                'rows': '-1',
                }
        requests.packages.urllib3.disable_warnings()
        resp = requests.post(self.url, cookies=cookies,data=payload, headers=self.headers,verify=False)
        pro_contents=resp.json()
        if 'total' in pro_contents.keys():
            pro_total=pro_contents['total']
            return pro_total

    
    def get_pro_list(self):
        pro_total = self.get_pro_total()
        num = pro_total//50
        for i in range(num+1):
            payload = {
                'fn': 'grid_list',
                'sysMenuId': '8FCE1CFE6FE34A1328D547E398C43DB4',
                'viewId': 'B3E884EFADCE823956080778FA5B937A',
                'sysUnid': '2CAA2C792CF1C85A91A8DE67D1FAFA40',
                'ID': f'{self.cityid}',
                'TYPE': 'dept',
                'SERIALNUMBER':'4108',
                'fn': 'grid_list',
                'page': f'{i}',
                'rows': '50',
                }
            requests.packages.urllib3.disable_warnings()
            resp = requests.post(self.url,data=payload, headers=self.headers,verify=False)
            pro_contents=resp.json()            
            if 'rows' in pro_contents.keys():
                pro_lists=pro_contents['rows']
                if len(pro_lists) > 0:
                    for pro_list in pro_lists:
                        projid=pro_list["PROJID"]
                        servicecode=pro_list["SERVICECODE"]
                        transact_name=pro_list["SERVICENAME"]
                        card_num=pro_list["APPLYCARDNUM"]
                        tel_num=pro_list["TELPHONE"]
                        applicant=pro_list["CONTACTMAN"]
                        dept_name=pro_list["DEPTID"]
                        time=pro_list["TRANSACTTIME"]
                        result=pro_list["HANDLESTATE"]
                        content={
                            "申报号":projid,
                            '办理单位':dept_name,
                            "事项编码":servicecode,
                            "办件名称":transact_name,
                            "证件号码":str(card_num),
                            "手机号码":str(tel_num),
                            "申请人":applicant,
                            "办结时间":time,
                            "办件状态":result
                        }
                        print(content)
                        contents.append(content)
        write_excle(contents,savefile)


    def get_cookies(self):
            with open(os.path.join(self.cookie_path, self.cookie_name),'r') as cookief:
                #使用json读取cookies 注意读取的是文件 所以用load而不是loads
                cookieslist = json.load(cookief)
                # 方法1删除该字段
                cookies_dict = dict()
                for cookie in cookieslist:
                    #该字段有问题所以删除就可以,浏览器打开后记得刷新页面 有的网页注入cookie后仍需要刷新一下
                    if 'expiry' in cookie:
                        del cookie['expiry']
                    cookies_dict[cookie['name']] = cookie['value']
            print(cookies_dict)
            return cookies_dict



class TelCommitContent(object):
    

    def __init__(self,tel,projid,projname,offerorname,offerortelphone,jsessionid):
        self.url = "http://59.207.104.9:8062/hd//essm/jsp/comment/appointment_savecomment.action"
        self.cookie_path='./source'
        self.cookie_name = 'cookies_pjxxk.txt'
        self.headers ={
                    'Connection': 'keep-alive',
                    'Content-Length': '404',
                    'Host': '59.207.104.9:8062' , 
                    'Origin':'http://59.207.104.9:8062',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 
                    'Cookie': f'JSESSIONID={jsessionid}',  
                    }
        self.tel=tel
        self.projid=projid
        self.projname = projname
        self.offerorname=offerorname
        self.offerortelphone=offerortelphone


    def get_cookies(self):
        with open(os.path.join(self.cookie_path, self.cookie_name),'r') as cookief:
            #使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookieslist = json.load(cookief)
            # 方法1删除该字段
            cookies_dict = dict()
            for cookie in cookieslist:
                #该字段有问题所以删除就可以,浏览器打开后记得刷新页面 有的网页注入cookie后仍需要刷新一下
                if 'expiry' in cookie:
                    del cookie['expiry']
                cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict

   
    def commit_projectlist(self):
        cookies = self.get_cookies()
        payload = {
                'fn': 'save',
                'projid': f'{self.projid}',
                'isAnonymity': '2',
                'evaluteCount': '1',
                'isOpened': '1',
                'checkState': '2',
                'evaluateContent': '',
                'satisfactionEvaluate': '5',
                'evaluateDetail': '',
                'syncStatus': 'I',
                'isAboveLegalday': '2',
                'isOvercharge': '2',
                'isMediation': '2',
                'serviceAttitudeEvaluate': '1',
                'serviceAttitudeReason': '',
                'workAttitudeEvaluate': '1',
                'workAttitudeReason': '',
                'evaluatorPhone': f"{self.tel}",
                'offerorName': f'{self.offerorname}',
                'offerorTelphone': f'{self.offerortelphone}',
                'extend_2': '1',
                'viewId':'B3E884EFADCE823956080778FA5B937A',
                }
        url = 'http://59.207.104.9:8062/hd//essm/jsp/comment/appointment.jsp?projid={}&projname={}&viewId=B3E884EFADCE823956080778FA5B937A&phone={}'.format(self.projid,self.projname,self.tel)
        requests.packages.urllib3.disable_warnings()
        resp = requests.post(self.url,cookies=cookies, data=payload, headers=self.headers,verify=False)
        try:
            msg = json.loads(resp.text)
        except:
            msg = {'msg':'评价失败'}
        print(msg)
        return msg




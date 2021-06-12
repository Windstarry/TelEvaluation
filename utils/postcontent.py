# coding:utf-8
import requests
from utils.handleexcel import write_excle
from utils.config import contents,savefile



class ProjectContent(object):
    
    
    def __init__(self,pagenum,cityid,cityname,jsessionid):
        self.url = "http://59.207.104.4:8060/rsp/view.action"
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
        self.pagenum=pagenum
        self.cityid=cityid
        self.cityname=cityname
    

    def get_projectlist(self):
        payload = {
                '_search':'0',
                'ID': f'{self.cityid}',
                'TREENODE_NAME':f'{self.cityname}',
                'viewId': 'A97604BB8E12B56595743D8BAF0651CC',
                'fn': 'grid_list',
                'page': f'{self.pagenum}',
                'rows': '50',
                }
        requests.packages.urllib3.disable_warnings()
        resp = requests.post(self.url, data=payload, headers=self.headers,verify=False)
        pro_contents=resp.json()
        if 'rows' in pro_contents.keys():
            pro_lists=pro_contents['rows']
            if len(pro_lists) > 0:
                for pro_list in pro_lists:
                    projid=pro_list["PROJID"]
                    servicecode=pro_list["SERVICECODE"]
                    transact_name=pro_list["PROJECTNAME"]
                    card_num=pro_list["APPLY_CARDNUMBER"]
                    tel_num=pro_list["TELPHONE"]
                    applicant=pro_list["APPLYNAME"]
                    dept_name=pro_list["DEPTNAME"]
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


class CommitContent(object):
    
    def __init__(self,tel,projid,servicecode,evaluatorname,projectname,cardnumber,projectno):
        self.url = "http://was.hnzwfw.gov.cn/ycslypt_web/pingjia.action"
        self.headers ={
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9', 
                    'Connection': 'keep-alive',
                    'Content-Length': '2123',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'was.hnzwfw.gov.cn' , 
                    'Origin':'http://was.hnzwfw.gov.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Cookie': 'JSESSIONID=ADFD2374489F509651FDF81ABCD16B3C; app_cook=webapp_1', 
                    }
        self.tel=tel
        self.projid=projid
        self.servicecode=servicecode
        self.evaluatorname=evaluatorname
        self.projectname=projectname
        self.cardnumber=cardnumber
        self.projectno=projectno
    
    
    def get_projectlist(self):
        payload = {
                'fn': 'save',
                'projid': f'{self.projid}',
                'serviceCode': f'{self.servicecode}',
                'evaluatefrom': '4',
                'userType': '',
                'evaluatorName': f'{self.evaluatorname}',
                'isAnonymity': '2',
                'evaluteCount': '1',
                'projectname': f'{self.projectname}',
                'isOpened': '1',
                'checkState': '1',
                'evaluateContent': '',
                'satisfactionEvaluate': '5',
                'evaluateDetail': '510,517',
                'syncStatus': 'I',
                'isAboveLegalday': '2',
                'isOvercharge': '2',
                'isMediation': '2',
                'serviceAttitudeEvaluate': '1',
                'serviceAttitudeReason': '',
                'workAttitudeEvaluate': '1',
                'workAttitudeReason': '',
                'evaluatorCardnumber': f'{self.cardnumber}',
                'belongsystem': '',
                'evaluatecount': '1',
                'evaluatorPhone': f'{self.tel}',
                'token': '7bc414579c16f38e324553a89f95cbf6',
                'evaluateDetailArray[]': '510',
                'evaluateDetailArray[]': '517',
                'huaKuaiFlag': 'true',
                'checkFlag': 'notRobot',
                'projectNo': f'{self.projectno}',
                'proStatus': '3',
                }
        requests.packages.urllib3.disable_warnings()
        resp = requests.post(self.url, data=payload, headers=self.headers,verify=False,timeout=200)
        print(resp.json())
        return resp.json()
    
    def second_evaluate(self):
        payload = {
                'fn': 'save',
                'projid': f'{self.projid}',
                'serviceCode': f'{self.servicecode}',
                'evaluatefrom': '4',
                'userType': '',
                'evaluatorName': f'{self.evaluatorname}',
                'isAnonymity': '2',
                'evaluteCount': '2',
                'projectname': f'{self.projectname}',
                'isOpened': '1',
                'checkState': '1',
                'evaluateContent': '',
                'satisfactionEvaluate': '5',
                'evaluateDetail': '510,517',
                'syncStatus': 'I',
                'isAboveLegalday': '2',
                'isOvercharge': '2',
                'isMediation': '2',
                'serviceAttitudeEvaluate': '1',
                'serviceAttitudeReason': '',
                'workAttitudeEvaluate': '1',
                'workAttitudeReason': '',
                'evaluatorCardnumber': f'{self.cardnumber}',
                'belongsystem': '',
                'evaluatecount': '2',
                'evaluatorPhone': f'{self.tel}',
                'token': '7bc414579c16f38e324553a89f95cbf6',
                'evaluateDetailArray[]': '510',
                'evaluateDetailArray[]': '517',
                'huaKuaiFlag': 'true',
                'checkFlag': 'notRobot',
                'projectNo': f'{self.projectno}',
                'proStatus': '2',
                }
        requests.packages.urllib3.disable_warnings()
        resp = requests.post(self.url, data=payload, headers=self.headers,verify=False,timeout=200)
        print(resp.json())
        return resp.json()

    def third_evaluate(self):
        payload = {
                'fn': 'save',
                'projid': f'{self.projid}',
                'serviceCode': f'{self.servicecode}',
                'evaluatefrom': '4',
                'userType': '',
                'evaluatorName': f'{self.evaluatorname}',
                'isAnonymity': '2',
                'evaluteCount': '3',
                'projectname': f'{self.projectname}',
                'isOpened': '1',
                'checkState': '1',
                'evaluateContent': '',
                'satisfactionEvaluate': '5',
                'evaluateDetail': '510,517',
                'syncStatus': 'I',
                'isAboveLegalday': '2',
                'isOvercharge': '2',
                'isMediation': '2',
                'serviceAttitudeEvaluate': '1',
                'serviceAttitudeReason': '',
                'workAttitudeEvaluate': '1',
                'workAttitudeReason': '',
                'evaluatorCardnumber': f'{self.cardnumber}',
                'belongsystem': '',
                'evaluatecount': '3',
                'evaluatorPhone': f'{self.tel}',
                'token': '7bc414579c16f38e324553a89f95cbf6',
                'evaluateDetailArray[]': '510',
                'evaluateDetailArray[]': '517',
                'huaKuaiFlag': 'true',
                'checkFlag': 'notRobot',
                'projectNo': f'{self.projectno}',
                'proStatus': '1',
                }
        requests.packages.urllib3.disable_warnings()
        resp = requests.post(self.url, data=payload, headers=self.headers,verify=False,timeout=200)
        print(resp.json())
        return resp.json()


class TelCommitContent(object):
    

    def __init__(self,tel,projid,offerorname,offerortelphone,jsessionid):
        self.url = "http://59.207.104.9:8062/hd//essm/jsp/comment/appointment_savecomment.action"
        self.headers ={
                    'Connection': 'keep-alive',
                    'Content-Length': '405',
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
        self.offerorname=offerorname
        self.offerortelphone=offerortelphone

    
    def commit_projectlist(self):
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
                }
        requests.packages.urllib3.disable_warnings()
        resp = requests.post(self.url, data=payload, headers=self.headers,verify=False)
        print(resp.json())
        return resp.json()




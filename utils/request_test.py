import requests

url = "http://was.hnzwfw.gov.cn/ycslypt_web/pingjia.action?fn=save&projid=410821020210525A000002&serviceCode=005677264XK46177001&evaluatefrom=4&userType&evaluatorName=修武中裕燃气发展有限公司焦庄加气站&evaluteCount=1&projectname=关于修武中裕燃气发展有限公司焦庄加气站申请城镇燃气经营许可&isOpened=1&checkState=1&evaluateContent&satisfactionEvaluate=5&syncStatus=I&isAboveLegalday=2&isMediation=2&serviceAttitudeEvaluate=1&isAnonymity=2&serviceAttitudeReason&workAttitudeEvaluate=1&workAttitudeReason=&evaluatorCardnumber=91410821MA44W25695&belongsystem&evaluatecount=1&evaluatorPhone=13619856612&token=cdeb4ce0a0ea48b86c7be8fba9a412ca&huaKuaiFlag=true&checkFlag=notRobot&projectNo=11410821005677264N4000117018000202105250002&proStatus=3&evaluateDetail "

payload={}
files={}
headers = {
  'Cookie': 'JSESSIONID=FFB9A8CAA0E1005C7B202D8944A88251; app_cook=webapp_3'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
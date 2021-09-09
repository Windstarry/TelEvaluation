# coding:utf-8
from utils.handleexcel import HandleExcle,write_excle
from utils.postcontent import ProjectContent,TelCommitContent
from utils.test_login import Tel_loggin
from utils.config import login_url,home_url,contents,savefile,offerorname,offerortelphone
import time

def main():
    #运行程序
    test_loggin = Tel_loggin(login_url=login_url,home_url=home_url)
    jsessionid=test_loggin.get_jsessionid()
    try:
        ProjectContent(cityid,jsessionid).get_pro_list()
        write_excle(contents,savefile)
        print("{}保存完毕".format(savefile))
    except:
        print('没有找到新的办件')


def tel_evaluation():
    #修改电话邀评账号
    tel_loggin = Tel_loggin(login_url=login_url,home_url=home_url)
    jsessionid=tel_loggin.get_jsessionid()
    he=HandleExcle(savefile)
    if "评价状态" not in he.column_list:
        he.insert_column()
    for i in range(0,he.max_num): 
        result=he.get_result(i)
        tel=he.get_tel(i)
        projid=he.get_projid(i)
        projname = he.get_projname(i)
        if result=="已评价":
            print(f"第{i}件事项已评价")
        else:
            msg=TelCommitContent(tel,projid,projname,offerorname,offerortelphone,jsessionid).commit_projectlist()
            time.sleep(2)
            if msg['msg'] =='保存成功' or msg['msg'] =='重复评价':
                he.resultstate(i)
    he.save_excle(savefile)




if __name__ == "__main__":
    cityid='001003018006016'
    cityname='修武县'
    main()
    tel_evaluation()



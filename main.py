# coding:utf-8
from utils.handleexcel import HandleExcle,ExcleRemoveDupl,ExcelConcat,write_excle
from utils.postcontent import ProjectContent,CommitContent,TelCommitContent
from utils.test_login import Test_loggin,Tel_loggin,LoginPage,AddPage
from utils.config import login_url,home_url,contents,savefile,filecontents,setindex_col,offerorname,offerortelphone
from playwright.sync_api import sync_playwright
from playwright.sync_api import BrowserContext

def main():
    #运行程序
    test_loggin = Test_loggin(login_url=login_url)
    jsessionid=test_loggin.get_jsessionid()
    for i in range(pagestart,pageend):
        procontens=ProjectContent(i,cityid,cityname,jsessionid).get_projectlist()
    write_excle(contents,savefile)
    print("{}保存完毕".format(savefile))
    #去除申报号在已评价事项里办件信息
    erd=ExcleRemoveDupl(savefile,filecontents,savefile,setindex_col)
    erd.excle_removedupl()


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
        print(projid)
        if result=="已评价":
            print(f"第{i}件事项已评价")
        else:
            commitcontens=TelCommitContent(tel,projid,offerorname,offerortelphone,jsessionid).commit_projectlist()
            msg=commitcontens['msg']
            print(msg)
            if msg =='保存成功' or msg =='重复评价':
                he.resultstate(i)
            if i%500==0:
                he.save_excle(savefile)
    he.save_excle(savefile)
    #将已评价完的数据同步到汇总表中
    ec=ExcelConcat(savefile,filecontents,filecontents,setindex_col)
    ec.excle_concat()


def second_evaluation():
    playwright = sync_playwright().start()
    #以无头模式运行
    browser = playwright.chromium.launch()
    #browser = playwright.chromium.launch(headless=False,slow_mo=200)
    context = browser.new_context()
    lp=LoginPage(context)
    lp.to_login()
    ap=AddPage(context) 
    he=HandleExcle(savefile)
    if "评价状态" not in he.column_list:
        he.insert_column()
    for i in range(0,he.max_num): 
        tel = he.get_tel(i)
        url = he.get_url(i)
        #print("*"*50)
        #ap.add_content(url[0],tel)
        ap.add_content(url[1],tel)
        ap.add_content(url[2],tel)
    context.close()
    browser.close()


if __name__ == '__main__':
    cityid='001003018006016'
    cityname='修武县'
    # cityid='001003018006016003017'
    # cityname='县税务局'
    # cityid='001003018006016003018'
    # cityname='修武县人力资源和社会保障局'
    #设置读取页面起始结束页
    # cityid="001003018006016003009"
    # cityname="修武县市场监督管理局"
    pagestart=1
    pageend=2
    # #运行程序
    main()
    # 进行第一次评价
    tel_evaluation()
    #进行第二次评价
    second_evaluation()


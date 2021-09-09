# coding:utf-8
import pandas as pd
import re

class HandleExcle(object):
    
    def __init__(self,filename):
        self.filename = filename
        self.df=pd.read_excel(filename,dtype=str)
        self.max_num=self.df.shape[0]
        self.column_list=list(self.df.columns)

    
    def get_tel(self,x):
        tel=self.df["手机号码"].at[x]
        if pd.isnull(tel):
            tel = '0391-7118602'
        else:   
            tel = self.tel_num_judge(tel)
        return tel


    def get_projname(self,x):
        url=self.df["办件名称"].at[x]
        return url 
    
    
    def get_name(self,x):
        name=self.df["申请人"].at[x]
        return name

    
    def get_idcard(self,x):
        idcard=self.df["证件号码"].at[x]
        return idcard


    def get_projid(self,x):
        projid=self.df['申报号'].at[x]
        return projid


    def get_servicename(self,x):
        servicename=self.df['办件名称'].at[x]
        print(servicename)
        return servicename
   

    def get_result(self,x):
        result=self.df["评价状态"].at[x]
        return result
    

    def resultstate(self,x):
        self.df.loc[x,"评价状态"]="已评价"
    
    
    def save_excle(self,savefile):
        df=self.df.set_index("申报号")
        df.to_excel(savefile)

    
    def insert_column(self):
        self.df.insert(1,"评价状态",'未评价')

    
    
    @staticmethod
    def tel_num_judge(tel_num):
        ret = '\d{3}\*{7}\d{1}'
        tel_judge = re.match(ret,tel_num)
        tel_judge_two = re.match('\*{7}',tel_num)
        if tel_judge:
            tel_num = "0391-7873031"
        elif tel_judge_two:
            tel_num = "0391-7873031"
        elif tel_num == '空':
            tel_num = "0391-7118602"
        else:
            tel_num = tel_num
        return tel_num


def write_excle(content,savefile):
    df=pd.DataFrame.from_dict(content)
    df.set_index(df.columns[0],inplace=True)
    df.to_excel(savefile)


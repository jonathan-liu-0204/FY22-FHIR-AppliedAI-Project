import re
import json

with open('result.json') as f:
    data = json.load(f)
seg = []
for i in data['analyzeResult']['readResults'][0]['lines']:
    seg.append(i['text'])


str_seg = ' '.join(seg)

name = str_seg[re.search(r'姓名',str_seg).span()[1]+1:re.search(r'身分證號碼',str_seg).span()[0]-1]
SocialID = str_seg[re.search(r'身分證號碼',str_seg).span()[1]+1:re.search(r'出生',str_seg).span()[0]-1]
Birth = str_seg[re.search(r'日期',str_seg).span()[1]+1:re.search(r'被保險人 性別',str_seg).span()[0]-3]
Gender = str_seg[re.search(r'性別',str_seg).span()[1]+1:re.search(r'婚姻',str_seg).span()[0]-1]
Marriage = str_seg[re.search(r'婚姻',str_seg).span()[1]+1:re.search(r'年齡',str_seg).span()[0]-1]
YearsOld = str_seg[re.search(r'年齡',str_seg).span()[1]+1:re.search(r'公司名稱',str_seg).span()[0]-1]
Company = str_seg[re.search(r'公司名稱',str_seg).span()[1]+1:re.search(r'工作內容',str_seg).span()[0]-1]
Work = str_seg[re.search(r'工作內容',str_seg).span()[1]+1:re.search(r'職稱',str_seg).span()[0]-1]
Position = str_seg[re.search(r'職稱',str_seg).span()[1]+1:re.search(r'副業',str_seg).span()[0]-1]
OtherWork = str_seg[re.search(r'副業',str_seg).span()[1]+1:re.search(r'職業代碼',str_seg).span()[0]-1]
WorkCode = str_seg[re.search(r'職業代碼',str_seg).span()[1]+1:re.search(r'國籍',str_seg).span()[0]-1]
Nationality = str_seg[re.search(r'國籍',str_seg).span()[1]+1:re.search(r'外國',str_seg).span()[0]+2]
Address = str_seg[re.search(r'外國',str_seg).span()[1]+1:re.search(r'※數字0請以の書寫',str_seg).span()[0]-1]
Email = str_seg[re.search(r'E-MAIL',str_seg).span()[1]+1:re.search(r'電話 住',str_seg).span()[0]-1]
HomeNum = str_seg[re.search(r'住宅',str_seg).span()[1]+1:re.search(r' 公司:',str_seg).span()[0]]
CompanyNum = str_seg[re.search(r' 公司:',str_seg).span()[1]:re.search(r' 手機:',str_seg).span()[0]]
TelNum = str_seg[re.search(r'手機:',str_seg).span()[1]:re.search(r'可免填要保人相',str_seg).span()[0]-10]
SameData = str_seg[re.search(r'可免填要保人相',str_seg).span()[1]-18:re.search(r'可免填要保人相',str_seg).span()[0]+11]
HelpEmail = str_seg[re.search(r'人相關欄位',str_seg).span()[1]+9:re.search(r'電子保單',str_seg).span()[0]]
Paper = str_seg[re.search(r'電子保單',str_seg).span()[1]:re.search(r'保單 要',str_seg).span()[0]+2]
SecondName = str_seg[re.search(r' 要 姓名 ',str_seg).span()[1]:re.search(r'/統一編號',str_seg).span()[0]]
SecondSocialID = str_seg[re.search(r'/統一編號',str_seg).span()[1]:re.search(r' /統一編號 ',str_seg).span()[0]+17]
SecondBirth = str_seg[re.search(r' 代表人姓名 ',str_seg).span()[1]-14:re.search(r' 代表人姓名 ',str_seg).span()[0]+1]
RepresentName = str_seg[re.search(r' 代表人姓名 ',str_seg).span()[1]:re.search(r' 代表人姓名 ',str_seg).span()[0]+10]
RepresentSocialID = str_seg[re.search(r'日 保 身分證號碼',str_seg).span()[1]:re.search(r'日 保 身分證號碼',str_seg).span()[0]+20]
SecondAddress = str_seg[re.search(r'日 保 身分證號碼',str_seg).span()[1]+12:re.search(r'人 地址 關係',str_seg).span()[0]]
Relationship =  str_seg[re.search(r'人 地址 關係',str_seg).span()[1]:re.search(r'人 地址 關係',str_seg).span()[0]+10]
SecondHomeNum =  str_seg[re.search(r'人 地址 關係',str_seg).span()[1]+10:re.search(r'人 地址 關係',str_seg).span()[0]+25]
SecondCompanyNum = str_seg[re.search(r'人 地址 關係',str_seg).span()[1]+22:re.search(r'人 地址 關係',str_seg).span()[0]+45]
SecondTelNum = str_seg[re.search(r'人 地址 關係',str_seg).span()[1]+41:re.search(r'人 地址 關係',str_seg).span()[0]+58]
PayPerson = str_seg[re.search(r' 付款人 ',str_seg).span()[1]:re.search(r'保險期間 自',str_seg).span()[0]-3]
StartFrom = str_seg[re.search(r'保險期間 自',str_seg).span()[1]:re.search(r'零時起',str_seg).span()[0]]
ThisPay = str_seg[re.search(r' 本 期: ',str_seg).span()[1]:re.search(r' 續 期:',str_seg).span()[0]]
NextPay = str_seg[re.search(r' 續 期:',str_seg).span()[1]:re.search(r'未勾選視同本期繳費方式',str_seg).span()[0]-1]
Continue = str_seg[re.search(r'效力。 自動續約附加條款',str_seg).span()[1]:re.search(r'防疫保障主',str_seg).span()[0]]
TotalMoney = str_seg[re.search(r'合計總保險費',str_seg).span()[1]+5:re.search(r'合計總保險費',str_seg).span()[0]+18]


# name 被保人姓名
# SocialID 被保人身分證號碼
# Birth 被保人出生日期
# Gender 被保人性別
# Marriage 被保人婚姻狀況
# YearsOld 被保人年齡
# Company 被保人公司名稱
# Work 被保人工作內容
# Position 被保人職稱
# OtherWork 被保人副業
# WorkCode 被保人工作代碼
# Nationality 被保人國籍
# Address 被保人住所地址
# Email 被保人 Email
# HomeNum 被保人住宅電話
# CompanyNum 被保人公司電話
# TelNum 被保人手機號碼
# SameData 要保人同被保人
# HelpEmail 要保人 Email
# Paper 電子保單
# SecondName 要保人姓名
# SecondSocialID 要保人身分證字號
# SecondBirth 要保人生日
# #RepresentName 代表人姓名
# RepresentSocialID 代表人身分證字號
# SecondAddress 要保人地址
# Relationship 要保人與被保人關係
# SecondHomeNum 要保人住宅電話
# SecondCompanyNum 要保人公司電話
# SecondTelNum 要保人手機
# #PayPerson 付款人
# #StartFrom 保險期間
# ThisPay 本期付款方式
# NextPay 續期付款方式
# Continue 自動續約
# TotalMoney 保險總金額
from selenium import webdriver
from time import sleep
import json
import os

def get_online_name(groupnum):
  #1.创建Chrome浏览器对象
  path = 'F:/anaconda3/chromedriver.exe'
  option = webdriver.ChromeOptions()
  option.add_argument("headless")
  browser = webdriver.Chrome()

  info = {}
  __current_path = os.path.dirname(__file__)
  with open(__current_path + '/config.json', 'r', encoding='utf-8') as fp:
    info = json.load(fp)

  #2.通过浏览器向服务器发送URL请求
  browser.get("https://qun.qq.com/member.html#gid="+ str(groupnum))
  sleep(20)

  all_number_name = browser.find_elements_by_xpath('//*[@class="list"]/tr/td[4]/span[1]')
  all_number_qq = browser.find_elements_by_xpath('//*[@class="list"]/tr/td[5]')

  li=[]
  for k in range(len(all_number_qq)):
    li.append([])
    li[k].append(all_number_qq[k].text)
    li[k].append(all_number_name[k].text)
  print(li)
'''
  config_info = dict(zip(["id","name"],li))
  print(config_info)
  current_path = os.path.dirname(__file__)
  with open(current_path + '/online_info.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(config_info))
'''
get_online_name(926594031)


# -*- coding: utf-8 -*-

import sys 	
from PyQt5.QtWidgets import QApplication , QMainWindow
from WeatherWin import Ui_Form
import requests, pandas, sys, urllib, time, datetime
import pandas as pd
from pandas.core.frame import DataFrame


class MainWindow(QMainWindow ):
	def __init__(self, parent=None):    
		super(MainWindow, self).__init__(parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)

	def queryWeather(self):
		print('* queryWeather  ')
		cityName = self.ui.weatherComboBox.currentText()
		cityCode = self.transCityName(cityName)

		# 统计时间
		NowDate = datetime.datetime.now().strftime("%m-%d")
		NextDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m-%d")
		NowTime = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))

		# 读取企业微信会商
		url = "http://qywx1.soweather.com:8383/conference.php?userid=XiaJingJie&username=%E5%A4%8F%E9%9D%96%E6%9D%B0&department=2&departmentname=%E4%BF%A1%E6%81%AF%E4%B8%AD%E5%BF%83&avatar=https://wework.qpic.cn/bizmail/vZIdhGNNP2dCXbKj330s2ZibyRt62Vhnw8nJrIeZrnkndt1VKrm0tNw/0&avatar_thumbnail=https://wework.qpic.cn/bizmail/vZIdhGNNP2dCXbKj330s2ZibyRt62Vhnw8nJrIeZrnkndt1VKrm0tNw/100&qr_code=https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=vc5f77fdb03169d3d5&verification_code=llkjxxjb5sa3k9prin0b8mtdmaopuo3ho6u7"
		try:
			ConWe = pandas.read_html(url)[0]
			table = DataFrame({
				"日期": ConWe.values[1:, 0],
				"时间": ConWe.values[1:, 1],
				"内容": ConWe.values[1:, 2]
			}).sort_index(axis=0, ascending=True)
		except:
			print("企业微信源失联了，请联系开发者")

		# 查询今明两天数据
		result = pd.concat([table.loc[table["日期"] == NowDate], table.loc[table["日期"] == NextDate]])  # .to_csv("ss.csv")
		print("\n")
		print(result)
		self.ui.resultText.setText(result)
		
	def transCityName(self ,cityName):
		cityCode = ''
		if cityName == '北京' :
			cityCode = '101010100'
		elif cityName == '天津' :
			cityCode = '101030100'
		elif cityName == '上海' :
			cityCode = '101020100'
			
		return cityCode
				
	def clearResult(self):
		print('* clearResult  ')
		self.ui.resultText.clear()	
		
if __name__=="__main__":  
	app = QApplication(sys.argv)  
	win = MainWindow()  
	win.show()  
	sys.exit(app.exec_())  

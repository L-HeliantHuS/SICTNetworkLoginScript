#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "HeliantHuS"
__version__ = "1.1"
import re
import time
import random
import requests
from urllib import parse


postUrl = "http://10.253.1.2/eportal/userV2.do?"

paramsData = {
		'method': 'login', 
		'param': 'true', 
		'wlanuserip': '',
		'wlanacname': '',
		'ssid': '', 
		'nasip': '',
		'snmpagentip': '',
		'mac': '',
		't': '',
		'url': '',
		'apmac': '', 
		'nasid': '', 
		'vid': '', 
		'port': '', 
		'nasportid': ''
	}

postData = {
	i.split("=")[0]:i.split("=")[1] for i in "is_auto_land=false&usernameHidden=&username_tip=Username&username=&strTypeAu=&uuidQrCode=&authorMode=&pwd_tip=Password&pwd=".split("&")
}

def sendGetRequest(url):
	return requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"})

def sendPostRequest(url, data):
	return requests.post(url, data=data, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"}, allow_redirects=False)

def getPostUrl():
	response = sendGetRequest("http://baidu.com")
	toLoginUrl = re.findall("<script>top.self.location.href='(.*?)'</script>", response.text)[0]
	params = parse.parse_qs(toLoginUrl.split("?")[1])
	for p in params:
		paramsData[p] = params[p][0]

	# parse post url params!
	urlParms = parse.urlencode(paramsData)
	return postUrl+urlParms


def randomUserAndPasswd():
	with open("userAndpassword.txt", "r") as fp:
		data = fp.readlines()
		luckText = random.sample(data, 1)[0].strip().split(" ")
		return {"username": luckText[0], "pwd": luckText[1]}
		

def testNetwork():
	try:
		response = sendGetRequest("https://baidu.com")
		return True
	except:
		return False

def login():
	netFlag = testNetwork()
	# if not network
	if not netFlag:
		postUrl = getPostUrl()

		# parse post data (username and password)
		userAndPwd = randomUserAndPasswd()
		for i in userAndPwd:
			postData[i] = userAndPwd[i]
		
		response = sendPostRequest(postUrl, postData)

		# get logout url
		location = response.headers['Location']
		req_success = len(sendGetRequest(location).text)
		if req_success > 1000:
			data = parse.parse_qs(location.split("?")[1])
			userIndex = data["userIndex"]
			logoutUrl = "http://10.253.1.2/eportal/userV2.do?method=logout&userIndex= "+ userIndex[0]
			with open("logout.txt", "w") as fp:
				fp.write(logoutUrl)

		# test network
		if testNetwork():
			print(f"[+] Network Connected!  user:{userAndPwd['username']} pwd:{userAndPwd['pwd']}")
			with open("currentUser.txt", "w") as fp:
				fp.write(f"user:{userAndPwd['username']} pwd:{userAndPwd['pwd']}")

		else:
			print("[-] No!!!!, Can't Connect Network..， please try again!")
	else:
		print("[+] You Connectd the network, not connect again!")

def logout():
	with open("logout.txt", "r") as fp:
		data = fp.read().strip()
		sendGetRequest(data)
		print("[+] Logout success!")

if __name__ == '__main__':
	print("""
		1. ToLogin  :)
		2. ToLogout :(
		""")

	uinput = input(">>>")

	if uinput == "1":
		login()
	elif uinput == "2":
		logout()
	else:
		print("[-] please input 1 or 2, understand?")

	print("[*] 5s auto exit...")
	time.sleep(5)
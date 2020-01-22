from django.shortcuts import render, render_to_response
from django.db import models
import json, time, re
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from AIEP.settings import BASE_DIR
import os
import subprocess

def welcome(request):
	return render_to_response('welcome.html')

def page_not_found(request, exception):
	return render_to_response('404.html')

def submit(request):
	return render_to_response('submit.html')

def waiting(request):
	return render_to_response('waiting.html')

def submit_check(request):
	if request.method == 'GET':
		return render(request, 'index.html')
	elif request.method == 'POST':
		print("后端收到如下信息：", request.POST)
		now = int(time.time())
		time_array = time.localtime(now)
		time_part = time.strftime("%Y_%m_%d-%H%M%S", time_array)
		upload_file = request.FILES.get('submit_model')
		os.mkdir(BASE_DIR + "/static/upload/" + time_part)
		if upload_file != None:
			filename = time_part + '.' + upload_file.name.split('.')[-1]
			filepath = os.path.join(BASE_DIR + "/static/upload/uploadfile/", filename)
			f = open(filepath, 'wb')
			for i in upload_file.chunks():
				f.write(i)
			f.close()
		# print(request.POST.get("submit_proname"))
		# print(request.POST.get("jingxiang"))
		# print(request.POST.get("gpu_type"))
		# print(request.POST.get("describe"))
		# print(request.POST.get("retryCount"))
		# print(request.POST.get("evaluate"))
		# receive_data = json.loads(request.body.decode())
		# print("I receive: ", receive_data)
		# try:
		# 	pro_name = receive_data["name"]
		# 	pro_jingxiang = receive_data["jingxiang"]
		# 	pro_gpu_type = receive_data["gpu_type"]
		# 	pro_describe = receive_data["describe"]
		# 	pro_retry = receive_data["retryCount"]
		# 	pro_evalu = receive_data["evaluate"]
		# 	# pro_model = receive_data["model"]
		# 	print("name: ", pro_name)
		# 	print("jingxiang: ", pro_jingxiang)
		# 	print("gpu_type: ", pro_gpu_type)
		# 	print("describe: ", pro_describe)
		# 	print("retry: ", pro_retry)
		# 	print("evalu: ", pro_evalu)
		# 	# print("model: ", pro_model)
		# output = subprocess.getoutput("python D:/LABOR/temp/testimport.py --defense_model zhaoze_model")
		output = subprocess.getoutput("python /home/aiep/soft/aiepalg_code/SUIBUAA_Sample/test/testimport.py --save_path " + time_part)
		print(output)
		# except Exception as e:
		# 	print(e)
	return render(request, 'waiting.html')


def showline(request):
	currency = {"labels": ["clean", "adver", "corru", "something", "else"],
	 "datasets": [89.8, 27.6, 57.6, 45.8, 99.8]}
	judge_edge_dis = {"label": ["checkpoint1", "checkpoint2", "checkpoint3", "checkpoint4"], 
			"data":{"2a":[[10.1, 12.5, 20.3, 28.9]], "2b":[[5.3, 7.9, 12.8, 21.4]]}}
	pic = {"DIR": "/static/img/2020_01_08/",
			"name":["1.png", "2.png", "3.png", "4.png"]}
	dic = {"currency": currency,
		"judge_edge_dis": judge_edge_dis,
		"pic" : pic}
	return render(request, 'show_result.html', {
			'data': json.dumps(dic),
		})


def isImage(filename):
	filename = filename.lower()
	if "png" in filename or "jpg" in filename:
		return True
	if "jpeg" in filename or "gif" in filename:
		return True
	return False


def show_result(request, name):
	pic = {"DIR": "/static/upload/" + name,
			"name": []}
	dic = {}
	path = BASE_DIR + "/static/upload/" + name + "/"
	for home, dirs, files in os.walk(path):
		if "result.txt" in files:
			with open(path + "result.txt", "r", encoding="utf-8") as res:
				js = res.read()
				dic = json.loads(js)
		for filename in files:
			if isImage(filename):
				pic["name"].append(filename)
	dic["pic"] = pic
	return render(request, 'show_result.html', {
			'data': json.dumps(dic),
		})


def ajax_load_menu(request):
	file_list = []
	if request.method == 'GET':
		for home, dirs, files in os.walk(BASE_DIR + "/static/upload"):
			dirs.remove("uploadfile")
			dirs.remove("default")
			return JsonResponse(dirs, safe=False);
	return HttpResponse("Error")
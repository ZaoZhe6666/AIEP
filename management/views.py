from django.shortcuts import render, render_to_response
from django.db import models
import json, time, re
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

def welcome(request):
	# return render_to_response('welcome.html')
	return render_to_response('index.html')

def page_not_found(request):
	return render_to_response('404.html')

def submit(request):
	return render_to_response('submit.html')

def submit_check(request):
	if request.method == 'GET':
		return render_to_response('index.html')
	elif request.method == 'POST':
		print(request.POST)
		try:
			pro_name = request.POST.get("name")
			pro_jingxiang = request.POST.get("jingxiang")
			pro_gpu_type = request.POST.get("gpu_type")
			pro_describe = request.POST.get("describe")
			pro_retry = request.POST.get("retryCount")
			pro_evalu = request.POST.get("evaluate")
			pro_model = request.POST.get("model")
			print("name: ", pro_name)
			print("jingxiang: ", pro_jingxiang)
			print("gpu_type: ", pro_gpu_type)
			print("describe: ", pro_describe)
			print("retry: ", pro_retry)
			print("evalu: ", pro_evalu)
			print("model: ", pro_model)
		except Exception as e:
			print(e)
	return render_to_response('submit.html')
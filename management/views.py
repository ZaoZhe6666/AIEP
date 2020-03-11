from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.db import models
import json, time, re
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from AIEP.settings import BASE_DIR
import os
import random
from django.contrib.auth.models import User
from .forms import TaskSubmitForm, RunSubmitForm
from .models import TaskSubmit, TaskColumn, ShowImgAfterUpload, runSubmit
import subprocess
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import time
import shutil
from django.db.models import Q

status_num = []
status_name = []


def welcome(request):
    return render_to_response('welcome.html')


def page_not_found(request, exception):
    return render_to_response('404.html')


@login_required(login_url='/privileges/login')
def submit(request):
    if request.method == 'POST':
        run_submit_form = RunSubmitForm(request.POST)
        if run_submit_form.is_valid():
            new_run = run_submit_form.save(commit=False)
            new_run.author = User.objects.get(id=request.user.id)
            new_run.modelname = request.FILES.get("model", None).name.split('.')[0][0:20]
            new_run.save()
            now = int(time.time())
            time_array = time.localtime(now)
            time_part = time.strftime("%Y_%m_%d-%H%M%S", time_array)
            os.mkdir(BASE_DIR + "/static/upload/uploadfile/" + time_part)
            src_path = BASE_DIR + "/static/upload/Results/2020_02_18-164203"
            dst_path = BASE_DIR + "/static/upload/Results/" + time_part
            shutil.copytree(src_path, dst_path)
            upload_file = request.FILES.get('model')
            if upload_file != None:
                print("file is not empty!")
                filename = time_part + '.' + upload_file.name.split('.')[-1]
                filepath = os.path.join(BASE_DIR + "/static/upload/uploadfile/" + time_part, filename)
                f = open(filepath, 'wb')
                for i in upload_file.chunks():
                    f.write(i)
                f.close()
            else:
                print("file is empty!")
            # p = subprocess.Popen(
            #    "python /home/aiep/soft/aiepalg_code/SUIBUAA_Sample/test/testimport.py --save_path " + time_part)
            # except Exception as e:
            # 	print(e)
            set_status(['Accuracy', 'Decision Boundary', 'Sensitivity'])
            return render(request, 'waiting.html')
            # return redirect("management:run_record")
        else:
            ErrorDict = run_submit_form.errors
            Error_Str = json.dumps(ErrorDict)
            Error_Dict = json.loads(Error_Str)
            return HttpResponse(Error_Dict.values())
    else:
        run_submit_form = RunSubmitForm()
        context = {'run_submit_form': run_submit_form}
        return render(request, 'submit.html', context)


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
        # output = subprocess.Popen("python D:/LABOR/temp/testimport.py --defense_model zhaoze_model")
        p = subprocess.Popen(
            "python /home/aiep/soft/aiepalg_code/SUIBUAA_Sample/test/testimport.py --save_path " + time_part)
        # except Exception as e:
        # 	print(e)
        set_status(['Accuracy', 'Decision Boundary', 'Sensitivity'])
    return render(request, 'waiting.html')


def showline(request):
    currency = {"labels": ["clean", "adver", "corru", "something", "else"],
                "datasets": [89.8, 27.6, 57.6, 45.8, 99.8]}
    judge_edge_dis = {"label": ["checkpoint1", "checkpoint2", "checkpoint3", "checkpoint4"],
                      "data": {"2a": [[10.1, 12.5, 20.3, 28.9]], "2b": [[5.3, 7.9, 12.8, 21.4]]}}
    pic = {"DIR": "/static/img/2020_01_08/",
           "name": ["1.png", "2.png", "3.png", "4.png"]}
    dic = {"currency": currency,
           "judge_edge_dis": judge_edge_dis,
           "pic": pic}
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
    pic = {"DIR": "/static/upload/Results/" + name + "/",
           "name": []}
    dic = {}
    path = BASE_DIR + "/static/upload/Results/" + name + "/"
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
        for home, dirs, files in os.walk(BASE_DIR + "/static/upload/Results"):
            return JsonResponse(dirs, safe=False)
    return HttpResponse("Error")


def show_status(request):
    global status_num
    for i in range(len(status_num)):
        status_num[i] += random.randint(1, 20)
    return JsonResponse(status_num, safe=False)


def set_status(status):
    global status_num
    global status_name
    status_name = status
    status_num = [0] * len(status)


def ajax_load_per_style(request):
    global status_name
    return JsonResponse(status_name, safe=False)


@login_required(login_url='/privileges/login/')
def task_submit(request):
    # 判断用户是否提交数据
    print("I am in task_submit!")
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        task_submit_form = TaskSubmitForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if task_submit_form.is_valid():
            new_task = task_submit_form.save(commit=False)
            # 指定登录的用户为作者
            new_task.author = User.objects.get(id=request.user.id)
            new_task.save()
            return redirect("management:task_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        task_submit_form = TaskSubmitForm()
        # 文章栏目
        # columns = TaskColumn.objects.all()
        # 赋值上下文
        imgs = ShowImgAfterUpload.objects.all()
        context = {'task_submit_form': task_submit_form, "imgs": imgs}  # , 'columns': columns
        # 返回模板
        return render(request, 'TaskSubmit.html', context)


def task_detail(request, id):
    task = get_object_or_404(TaskSubmit, id=id)
    return render(request, 'taskDetail.html', {'task': task})


@login_required(login_url='/privileges/login/')
def task_delete(request, id):
    task = TaskSubmit.objects.get(id=id)
    if request.user != task.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    task.delete()
    return redirect("management:task_list")


def task_list(request):
    flag = ''
    if_join = request.GET.get('join')
    all_task_list = TaskSubmit.objects.all()
    user = User.objects.get(id=request.user.id)
    join_list = user.tasksubmit_set.all()
    notjoin_list = all_task_list.exclude(pk__in=join_list)
    if if_join == 'joined':
        task_list = join_list
        flag = 'join'
    else:
        task_list = notjoin_list
        flag = 'not_join'
    paginator = Paginator(task_list, 6)
    page = request.GET.get('page')
    tasks = paginator.get_page(page)
    context = {'tasks': tasks, 'flag': flag}
    return render(request, 'taskList.html', context)


def joinTask(request, id):
    user = User.objects.get(id=request.user.id)
    task = TaskSubmit.objects.get(id=id)
    task.participant.add(user)
    return redirect("management:task_list")


@login_required(login_url='/privileges/login/')
def run_record(request):
    search = request.GET.get('search')
    user_run_list = runSubmit.objects.filter(author=request.user.id)
    if search:
        run_list = user_run_list.filter(Q(title__icontains=search) | Q(description__icontains=search)).order_by(
            '-created')
    else:
        search = ''
        run_list = user_run_list.order_by('-created')
    paginator = Paginator(run_list, 6)
    page = request.GET.get('page')
    runs = paginator.get_page(page)
    context = {'runs': runs, 'search': search}
    return render(request, 'runRecord.html', context)


@login_required(login_url='/privileges/login/')
def run_delete(request, id):
    run = runSubmit.objects.get(id=id)
    if request.user != run.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    run.delete()
    return redirect("management:run_record")

from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.db import models
import json, time, re
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from AIEP.settings import BASE_DIR
import os
import random
from django.contrib.auth.models import User
from .forms import TaskSubmitForm, RunSubmitForm, TaskInnerSubmitForm, DatasetSubmitForm, CommentForm, ForumSubmitForm
from .models import TaskSubmit, TaskColumn, ShowImgAfterUpload, runSubmit, Task_User, Comment, Datasets, Forum
import subprocess
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import time
import shutil
from django.db.models import Q
from django.utils import timezone
from django import forms
from django.forms import widgets
from django.forms import fields
from django.forms import ModelChoiceField
import random
from notifications.signals import notify
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


def welcome(request):
    return render_to_response('welcome.html')


def page_not_found(request, exception):
    return render_to_response('404.html')


@login_required(login_url='/privileges/login')
def submit(request):
    if request.method == 'POST':
        return submit_check(request)
        # 表单适配
        run_submit_form = RunSubmitForm(request.POST)
        if run_submit_form.is_valid():
            # 表单存储
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
            #     print(e)
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
        # print("后端收到如下信息：", request.body)
        now = int(time.time())
        time_array = time.localtime(now)
        time_part = time.strftime("%Y_%m_%d-%H%M%S", time_array)
        save_path = BASE_DIR + "/static/upload/Results/" + time_part + "/"
        os.mkdir(save_path)

        # 添加进度分析文件
        with open(save_path + "temp.txt", "w") as file:
            percent_dic = {}
            attack_method_list = request.POST.getlist("attack_method")
            for key in attack_method_list:
                percent_dic[key] = 0
            file.write(json.dumps(percent_dic))

        # 存储用户上传模型
        upload_model = request.FILES.get('model')
        model_name = ""
        if upload_model != None:
            filename = upload_model.name
            filepath = os.path.join(save_path, filename)
            model_name = filename.split('.')[0]
            f = open(filepath, 'wb')
            for i in upload_model.chunks():
                f.write(i)
            f.close()
        upload_model_data = request.FILES.get('model_data')
        data_path = ""
        if upload_model_data != None:
            filename = time_part + '.' + upload_model_data.name.split('.')[-1]
            data_path = save_path + filename
            filepath = os.path.join(save_path, filename)
            f = open(filepath, 'wb')
            for i in upload_model_data.chunks():
                f.write(i)
            f.close()

        # 执行算法
        try:
            Algorithm_DIR = "D:/LABOR/SUIBUAA_AIEP/test/"
            attack_method_list = request.POST.getlist("attack_method")
            evaluate_method = request.POST.get("evaluate_method")
            for attack_method in attack_method_list:
                command = "python " + Algorithm_DIR + "testimport.py"
                command += " --attack_method " + attack_method
                command += " --evaluation_method " + evaluate_method
                command += " --save_path " + save_path
                command += " --defense_model " + "static.upload.Results." + time_part + "." + model_name
                command += " --model_defence_dir " + data_path
                output = subprocess.Popen(command, cwd = Algorithm_DIR)
        # p = subprocess.Popen(
        #     "python /home/aiep/soft/aiepalg_code/SUIBUAA_Sample/test/testimport.py --save_path " + time_part)
        except Exception as e:
            print(e)
        
    return render(request, 'waiting.html', {
        'data': json.dumps({'time_part' : time_part}),
    })


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
        if "temp.txt" in files:
            dic["time_part"] = name
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

def ajax_load_status(request):
    time_part = request.GET.get("data")
    with open(BASE_DIR + "/static/upload/Results/" + time_part + "/temp.txt", "r") as load_f:
        status = json.load(load_f)
    return JsonResponse(status, safe=False)



class DatasetChoose(forms.Form):
    dataset = fields.ChoiceField(
        choices=Datasets.objects.all().values_list('id', 'name'),
        widget=widgets.Select(attrs={'class': "form-control custom-select"})
    )

    def __init__(self, *args, **kwargs):
        super(DatasetChoose, self).__init__(*args, **kwargs)
        self.fields['dataset'].choices = Datasets.objects.all().values_list('id', 'name')


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
            task_submit_form.save_m2m()
            return redirect("management:task_list")
        # 如果数据不合法，返回错误信息
        else:
            ErrorDict = task_submit_form.errors
            Error_Str = json.dumps(ErrorDict)
            Error_Dict = json.loads(Error_Str)
            return HttpResponse(Error_Dict.values())
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        task_submit_form = TaskSubmitForm()
        # 文章栏目
        # columns = TaskColumn.objects.all()
        datasets = DatasetChoose()
        # 赋值上下文
        imgs = ShowImgAfterUpload.objects.all()
        context = {'task_submit_form': task_submit_form, "imgs": imgs, 'datasets': datasets}  # , 'columns': columns
        # 返回模板
        return render(request, 'TaskSubmit.html', context)


def task_detail(request, id):
    task = get_object_or_404(TaskSubmit, id=id)
    # 比赛排名
    task_rank = Task_User.objects.filter(task=task).order_by('-best')
    # 是否参加比赛 是否是比赛发起者
    is_owner = False
    if Task_User.objects.filter(task=task, user=request.user).exists():
        is_join = True
        if task.author == request.user:
            is_owner = True
    else:
        is_join = False
    num = task_rank.count()
    dataSet = Datasets.objects.get(id=task.dataset)
    comments = Comment.objects.filter(Task=id)
    comment_form = CommentForm()
    nowTime = timezone.now()
    context = {'task': task, 'comments': comments, 'comment_form': comment_form,
               'task_rank': task_rank, 'dataSet': dataSet, 'nowTime': nowTime,
               'is_join': is_join, 'is_owner': is_owner, 'num': num}
    return render(request, 'taskDetail.html', context)


@login_required(login_url='/privileges/login/')
def task_delete(request, id):
    task = TaskSubmit.objects.get(id=id)
    if request.user != task.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    task.delete()
    return redirect("management:task_list")


def task_list(request):
    flag = ''
    tag = request.GET.get('tag')
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
    if tag and tag != 'None':
        task_list = task_list.filter(tags__name__in=[tag])
    paginator = Paginator(task_list, 6)
    page = request.GET.get('page')
    tasks = paginator.get_page(page)
    context = {'tasks': tasks, 'flag': flag}
    return render(request, 'taskList.html', context)


def joinTask(request, id):
    user = User.objects.get(id=request.user.id)
    task = TaskSubmit.objects.get(id=id)
    task.participant.add(user)
    Task_User.objects.create(user=user, task=task)
    return redirect("management:task_detail", id)


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

def task_demo(request):
    return render_to_response('task_demo.html')


def task_innerSubmit(request, id):
    if request.method == "POST":
        run_submit_form = TaskInnerSubmitForm(request.POST)
        task = TaskSubmit.objects.get(id=id)
        user = request.user
        new_run = run_submit_form.save(commit=False)
        new_run.author = user
        new_run.modelname = request.FILES.get("model", None).name.split('.')[0][0:20]
        new_run.dataset = task.dataset
        new_run.algorithm = task.algorithm
        new_run.ind = task.ind
        new_run.save()
        task.submit.add(new_run)
        now = int(time.time())
        time_array = time.localtime(now)
        time_part = time.strftime("%Y_%m_%d-%H%M%S", time_array)
        os.mkdir(BASE_DIR + "/static/upload/uploadfile/" + time_part)
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
        grade = random.randint(85, 99)
        task_user = Task_User.objects.get(task=task, user=user)
        task_user.submitNum = task_user.submitNum + 1
        time_now = timezone.now()
        if grade > task_user.best:
            task_user.best = grade
            task_user.bestTime = time_now
        task_user.save()
        return redirect("management:task_detail", id)
    else:
        run_submit_form = TaskInnerSubmitForm(request.POST)
        context = {'run_submit_form': run_submit_form}
        return render(request, '', context)


def DatasetSubmit(request):
    if request.method == "POST":
        dataset_submit_form = DatasetSubmitForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if dataset_submit_form.is_valid():
            dataset = dataset_submit_form.save(commit=False)
            dataset.author = User.objects.get(id=request.user.id)
            dataset.save()
            return redirect("management:dataset_list")
        else:
            ErrorDict = dataset_submit_form.errors
            Error_Str = json.dumps(ErrorDict)
            Error_Dict = json.loads(Error_Str)
            return HttpResponse(Error_Dict.values())
    # 如果用户请求获取数据
    else:
        dataset_submit_form = DatasetSubmitForm(request.POST, request.FILES)
        context = {'dataset_submit_form': dataset_submit_form}
        return render(request, 'datasetSubmit.html', context)


def XmlSubmit(request):
    if request.method == "POST":
        pass



def dataset_list(request):
    dataset_list = Datasets.objects.all()
    user = User.objects.get(id=request.user.id)
    paginator = Paginator(dataset_list, 6)
    page = request.GET.get('page')
    datasets = paginator.get_page(page)
    context = {'datasets': datasets}
    return render(request, 'datasetlist.html', context)

@login_required(login_url='/privileges/login/')
def post_comment(request, id, parent_comment_id=None):
    task = get_object_or_404(TaskSubmit, id=id)
    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.task = task
            new_comment.Task_id = task.id
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                # 新增代码，给其他用户发送通知
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=task,
                        action_object=new_comment,
                    )

                return HttpResponse('200 OK')

            new_comment.save()
            # 新增代码，给管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=task,
                    action_object=new_comment,
                )

            return redirect(task)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'id': id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'reply.html', context)

class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'noticelist.html'
    # 登录重定向
    login_url = '/privilege/login/'

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
    """更新通知状态"""
    # 处理 get 请求
    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            task = TaskSubmit.objects.get(id=request.GET.get('task_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(task)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('management:notice_list')

def forum_list(request):
    forums = Forum.objects.all()
    context = {'forums': forums}
    return render(request, 'forumlist.html', context)


def forum_create(request):
    if request.method == "POST":
        forum_post_form = ForumSubmitForm(request.POST)
        if forum_post_form.is_valid():
            new_forum = forum_post_form.save(commit=False)
            new_forum.author = request.user
            new_forum.save()
            return redirect("management:forum_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        forum_post_form = ForumSubmitForm()
        context = { 'forum_post_form ': forum_post_form  }
        return render(request, 'forum_create.html', context)


from django.shortcuts import render,HttpResponse,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect
from CodeDiff.models import ProjectInfo,ServerInfo,TaskInfo,UserInfo
from CodeDiff.util.common import add_task_logic,delete_task,get_ajax_msg,edit_task_logic,add_register_data
from CodeDiff.util.run_diff import RunDiff
import json
import os

# Create your views here.
def login_check(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('login_status'):
            return HttpResponseRedirect('/')
        if not request.session.get('auth'):
            return HttpResponse('您的账号目前还没有开通项目权限，请联系管理员开通')
        return func(request, *args, **kwargs)
    return wrapper

def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pw')

        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            request.session["login_status"] = True
            request.session["now_account"] = username
            request.session['auth'] = UserInfo.objects.get(username=username).auth
            return HttpResponseRedirect('/index/')
        else:
            request.session["login_status"] = False
            return render_to_response("login.html")
    elif request.method == 'GET':
        return render_to_response("login.html")

def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.is_ajax():
        user_info = json.loads(request.body.decode('utf-8'))
        msg = add_register_data(**user_info)
        return HttpResponse(get_ajax_msg(msg, '恭喜您，账号已成功注册'))
    elif request.method == 'GET':
        return render_to_response("register.html")

@login_check
def log_out(request):
    """
    注销登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        del request.session['now_account']
        del request.session['login_status']
        del request.session['auth']
        return HttpResponseRedirect("/")

@login_check
def index(request,eid=0):
    """
    首页
    :param request:
    :param eid:
    :return:
    """
    if request.is_ajax():
        kwargs = json.loads(request.body.decode('utf-8'))
        mode = kwargs.pop('mode')
        id = kwargs.pop('id')
        if mode == 'del':
            msg = delete_task(id)
        return HttpResponse(get_ajax_msg(msg, 'ok'))
    else:
        user = request.session["now_account"]
        ids = request.session['auth']
        ids_list = ids.split(',')
        pro_list = ProjectInfo.objects.filter(id__in=ids_list)
        ser_list = ServerInfo.objects.all()
        if eid == 0:
            task_list = TaskInfo.objects.filter(belong_pro_id__in=ids_list)
        else:
            if str(eid) in ids_list:
                task_list = TaskInfo.objects.filter(belong_pro_id=eid)
            else:
                task_list = []
        return render(request, 'index.html',{'pro_list':pro_list,
                                             'ser_list':ser_list,
                                             'ser':'All',
                                             'id':eid,
                                             'task_list':task_list,
                                             'user':user})

@login_check
def task_search(request,eid=0):
    """
    任务查询
    :param request:
    :param eid:
    :return:
    """
    user = request.session["now_account"]
    ids = request.session['auth']
    ids_list = ids.split(',')
    search_ser = request.GET.get('server', '')
    pro_list = ProjectInfo.objects.filter(id__in=ids_list)
    ser_list = ServerInfo.objects.all()
    if eid == 0:
        if search_ser != 'All':
            task_list = TaskInfo.objects.filter(belong_server__server_name=search_ser,belong_pro_id__in=ids_list)
        else:
            task_list = TaskInfo.objects.filter(belong_pro_id__in=ids_list)
    else:
        if search_ser != 'All':
            if str(eid) in ids_list:
                task_list = TaskInfo.objects.filter(belong_server__server_name=search_ser,belong_pro_id=eid)
            else:
                task_list = []
        else:
            if str(eid) in ids_list:
                task_list = TaskInfo.objects.filter(belong_pro_id=eid)
            else:
                task_list = []
    return render(request,'index.html',{'pro_list':pro_list,
                                         'ser_list':ser_list,
                                         'ser':search_ser,
                                         'id':eid,
                                         'task_list':task_list,
                                         'user': user})

@login_check
def add_task(request,eid=0):
    """
    添加任务
    :param request:
    :param eid:
    :return:
    """
    if request.method == 'POST':
        if eid != 0:
            pro = ProjectInfo.objects.get(id=eid).project_name
        else:
            pro = request.POST.get('pro', '')
        task_name = request.POST.get('task_name', '')
        ser = request.POST.get('ser', '')
        rel = request.POST.get('rel_name','')
        branch_no = request.POST.get('branch_no', '')
        kwargs = {'task_name':task_name,'pro':pro,'ser':ser,'rel_name':rel,'branch_no':branch_no}
        add_task_logic(**kwargs)
        return HttpResponseRedirect('/index/'+str(eid))
    elif request.method == 'GET':
        user = request.session["now_account"]
        ids = request.session['auth']
        ids_list = ids.split(',')
        pro_list = ProjectInfo.objects.filter(id__in=ids_list)
        ser_list = ServerInfo.objects.all()
        return render(request,"add_task.html",{'id':eid,
                                               'pro_list': pro_list,
                                               'ser_list': ser_list,
                                               'user':user})

@login_check
def edit_task(request,tid,eid=0):
    """
    编辑任务
    :param request:
    :param tid:
    :param eid:
    :return:
    """
    if request.method == 'POST':
        pro = request.POST.get('pro', '')
        task_name = request.POST.get('task_name', '')
        ser = request.POST.get('ser', '')
        rel = request.POST.get('rel_name','')
        branch_no = request.POST.get('branch_no', '')
        kwargs = {'task_name':task_name,'pro':pro,'ser':ser,'rel_name':rel,'branch_no':branch_no}
        edit_task_logic(tid,**kwargs)
        return HttpResponseRedirect('/index/'+str(eid))
    elif request.method == 'GET':
        user = request.session["now_account"]
        task = get_object_or_404(TaskInfo, id=tid)
        pro = task.belong_pro.project_name
        ser = task.belong_server.server_name
        rel = task.rel_name
        commit = task.branch_no
        task_name = task.task_name
        ser_list = ServerInfo.objects.all()
        return render(request,"edit_task.html",{'task':task_name,
                                               'pro': pro,
                                               'ser_list': ser_list,
                                                'ser':ser,
                                                'commit':commit,
                                                'eid':eid,
                                                'tid':tid,
                                                'user':user,
                                                'rel':rel})

@login_check
def jacoco_diff(request,eid,tid):
    """
    查看对应任务的变更代码覆盖率数据
    :param request:
    :param eid:
    :param tid:
    :return:
    """
    user = request.session["now_account"]
    task = TaskInfo.objects.get(id=tid)
    task_name = task.task_name
    rel_name = task.rel_name
    old_version = task.branch_no
    project_dir= os.path.join('/jenkins/workspace',task_name)  #对应服务在jenkin代码覆盖率任务的路径
    rel_dir = os.path.join('/jenkins/workspace',rel_name)  #对应服务在jenkin构建和发布任务的路径
    process = RunDiff(project_dir,old_version,rel_dir)
    ret = process.run_diff(eid,task_name)
    return render(request,'code_diff.html',{'ret':ret,
                                            'task_name':task_name,
                                            'eid':eid,
                                            'user':user})

@login_check
def diff_report(request,eid,task,package,class_name):
    """
    展示对应代码覆盖率的详情
    :param request:
    :param eid:
    :param task:
    :param package:
    :param class_name:
    :return:
    """
    dir = os.path.join(str(eid),task,package,"{}.java.html".format(class_name))
    return render_to_response(dir)

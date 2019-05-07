from CodeDiff.models import ProjectInfo,ServerInfo,TaskInfo,UserInfo
from django.db import DataError


def add_task_logic(**kwargs):
    belong_project = kwargs.pop('pro')
    belong_server = kwargs.pop('ser')
    kwargs['belong_pro'] = ProjectInfo.objects.get(project_name=belong_project)
    kwargs['belong_server'] = ServerInfo.objects.get(server_name=belong_server)
    TaskInfo.objects.create(**kwargs)

def edit_task_logic(tid,**kwargs):
    belong_project = kwargs.pop('pro')
    belong_server = kwargs.pop('ser')
    kwargs['belong_pro'] = ProjectInfo.objects.get(project_name=belong_project)
    kwargs['belong_server'] = ServerInfo.objects.get(server_name=belong_server)
    TaskInfo.objects.filter(id=tid).update(**kwargs)

def delete_task(id):
    try:
        TaskInfo.objects.filter(id=id).delete()
        return 'ok'
    except Exception:
        return 'error'

def get_ajax_msg(msg, success):
    """
    ajax提示信息
    :param msg: str：msg
    :param success: str：
    :return:
    """
    return success if msg is 'ok' else msg

def add_register_data(**kwargs):
    """
    用户注册信息逻辑判断及落地
    :param kwargs: dict
    :return: ok or tips
    """
    user_info = UserInfo.objects
    try:
        username = kwargs.pop('user')
        password = kwargs.pop('pw')
        station = kwargs.pop('station')

        if user_info.filter(username__exact=username).count() > 0:
            return '该用户名已被注册，请更换用户名'
        user_info.create(username=username, password=password, station=station)
        return 'ok'
    except DataError:
        return '字段长度超长，请重新编辑'


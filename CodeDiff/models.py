from django.db import models

# Create your models here.
class BaseTable(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
        verbose_name = '公共字段表'
        db_table = 'BaseTable'

class ProjectInfo(BaseTable):
    project_name = models.CharField('项目名称',max_length=50,unique=True,null=False)
    test_user = models.CharField('测试人员',max_length=200, null=True)
    project_ver = models.CharField('版本',max_length=25,null=False)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = '项目信息'
        db_table = 'ProjectInfo'

class ServerInfo(BaseTable):
    server_name = models.CharField('服务名称',max_length=50,unique=True,null=False)

    def __str__(self):
        return self.server_name

    class Meta:
        verbose_name = '服务信息'
        db_table = 'ServerInfo'

class TaskInfo(BaseTable):
    task_name = models.CharField('任务名称',max_length=50,unique=True,null=False)
    branch_no = models.CharField('比对分支',max_length=50)
    rel_name = models.CharField('发布名称',max_length=100,null=True)
    belong_pro = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    belong_server = models.ForeignKey(ServerInfo,on_delete=models.CASCADE)

    class Meta:
        verbose_name = '任务信息'
        db_table = 'TaskInfo'

class UserInfo(BaseTable):
    username = models.CharField('用户名',max_length=20,unique=True,null=False)
    password = models.CharField('密码',max_length=20,null=False)
    station = models.CharField('岗位',max_length=20,null=False)
    auth = models.CharField('项目权限',max_length=20)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        db_table = 'UserInfo'


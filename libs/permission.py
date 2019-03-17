from django.http import HttpResponseForbidden, HttpResponse
from libs.printf import print_debug as print
TOKEN_NAME = 'TOKEN'

def permission(request, model, type):
    '''
    验证权限，
    :param request:request
    :param model: model编号：PERMISSION_MODEL对应
    :param type: 权限类型：PERMISSION_TYPE对应
    :return:
    '''
    token = request.META.get(TOKEN_NAME)  # 获取token
    prm = token.get('prm')  # 从token获取权限
    if permission_validate(prm, model, type):  # 验证权限
        print('权限通过')
        return True
    else:
        print('权限不通过')
        return False


def permission_validate(prm, model, type):
    '''
    比对权限
    :param prm: 权限列表
    :param model: model编号：PERMISSION_MODEL对应
    :param type: 权限类型：PERMISSION_TYPE对应
    :return: T/F
    '''
    if model in prm:

        this_model_prm = prm[model]
        if 0 in this_model_prm:
            return True
        if type in this_model_prm:
            return True
    return False


def get_permission(jobid):
    pass


def forbidden_view():
    return HttpResponse('无权操作')

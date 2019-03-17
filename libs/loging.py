from system.models import Operationlog
import datetime
import re
from libs.printf import print_debug as print
URL_MODEL_TYPE = {
    'system':{
        'userinfo':('userid','人员',11),
        'jobtype':('jobid','岗位',12),
        'operation':('user_id','日志',19),
        'permission':('job_id','权限',12)
    },
    'craftwork':{
        'craftwork':('craftwork_id','工艺',8),
        'craftworkequipment':('craftwork_id','工艺设备',8),
        'craftworkmould':('craftwork_id','工艺模具',8),
        'craftworkoperater':('craftwork_id','工艺岗位',8),
        'materialcraftwork':('craftworkid','物料工艺',8),
    },
    'equipment':{
        'equipment':('equipmentid','设备',5),
        'equipmentmainten':('maintenid','设备维保计划',9),
        'equipmenttechparam':('id','设备技术参数',5),
        'equiptype':('etypeid','设备类型',5)
    },
    'inventory':{
        'delivery':('deliveryid','出库单',15),
        'deliveryinfo':('delivery_id','出库信息',15),
        'inventory':('inventoryid','库存',4),
        'warehousing':('warehousingid','入库单',16),
        'warehousinginfo':('warehousing_id','入库信息',16)
    },
    'material':{
        'material':('materialid','物料',3),
        'materialBOM':('parent_id','物料BOM',3)
    },
    'moulds':{
        'mould':('mouldid','模具',6),
        'mouldrepair':('repairid','模具维修计划',10),
        'mouldtype':('mtypeid','模具类型',6)
    },
    'order':{
        'customer':('customerid','客户',17),
        'order':('orderid','订单',0),
        'supplier':('supplierid','供应商',18)
    },
    'orderform':{
        'ordermaterial':('workid','制令单',1),
        'plan':('planid','计划',2),
        'planfeedback':('plan_id','计划反馈',13),
        'arrange':('workid','安排计划',14)
    },
    'qualinspect':{
        'craftworkqinspect':('projectid','工艺-质检项目',8),
        'dashsampling':('dashnum','零件检测',7),
        'qualinspection':('qinspectid','质量检查',7),
        'sampling':('dashnum_id','检查记录',7)
    },
    'statist':{
        'order':('id','订单-统计图表',0)
    }

}


def loging(request, describe,level, remark=''):
    token = request.META.get('TOKEN')
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    url = f'[{get_time()}]  "{request.method} {request.path}"'
    Operationlog.objects.create(user=token.get('user'), ip=ip, level=level,url=url, describe=describe, remark=remark)


def get_time():
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(date)


def parse_api_url(api_url,retrieve=False):
    if retrieve:
        parse = re.search(r'/(\w+)/api/(\w+)/(\w+)/', api_url)
        return (URL_MODEL_TYPE[parse.group(1)].get(parse.group(2)),parse.group(3))
    else:
        parse = re.search(r'/(\w+)/api/(\w+)/',api_url)
        return URL_MODEL_TYPE[parse.group(1)].get(parse.group(2))


def parse_extra_url(extra_url,retrieve=False):
    if retrieve:
        parse = re.match(r'/(\w+)/(\w+)/(\w+)/', extra_url)
        print((URL_MODEL_TYPE[parse.group(1)].get(parse.group(2)),parse.group(3)))
        return (URL_MODEL_TYPE[parse.group(1)].get(parse.group(2)),parse.group(3))
    else:
        parse = re.match(r'/(\w+)/(\w+)/',extra_url)
        print(URL_MODEL_TYPE[parse.group(1)].get(parse.group(2)))
        return URL_MODEL_TYPE[parse.group(1)].get(parse.group(2))


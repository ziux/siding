from .db import select_sql
from libs.printf import print_debug as print,print_error

def get_screen_data(field,table,where=None,many=False):
    '''

    :param field: 字段名
    :param table: 表名
    :param where:where条件，{}
    :return: [] 值
    '''
    this_where = 'df=0'
    args = []
    if where:
        for key,value in where.items():
            this_where += f' and `{key}`="{value}"'
            # args.append(value)
    this_field = f'`{field}`'
    if many:
        fieldlist = field.split(',')
        this_field = f'`{ fieldlist[0]}`'
        for f in fieldlist[1:]:
            this_field += f',`{f}`'
    sql = f'select {this_field} from `{table}` WHERE {this_where} GROUP BY {this_field}; '
    # print(sql)
    try:
        data = select_sql(sql)
        # print(data)
    except Exception as e:
        print_error(e,sql)
        return []
    if not data:
        return []
    screenlist = []
    if many:
        for d in data:
            screenlist.append(d)
    else:
        for d in data:
            screenlist.append(d[0])
    return screenlist


def get_foreign_screen_data(foreign_fields,foreign_table,table,compare,where=None):
    '''
    外键字段作为筛选条件时，获取筛选数据
    :param foreign_fields: 要从外键表中获取的字段
    :param foreign_table: 外键表名
    :param table: 当前表名
    :param compare: 比较字段，（外键在当前表中的字段名，对应外键表中的字段名）
    :param where: 其他条件，对应外键表中的筛选
    :return:
    '''
    this_compare,foreign_compare = compare
    this_where = f'`df`=0 and `{foreign_compare}` in (select `{this_compare}` from `{table}` where `df`=0 ) '
    args = []
    if where:
        for key,value in where.items():
            this_where += f' and `{key}`="{value}"'

    fieldlist = foreign_fields.split(',')
    this_field = f'`{ fieldlist[0]}`'
    if len(fieldlist)>1:
        for f in fieldlist[1:]:
            this_field += f',`{f}`'
    sql = f'select {this_field} from `{foreign_table}` WHERE {this_where} GROUP BY {this_field}; '
    # print(sql)
    try:
        data = select_sql(sql)
    except Exception as e:
        print(e)
        return []
    if not data:
        return []
    screenlist = []
    for d in data:
        screenlist.append(d)
    return tplist_to_dict(screenlist)



def choice_to_dict(choice):
    '''
    将类似于((1,''),(2,''))转化为适合json的dict
    :param choice: 元祖
    :return: {} 值
    '''
    dct = {}
    for c in choice:
        key,value = c
        dct[key] = value
    return dct


def tplist_to_dict(tuplelist):
    '''
    将元组列表转化为合适json的dict，其中元组中第一个值作为dict的键，第三个及以上的值有括号
    :param tuplelist:
    :return:
    '''
    dct = {}
    for t in tuplelist:
        key,*value = t
        value = [str(v) for v in value]
        if len(value) > 1:
            dct[key] = value[0]+'(%s)' % ','.join(value[1:])
        elif value:
            dct[key] = value[0]
    return dct


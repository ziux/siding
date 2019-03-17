import os
from siding.settings import TEMPLATES
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.conf.urls import url
from libs.screen_libs import choice_to_dict, get_screen_data
from django.db.models.fields import DateTimeField, DateField, FloatField, IntegerField, DecimalField
from libs.printf import print_debug as print
from libs.permission import permission, forbidden_view
from libs.loging import parse_extra_url, parse_api_url
from django.core.paginator import Paginator
from libs.constant_pool import PAGE_FIELD_NAME, PAGE_SIZE_FILED_NAME, PAGE_SIZE, SEARCH_FIELD_NAME, ORDER_FIELD_NAME
from django.db.models import Q


class BaseView():
    '''
    创建list，create，update的视图
    筛选所需数据:
        格式：
            '字段名': {
                'name': '中文名',
                'type': 类型,
                'value': 值
            }
        筛选数据的type 0：list,1：dict，2：date，3：datetime，4：int，
        其中 int 可选vlaue值:
             max number	规定允许的最大值
             min number	规定允许的最小值
             step number	规定合法的数字间隔（如果 step="3"，则合法的数是 -3,0,3,6 等）
             value number	规定默认值
    用于继承
    必要数据:
    Model:模型
    templaters_path：模板所在path，template目录下
    其他参数:
    fields:
        可以进行查找的字段，查找本字段会返回这个字段的所有值的集合
        格式['字段名'，]
    default_view:默认list视图模板，
    default_createframe/default_updateframe:默认创建、修改视图模板
    js_path()：js路径，static目录下,默认js/{{templaters_path}}
    get_view_context():list视图context
    get_create_context():create视图context
    get_update_context()：update视图context
    get_screen_context()：筛选数据context
    模板默认参数：
    js_path:对应js文件
    tmpl:创建视图中参照数据
    data:修改视图数据
    '''
    templaters_path = ''
    default_view = 'view.html'
    default_view_js = 'view.js'
    default_retrieve = 'retrieve.html'
    default_createframe = 'createframe.html'
    default_createframe_js = 'createframe.js'
    default_updateframe = 'updateframe.html'
    default_updateframe_js = 'updateframe.js'
    Model = None
    fields = ()
    router_pool = []
    search_fields = ()
    create_fields = ()
    update_fields = ()

    def js_path(self):
        '''
        js路径，static目录下,默认js/{{templaters_path}}
        :return:
        '''
        return os.path.join('js', self.templaters_path)

    def get_view_context(self, context):
        '''
        视图详情界面的数据
        :param context:
        :return:
        '''
        return context

    def get_create_context(self, context):
        '''
        创建视图的数据
        :param context:
        :return:
        '''
        return context

    def get_update_context(self, context):
        '''
        修改界面的数据
        :param context:
        :return:
        '''
        return context

    def get_retrieve_context(self, context):
        '''
        详情界面的数据
        :param context:
        :return:
        '''
        return context

    def get_screen_context(self, data):
        return data

    def _model_fields(self, model=None):
        '''
        获取model的所有字段的verbose_name，column，choices，type
        :param model:
        :return:
        '''
        fields_dict = {}
        # 获取所有字段
        if not model:
            flds = self.Model._meta.fields
        else:
            flds = model._meta.fields
        for f in flds:
            fields_dict[f.attname] = {'verbose_name': f.verbose_name, 'column': f.column, 'choices': f.choices,
                                      'type': type(f), 'related_model': f.related_model}

        return fields_dict

    def _field_info(self, field):
        '''
        获取单个字段的信息
        :param field:
        :return:
        '''
        field_dict = self._model_fields()
        split_field = field.split('__')
        this_model_dict = field_dict  # 字段集
        this_dict_field = {}
        this_field_model = self.Model  # 字段所在model
        this_model = this_field_model  # 获取外键所在model
        for i in split_field:
            try:
                this_dict_field = this_model_dict[i]  # 获取字段信息
            except:
                this_dict_field = this_model_dict[i + '_id']
            this_field_model = this_model  # 获取当前字段所在的model
            this_model = this_dict_field.get('related_model')  # 获取其外键表
            if this_dict_field.get('related_model'):  # 如果存在，获取外键的字段集
                this_model_dict = self._model_fields(
                    model=this_model)  # this_dict_field = this_model_dict[split_field[i+1]]
        this_dict_field['model'] = this_field_model
        return this_dict_field

    @classmethod
    def get_fields_assemble(cls, fields):
        '''
        获取字段值的集合,用于筛选所需数据中，但只能获取本表中字段的数据
        :param fields: 需要获取的字段[]
        :return:
        '''
        field_dict = cls._model_fields(cls)
        fields_assemble = {}
        for field in fields:
            # 将__拆解
            split_field = field.split('__')
            this_model_dict = field_dict  # 字段集
            this_dict_field = {}
            this_field_model = cls.Model  # 字段所在model
            this_model = this_field_model  # 获取外键所在model
            for i in split_field:
                try:
                    this_dict_field = this_model_dict[i]  # 获取字段信息
                except:
                    this_dict_field = this_model_dict[i + '_id']
                this_field_model = this_model  # 获取当前字段所在的model
                this_model = this_dict_field.get('related_model')  # 获取其外键表
                if this_dict_field.get('related_model'):  # 如果存在，获取外键的字段集
                    this_model_dict = cls._model_fields(cls,
                                                        this_model)  # this_dict_field = this_model_dict[split_field[i+1]]
            if this_dict_field['choices']:
                fields_assemble[field] = {'name': this_dict_field['verbose_name'], 'type': 1,
                                          'value': choice_to_dict(this_dict_field['choices'])}
            # 日期时间
            elif this_dict_field['type'] == DateTimeField:
                fields_assemble[field + '_min'] = {'name': this_dict_field['verbose_name'] + '开始', 'type': 2,
                                                   'value': {}}
                fields_assemble[field + '_max'] = {'name': this_dict_field['verbose_name'] + '结束', 'type': 2,
                                                   'value': {}}  # 日期字段
            elif this_dict_field['type'] == DateField:
                fields_assemble[field + '_min'] = {'name': this_dict_field['verbose_name'] + '开始', 'type': 3,
                                                   'value': {}}
                fields_assemble[field + '_max'] = {'name': this_dict_field['verbose_name'] + '结束', 'type': 3,
                                                   'value': {}}

            #     int
            elif this_dict_field['type'] == IntegerField:
                fields_assemble[field] = {'name': this_dict_field['verbose_name'], 'type': 4,
                                          'value': {'step': 1, 'min': 0}}
            #     小数
            elif this_dict_field['type'] == FloatField or this_dict_field['type'] == DecimalField:
                fields_assemble[field] = {'name': this_dict_field['verbose_name'], 'type': 4,
                                          'value': {'step': 0.01, 'min': 0}}
            else:
                fields_assemble[field] = {'name': this_dict_field['verbose_name'], 'type': 0,
                                          'value': get_screen_data(this_dict_field['column'],
                                                                   this_field_model._meta.db_table)}
        return fields_assemble

    @classmethod
    def get_foreign_fields(cls, f_field=('pk', 'code', 'name'), without=None, only=None, where=None):
        '''
        获取所有外键字段，对应集合
        :param f_field: 外键对应模型中的要获取的字段
        :param without:要排除的字段，如果设有only，此值无效
        :param only:仅需要获取的字段，
        :param where:筛选条件
        :return: {'字段名':[{'外键字段名1'：值，'外键字段名2'：值...},...],...}

        '''
        if not without:
            without = []
        if not where:
            where = {}
        model_fields = cls._model_fields(cls)
        foreign_fields = {}
        if only:
            for field in only:
                m_field = model_fields[field]
                foreeign_model = m_field['related_model']
                foreign_fields[field] = foreeign_model.objects.filter(df=0, **where).values(*f_field)
        else:
            for k, field in model_fields.items():
                if field['related_model'] and not k in without:
                    foreeign_model = field['related_model']
                    foreign_fields[k] = foreeign_model.objects.filter(df=0, **where).values(*f_field)
        # print(foreign_fields)
        return foreign_fields

    def choice_to_value(self, query=None):
        '''
        将choice项换成（int，value）
        :param query: 要替换的query，单个query
        :return:
        '''
        choice_dict = {}
        model_fields = self._model_fields(self)
        for k, field in model_fields.items():
            if field['choices']:
                field_choice_dict = choice_to_dict(field['choices'])
                if query:
                    field_int_choice = getattr(query, k)
                    setattr(query, k, (field_int_choice, field_choice_dict.get(field_int_choice)))
                else:
                    choice_dict[k] = field_choice_dict
        if query:
            return query
        else:

            return choice_dict

    # list视图
    @classmethod
    def to_view(cls, request):
        pk, name, permission_table = parse_api_url(request.path)
        if not permission(request, permission_table, 1):
            return forbidden_view()
        context = {}
        context['js_path'] = os.path.join(cls.js_path(cls), cls.default_view_js)
        context['request'] = request
        if permission(request, permission_table, 2):
            context['create_permission'] = True
        if permission(request, permission_table, 3):
            context['update_permission'] = True
        if permission(request, permission_table, 4):
            context['delete_permission'] = True
        context = cls.get_view_context(cls, context)
        return render(request, os.path.join(cls.templaters_path, cls.default_view), context)

    @classmethod
    def api_view(cls, request):
        pk, name, permission_table = parse_extra_url(request.path)
        if not permission(request, permission_table, 1):
            return forbidden_view()
        # 获取前端传过来的GET数据
        get_data = request.GET
        # 页码
        page = get_data.get(PAGE_FIELD_NAME) or 1
        # 每页数据
        page_size = get_data.get(PAGE_SIZE_FILED_NAME) or PAGE_SIZE
        # 搜索项
        search = get_data.get(SEARCH_FIELD_NAME)
        # 排序
        order = get_data.get(ORDER_FIELD_NAME) or 'id'
        # 分页

        # 获取数据
        query_set = cls.Model.objects.all()
        # 自定义筛选条件
        query_set = cls.view_queryset(cls, query_set)
        #   前端传过来的筛选条件
        screen_data = cls.get_screen_context(cls, {})
        # 应用的筛选项
        effective_screen = {}
        for screen_field in screen_data:
            if get_data.get(screen_field):
                effective_screen[screen_field] = get_data[screen_field]
        # 筛选数据
        if effective_screen:
            query_set = query_set.filter(**effective_screen)
        #     搜索数据
        if search:
            query_set = cls.view_search(cls, query_set)
        #     排序
        query_set = query_set.order_by(order)
        query_set = cls.view_return_queryset(cls, query_set)
        paginator = Paginator(query_set,page_size)
        return JsonResponse({
            'count':paginator.count(),
            'page:':page,
            'code':200,
            'data':paginator.page(page)
        }, safe=False)

    def view_queryset(self, queryset):
        '''
        自定义筛选条件
        :param queryset:
        :return:
        '''
        return queryset.filter(df=0)

    def view_return_queryset(self, queryset):
        '''
        在返回response之前处理queryset
        :param queryset:
        :return:
        '''
        return queryset

    def view_search(self, queryset):
        '''
        搜索处理
        :param queryset:
        :return:
        '''
        return queryset

    # 创建视图
    @classmethod
    def to_create_frame(cls, request, id=None):
        pk, name, permission_table = parse_extra_url(request.path)
        if not permission(request, permission_table, 2):
            return forbidden_view()
        context = cls.choice_to_value(cls)
        tmpl_data = {}
        if id:
            try:
                # 有参照数据时，加载参照数据
                tmpl_data = cls.Model.objects.get(pk=id, df=0)
            except:
                tmpl_data = {}
        context['tmpl'] = tmpl_data
        context['js_path'] = os.path.join(cls.js_path(cls), cls.default_createframe_js)
        context['request'] = request
        context = cls.get_create_context(cls, context)
        return render(request, os.path.join(cls.templaters_path, cls.default_createframe), context)

    @classmethod
    def api_create(cls, request):
        create_fields = cls.create_fields
        fields_data =  request.POST
        fields_data = cls.create_fields_data(cls,fields_data)
        create_Data = {}
        for field in fields_data:
            if field in create_fields:
                create_Data[field] = fields_data[field]

        try:
            instance = cls.perform_create(cls,create_Data)
            return JsonResponse({'code':200,'instace':instance},safe=False)
        except Exception as e:
            return JsonResponse({'code':0,'err':e})

    def create_fields_data(self,data):
        return data

    def perform_create(self, data):
        return self.Meta.model.objects.create(**data)

    # 详情视图
    @classmethod
    def to_retrieve(cls, request, id):
        url_type, _ = parse_extra_url(request.path, retrieve=True)
        if not permission(request, url_type[2], 1):
            return forbidden_view()
        context = {}
        data = cls.Model.objects.get(pk=id, df=0)
        data = cls.choice_to_value(cls, data)
        context['data'] = data
        context['request'] = request
        context = cls.get_retrieve_context(cls, context)
        return render(request, os.path.join(cls.templaters_path, cls.default_retrieve), context)

    def api_retrieve(self,request,id):
        instance = self.Model.object.filter(df=0,id=id)
        if instance:
            instance = instance[0]
            return JsonResponse({'code':200,'data':instance},safe=False)
        else:
            return JsonResponse({'code':0,'err':'此id不存在:'+str(id)})

    # 修改视图
    @classmethod
    def to_update_frame(cls, request, id):
        url_type, _ = parse_extra_url(request.path, retrieve=True)
        if not permission(request, url_type[2], 3):
            return forbidden_view()
        context = cls.choice_to_value(cls)
        data = cls.Model.objects.get(pk=id, df=0)
        context['data'] = data
        context['js_path'] = os.path.join(cls.js_path(cls), cls.default_updateframe_js)
        context['request'] = request
        context = cls.get_update_context(cls, context)
        return render(request, os.path.join(cls.templaters_path, cls.default_updateframe), context)

    @classmethod
    def api_update(cls,request,id):
        instance = cls.Model.objects.filter(df=0,id=id)
        if instance:
            instance = instance[0]
        else:
            return JsonResponse({'code':0,'err':'次ID不存在:'+str(id)})
        update_fields = cls.update_fields
        fields_data = request.POST
        fields_data = cls.update_fields_data(cls, fields_data)
        update_data = {}
        for field in fields_data:
            if field in update_fields:
                update_data[field] = fields_data[field]
        try:
            instance = cls.perform_update(cls,instance,update_data)
            return JsonResponse({'code':200,'instace':instance},safe=False)
        except Exception as e:
            return JsonResponse({'code':0,'err':e})

    def perform_update(self,instance,data):
        return instance.update(**data)

    def update_fields_data(self,data):
        return data
    @classmethod
    def api_delete(cls,id):
        instance = cls.Model.objects.filter(df=0,id=id)
        if instance:
            instance = instance[0]
            if cls.perform_delete(cls,instance):
                return JsonResponse({'code':200,})
        else:
            return JsonResponse({'code':0,'err':'此id不存在:'+str(id)})
    def perform_delete(self,instance):
        instance.df = 1
        instance.save()
        return True
    # 筛选数据
    @classmethod
    def get_screen_data(cls, request):
        pk, name, permission_table = parse_extra_url(request.path)
        if not permission(request, permission_table, 1):
            return forbidden_view()
        data = {}
        data = cls.get_screen_context(cls, data)
        return JsonResponse(data)

    # 获取字段集合
    @classmethod
    def get_fields(cls, request, field):
        pk, name, permission_table = parse_extra_url(request.path)
        if not permission(request, permission_table, 1):
            return JsonResponse({'err': '无权操作'})
        cls.validate_fields(cls, request)
        field_dict = cls._model_fields(cls)
        fieldlist = field.split(',')
        many = False
        if len(fieldlist) > 1:
            many = True
        # 没有允许的字段
        if field not in cls.fields:
            for f in fieldlist:
                if f not in field_dict:
                    return JsonResponse({'err': '请求不允许', }, status=403)

        # 不存在的字段
        if field not in field_dict:
            for f in fieldlist:
                if f not in field_dict:
                    return JsonResponse({'err': '请求的字段不存在' + f}, status=403)
            where = request.GET  # 获取筛选项，即where条件
            data = get_screen_data(field, cls.Model._meta.db_table, where=where, many=True)
            return JsonResponse(data, safe=False)
        this_dict_field = field_dict[field]
        # dict字段
        if this_dict_field['choices']:
            return JsonResponse(choice_to_dict(this_dict_field['choices']))
        # 日期时间
        if this_dict_field['type'] == DateTimeField:
            return JsonResponse({'type': 'DateTimeField'})
        # 日期字段
        if this_dict_field['type'] == DateField:
            return JsonResponse({'type': 'DateField'})
        where = request.GET  # 获取筛选项，即where条件
        for key, value in where.items():
            print(key, value)
        data = get_screen_data(this_dict_field['column'], cls.Model._meta.db_table, where=where)
        return JsonResponse(data, safe=False)

    def register_router(self, regular, func):
        self.router_pool.append(url(regular, func))

    def new_router(self):
        pass

    def validate_fields(self, request):
        '''
        作为获取字段合集的验证函数
        :param request:
        :return:
        '''
        pass

    @classmethod
    def router(cls):
        cls.new_router(cls)
        urlpatterns = [url(r'^view/(.+?)/$', cls.to_retrieve),
                       url(r'^view/$', cls.to_view),
                       url(r'^createframe/?(.*?)/$', cls.to_create_frame),
                       url(r'^updateframe/(.+?)/$', cls.to_update_frame),
                       url(r'^screen.json/$', cls.get_screen_data),
                       url(r'^field/(.+?)/$', cls.get_fields),
                       url(r'^api/view/$',cls.api_view),
                       url(r'^api/create/$',cls.api_create),
                       url(r'^api/update/(\d+)/',cls.api_update),
                       url(r'api/retrieve/(\d+)/',cls.api_retrieve),
                       url(r'api/delete/(\d+)/', cls.api_delete)

                       ]
        return urlpatterns + cls.router_pool

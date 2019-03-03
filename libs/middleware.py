from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from siding.settings import TOKEN_NAME
from libs.token_cache import get_token
from libs.printf import print_debug as print


class SimpleMiddleware(MiddlewareMixin):
    # 请求
    def process_request(self, request):
        # print(request.META)
        # print(request.COOKIES)
        url = request.get_raw_uri()
        # 不对登录的url做任何限制
        if url.endswith(".js") or url.endswith(".css") or url.endswith(".png") or url.endswith(".jpg"):
            return None  # 放行
        if url.endswith("/login/") or url.endswith("/toLogin") or url.endswith("/system/login/"):
            return None  # 放行
        # 先判断是否header中带有tokenid，如果没有，则看cookie中
        if request.META.get('HTTP_' + TOKEN_NAME):
            token_id = request.META.get('HTTP_' + TOKEN_NAME)
        else:
            token_id = request.COOKIES.get('TOKEN')  # print(request.COOKIES)
        # print(token_id)
        if token_id:
            # 判断token是否有效
            token = get_token(token_id)
            # print(token)
            if token:
                # 设置token，及tokenid
                request.META['TOKEN'] = token
                request.META['TOKEN_ID'] = token_id
                # print(token_id, '通过验证')
                return None
        # print('请求')
        return render(request, 'login.html', {})

    # 响应
    def process_response(self, request, response):
        # 刷新token的时间
        token_id = request.META.get('TOKEN_ID')
        # print(token_id, '响应')
        if token_id:
            response.set_cookie('TOKEN', token_id, 60 * 20, path='/')
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST,DELETE,PUT,PATCH,GET'
        response['Access-Control-Max-Age'] = '1000'
        response['Access-Control-Allow-Headers'] = '*'
        # print('resp',token_id)
        return response

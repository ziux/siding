from django.core.cache import cache
from libs.constant_pool import TOKEN_TIMEOUT
from system.models import Token
import hashlib
import secrets
import pickle
import datetime


class ttoken:

    def add(self, token_id, content, timeout):
        bin_content = pickle.dumps(content)
        time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        Token.objects.create(token=token_id, value=bin_content, expiration=time)
        return True

    def delete(self, token_id):
        Token.objects.filter(token=token_id).delete()
        clear_timeout_token()
        return True

    def get(self, token_id):
        token = Token.objects.filter(token=token_id)
        now_time = datetime.datetime.now()
        if token:
            token = token[0]
            if token.expiration > now_time:
                return pickle.loads(token.value)
            else:
                token.delete()
        return None

    def touch(self, token_id, timeout):
        token = Token.objects.filter(token=token_id)
        now_time = datetime.datetime.now()
        if token:
            token = token[0]
            token.expiration = now_time + datetime.timedelta(seconds=timeout)
            token.save()
            return True
        return False


MD5_WORD = 'sDdFaD.h,h&kv*dDdFdsdEwFaS'
TOKEN_TYPE_SPACE = ttoken()


def create_token(content):
    token_id = build_token_id()
    if TOKEN_TYPE_SPACE.add(token_id, content, TOKEN_TIMEOUT):
        return token_id


def get_token(token_id):
    token = TOKEN_TYPE_SPACE.get(token_id)
    if token:
        TOKEN_TYPE_SPACE.touch(token_id, TOKEN_TIMEOUT)
    return token


def del_token(token_id):
    TOKEN_TYPE_SPACE.delete(token_id)
    return True


hash = hashlib.md5(bytes(MD5_WORD, encoding='utf-8'))


def build_token_id():
    hash.update(secrets.token_bytes(32))
    return hash.hexdigest()


def clear_timeout_token():
    for token in Token.objects.all():
        if token.expiration < datetime.datetime.now():
            token.delete()
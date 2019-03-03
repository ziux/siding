import inspect
import datetime
import os
from siding.settings import BASE_DIR
log_path  = os.path.join(BASE_DIR,'debug_logs')
max_buffer_log = 0


def write_log(log,filename):
    date = str(datetime.date.today())
    log_date_path = os.path.join(log_path,date)
    if not os.path.exists(log_date_path):
        os.makedirs(log_date_path)
    file_name = filename + '_log.txt'
    log_file = os.path.join(log_date_path, file_name)
    with open(log_file, 'a+') as f:
        f.write(log+'\n')


def print_debug(*args):
    stack = inspect.stack()
    stack = stack[1]
    log = ' '.join(('[DEBUG ',get_time(),']: ',*strlst(args),'   --<!',stack.function,stack.filename,str(stack.lineno),'!>--'))
    write_log(log,'debug')
    print(log)


def print_info(*args):
    stack = inspect.stack()
    stack = stack[1]
    log = ' '.join(
        ('[INFO  ',get_time(),']: ', *strlst(args),'   --<!',stack.function,stack.filename,str(stack.lineno),'!>--' ))
    write_log(log,'info')
    print(log)


def print_error(*args):
    stack = inspect.stack()
    stack = stack[1]
    log = ' '.join(
        ('[ERROE ',get_time(),']: ', *strlst(args), '   --<!',stack.function,stack.filename,str(stack.lineno),'!>--'))
    write_log(log,'error')
    print(log)


def print_warning(*args):
    stack = inspect.stack()
    stack = stack[1]
    log = ' '.join(
        ('[WARNING ',get_time(),']: ', *strlst(args),'   --<!',stack.function,stack.filename,str(stack.lineno),'!>--'))
    write_log(log,'warning')
    print(log)

def get_time():
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(date)

def strlst(lst):
    return [ str(i) for i in lst]


if __name__ == '__main__':
    print(get_time())
    print_debug('test')
    print_debug('gggg')
    print_error('sdsd')
    print_info('ggg')

import hashlib

def get_md5(*args):
    '''
    参数必须是字符串，不然返回None
    '''
    m = hashlib.md5()
    for arg in args:
        if not isinstance(arg, str):
            return None
        m.update(arg.encode('utf-8'))
    return m.hexdigest()

def get_sha1(*args):
    pass
    # print([x for x in args])

if __name__ == "__main__":
    pass
    a = ['a']
    print(get_md5('2'))
    print(get_md5(2))
    print(get_md5(a))
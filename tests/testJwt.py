def test_jst():
    import jwt
    import time
    from jwt import exceptions
    headers = {
    "alg": "HS256",
    "typ": "JWT"
    }
    # 设置headers，即加密算法的配置
    salt = "asgfdgerher"
    # 随机的salt密钥，
    exp = int(time.time() + 1)
    # 设置超时时间：当前时间的1s以后超时
    payload = {
    "name": "dawsonenjoy",
    "exp": exp
    }
    # 配置主体信息

    token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers).decode('utf-8')
    # 生成token
    print(token)

    info = jwt.decode(token, salt, True, algorithm='HS256')
    # 解码token，第二个参数用于校验
    # 第三个参数代表是否校验，如果设置为False，那么只要有token，就能够对其进行解码
    print(info)

    time.sleep(2)
    # 等待2s后再次验证token，因超时将导致验证失败
    try:
        info = jwt.decode(token, salt, True, algorithm='HS256')
        print(info)
    except exceptions.ExpiredSignatureError:
        print('token已失效')
    except jwt.DecodeError:
        print('token认证失败')
    except jwt.InvalidTokenError:
        print('非法的token')

    info = jwt.decode(token, '', False, algorithm='HS256')
    # 第三个参数设置为False，不进行校验，直接解码token
    print(info)

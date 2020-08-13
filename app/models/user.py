class User:
    '''
    用户信息
    seqied: 主键,自增
    phone_number: 注册电话号码 not null
    email: 邮箱 
    password: 密码 not null
    nickname: 昵称 not null
    sex: 性别
    relationships: 关联好友的seqid
    register_time: 注册时间(datetime) not null
    token: token
    '''
    seqid = ''
    phone_number = ''
    email = ''
    password = ''
    nickname = ''
    sex = ''
    relationships = ''
    register_time = ''
    token = ''

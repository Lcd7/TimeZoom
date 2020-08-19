class RelationUsers:
    '''
    用户好友关系表
    seqid: 主键,自增
    userid: 用户的seqid     not null
    friendid: 好友的seqid   not null
    isReceive: 是否接受  布尔值
    '''
    seqid = ''
    userid = ''
    friendid = ''
    isReceive = ''
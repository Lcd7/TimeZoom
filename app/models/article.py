class Article:
    '''
    已发表动态信息
    seqid: 自增主键
    text: 内容 not null
    relation_user_id: 评论 关联用户表的seqid
    is_public: 是否公开，默认否
    likes: 点赞数
    do_time: 上传时间
    '''
    seqid = ''
    text = ''
    is_public = False
    likes = 0
    relation_user_id = -1
    do_time = ''
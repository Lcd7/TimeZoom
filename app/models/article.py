class Article:
    '''
    已发表动态信息
    seqid: 自增主键
    text: 内容 not null
    relationUserId: 评论 关联用户表的seqid
    isPublic: 是否公开，默认否
    likes: 点赞数
    comments: 评论数
    doTime: 上传时间
    '''
    seqid = ''
    text = ''
    isPublic = False
    likes = 0
    likesNum = 0
    relationUserId = -1
    comments = ''
    doTime = ''
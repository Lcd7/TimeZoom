class TComment:
    '''
    评论表
    seqid: 评论id
    text: 正文
    is_public: 是否公开
    relationArticlesId: 外键约束 发表动态信息
    '''
    seqid = ''
    text = ''
    isPublic = ''
    relationArticlesId = ''
    doTime = ''
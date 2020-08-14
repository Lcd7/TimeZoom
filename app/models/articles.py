class Article:
    '''
    已发表动态信息
    content: 内容 not null
    relation_id: 评论 关联评论表的seqid
    is_public: 是否公开，默认否
    like: 点赞数
    '''
    seqid = ''
    content = ''
    is_public = False
    like = 0
    relation_id = -1
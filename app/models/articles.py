class Article:
    '''
    已发表文章信息
    content: 内容 not null
    comments: 评论 关联评论表的seqid
    is_public: 是否公开，默认否
    like: 点赞数
    '''
    seqid = ''
    content = ''
    comments = ''
    is_public = False
    like = 0
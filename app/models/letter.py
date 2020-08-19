class Letter:
    '''
    私信内容
    seqid : 留言主键字段，自增长
    user : 留言的主人的seqid, not null
    friend : 对方的ID, not null
    sender : 留言发送者ID, not null
    receiver : 留言接收者ID, not null
    msgType : 留言类型(普通消息1、系统消息0), not null
    content : 留言内容, not null
    sendTime : 发送时间, datetime, not null
    readTime : 阅读时间, datetime, not null
    status : 留言状态(未读0，已读1), not null
    '''
    seqid = ''
    userid = ''
    friendid = ''
    senderid = ''
    receiverid = ''
    msgType = ''
    content = ''
    sendTime = ''
    readTime = ''
    status = 0
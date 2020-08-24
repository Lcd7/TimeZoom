'''
图片类
包括验证码和用户上传的图片
'''
class Img:
    '''
    imgName: 图片名    not null    
    headPic: 七牛服务器该图片的链接 not null
    picValue: 验证码图片的值
    imgType: 图片的类型（2用户头像，1用户动态，0系统） not null
    imgUser: 图片所属的用户seqid
    imgArticle: 图片所属的文章seqid
    '''
    seqid = ''
    imgName = ''
    headPic = ''
    picValue = ''
    imgType = ''
    imgUser = ''
    imgArticle = ''
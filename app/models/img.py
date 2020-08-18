'''
图片类
包括验证码和用户上传的图片
'''
class Imgs:
    '''
    img_name: 图片名    not null    
    head_pic: 七牛服务器该图片的链接 not null
    pic_value: 验证码图片的值
    img_type: 图片的类型（1用户，0系统） not null
    img_user: 图片所属的用户seqid
    img_comment: 图片所属的文章seqid
    '''
    seqid = ''
    img_name = ''
    head_pic = ''
    pic_value = ''
    img_type = ''
    img_user = ''
    img_comment = ''
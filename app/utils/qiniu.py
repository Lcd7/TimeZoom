'''
七牛云服务器图片上传下载
'''
from qiniu import Auth, put_file
import requests

class QiNiuImage:
    '''
    bucketName: 七牛空间名称
    accessKey: AK密钥
    secretKey: SK密钥
    '''
    # 七牛
    qiniuBaseUrl = 'qf9fy6urv.hn-bkt.clouddn.com'

    def __init__(self, bucketName, accessKey, secretKey):
        self.bucketName = bucketName
        self.accessKey = accessKey
        self.secretKey = secretKey

    def upload_image(self, imgName, imgPath):
        '''
        imgName: 上传图片文件名
        imgPath: 上传图片文件路径
        '''
        q = Auth(self.accessKey, self.secretKey)
        token = q.upload_token(self.bucketName, imgName)
        ret, info = put_file(token, imgName, imgPath)
        if info.status_code == 200:
            return self.qiniuBaseUrl + ret.get('key')
        else:
            return False

    def download_image(self, url):
        response = requests.get(url)
        return response

if __name__ == "__main__":
    pass
    # Q = QiNiuImage('lcdimg', 'khVENkO1bITYxmXsqGY0aqCuEZSNx0dXYHUMpgWn', 'owB5tbJmCyjLwnXWJ1VZmnROYsiOyndKxk-ivA0w')
    # # 上传
    # _path = Q.upload_image('测试.png', 'C:/Users/user/Desktop/测试.png')
    # print(_path)

    # #下载
    # response = Q.download_image('http://qf9fy6urv.hn-bkt.clouddn.com/测试.png')
    # img = response.content
    # with open('C:/Users/user/Desktop/测试111.png', 'wb') as f:
        # f.write(img)


    # # url转码
    # from urllib.parse import quote, unquote

    # strs = 'http://qf9fy6urv.hn-bkt.clouddn.com/%E6%B5%8B%E8%AF%95.png'
    # str1 = unquote(strs)
    # print(str1)
    # str2 = quote(str1)
    # print(str2)

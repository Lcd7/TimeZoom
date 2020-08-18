'''
七牛云服务器图片上传下载
'''
from qiniu import Auth, put_file
import requests

class QiNiuImage:
    '''
    bucket_name: 七牛空间名称
    sccess_key: AK密钥
    secret_key: SK密钥
    '''
    # 七牛
    qiniu_base_url = ''

    def __init__(self, bucket_name, access_key, secret_key):
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key

    def upload_image(self, img_name, img_path):
        '''
        img_name: 上传图片文件名
        img_path: 上传图片文件路径
        '''
        q = Auth(self.access_key, self.secret_key)
        token = q.upload_token(self.bucket_name, img_name)
        _, info = put_file(token, img_name, img_path)
        if info.status_code == 200:
            return True
        else:
            return False

    def download_image(self, url):
        response = requests.get(url)
        return response
'''
请求测试脚本
'''
import requests
from Crypto.Cipher import AES
import base64
import datetime
import time

class Aescrypt():
    '''
    密钥（KEY）, 密斯偏移量（IV） CBC模式加密
    '''
    BLOCK_SIZE = 16  # Bytes
    IV = '0102030405060708'
    KEY = 'lcd12345fp123456'

    def __init__(self, model):
        self.model = model

    def pad(self, data):
        data = data + (self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE) * \
                chr(self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE)
        return data
    
    def unpad(self, data):
        return data[:-ord(data[len(data) - 1:])]

    def AES_Encrypt(self, data):
        # 字符串补位
        data = self.pad(data)
        
        if self.model == AES.MODE_CBC:
            cipher = AES.new(self.KEY.encode('utf8'), self.model, self.IV.encode('utf8'))
        elif self.model == AES.MODE_ECB:
            cipher = AES.new(self.KEY.encode('utf8'), self.model)

        encryptedbytes = cipher.encrypt(data.encode('utf8'))

        # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
        encodestrs = base64.b64encode(encryptedbytes)

        # 对byte字符串按utf-8进行解码
        enctext = encodestrs.decode('utf8')
        print(enctext)
        return enctext


    def AES_Decrypt(self, data):
        data = data.encode('utf8')
        encodebytes = base64.decodebytes(data)

        # 将加密数据转换位bytes类型数据
        if self.model == AES.MODE_CBC:
            cipher = AES.new(self.KEY.encode('utf8'), self.model, self.IV.encode('utf8'))
        elif self.model == AES.MODE_ECB:
            cipher = AES.new(self.KEY.encode('utf8'), self.model)

        text_decrypted = cipher.decrypt(encodebytes)

        # 去补位
        text_decrypted = self.unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        print(text_decrypted)
        return text_decrypted

def login_test():
    url = 'http://127.0.0.1:8058/index/register'
    aescryptor = Aescrypt(AES.MODE_CBC) # CBC模式

    phone_number = '15182696451'
    email = '1102217785@qq.com'
    nickname = '被李子吃了吗'
    sex = '男'
    timenow = str(int(time.time()))
    passw = 'Soda.123'
    passw = aescryptor.AES_Encrypt(passw)
    sign = aescryptor.AES_Encrypt(phone_number[:3] + timenow[:3] + passw)

    # 解密sign
    dec_text = aescryptor.AES_Decrypt(sign)
    dec_text = dec_text[6:]
    aescryptor.AES_Decrypt(dec_text)

    params = {
        'phone_number': phone_number,
        'password': passw,
        'email': email,
        'nickname': nickname,
        'sex': sex,
        'register_time': str(datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))[:-3],
        'timenow': timenow,
        'sign':sign
    }
    print(params)
    # print(requests.post(url, params))

if __name__ == "__main__":
    login_test()
from Crypto.Cipher import AES
import base64
from flask import current_app

class Aescrypt():
    '''
    密钥（KEY）, 密斯偏移量（IV） CBC模式加密
    '''
    BLOCK_SIZE = 16  # Bytes
    # IV = current_app.config['IV']
    # KEY = current_app.config['AES_KEY']

    def __init__(self, MODEL, AES_KEY, IV):
        self.MODEL = MODEL
        self.AES_KEY = AES_KEY
        self.IV = IV

    def pad(self, data):
        data = data + (self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE) * \
                chr(self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE)
        return data
    
    def unpad(self, data):
        return data[:-ord(data[len(data) - 1:])]

    def AES_Encrypt(self, data):
        # 字符串补位
        data = self.pad(data)
        
        if self.MODEL == AES.MODE_CBC:
            cipher = AES.new(self.AES_KEY.encode('utf8'), self.MODEL, self.IV.encode('utf8'))
        elif self.MODEL == AES.MODE_ECB:
            cipher = AES.new(self.AES_KEY.encode('utf8'), self.MODEL)

        encryptedbytes = cipher.encrypt(data.encode('utf8'))

        # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
        encodestrs = base64.b64encode(encryptedbytes)

        # 对byte字符串按utf-8进行解码
        enctext = encodestrs.decode('utf8')
        # print(enctext)
        return enctext


    def AES_Decrypt(self, data):
        data = data.encode('utf8')
        encodebytes = base64.decodebytes(data)

        # 将加密数据转换位bytes类型数据
        if self.MODEL == AES.MODE_CBC:
            cipher = AES.new(self.AES_KEY.encode('utf8'), self.MODEL, self.IV.encode('utf8'))
        elif self.MODEL == AES.MODE_ECB:
            cipher = AES.new(self.AES_KEY.encode('utf8'), self.MODEL)

        text_decrypted = cipher.decrypt(encodebytes)

        # 去补位
        text_decrypted = self.unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        # print(text_decrypted)
        return text_decrypted
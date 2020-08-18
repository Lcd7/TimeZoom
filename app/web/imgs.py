from app.web import blue_index, check_token, retMsg, parser
from app.utils.qiniu import QiNiuImage
from app.libs import tableImg, tableArticle
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource

api = Api(blue_index)

class pictures(Resource):

    bucket_name = current_app.config['BUCKET']
    access_key = current_app.config['AK']
    secret_key = current_app.config['SK']

    @check_token
    def get(self):
        pass

    @check_token
    def post(self):
        '''
        提交图片数据
        '''
        pass
            
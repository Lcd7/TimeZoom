from app.web import blue_index, check_token, retMsg, parser
from app.utils.qiniu import QiNiuImage
from app.libs import tableImg, tableArticle
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource

api = Api(blue_index)


class updateArticle(Resource):

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
        Q = QiNiuImage(self.bucket_name, self.access_key, self.secret_key)
        _res_upload = Q.upload_image(g.img_name, g.img_path)
        if _res_upload:
            # 保存动态 获取评论seqid
            _tmp_art_id = tableArticle.insert_art(g.art_text, g.user.seqid)
            head_pic = '七牛云路径' + g.img_name
            # 保存图片
            tableImg.insert_img(g.img_name, head_pic, g.user.seqid, _tmp_art_id)


            retMsg['code'] = 1
            retMsg['msg'] = '上传成功'
        else:
            retMsg['msg'] = '上传失败'
        
        return jsonify(retMsg)
from app.web import web_index, check_token, retMsg, parser
from app.utils.qiNiu import QiNiuImage
from app.libs import tableImg, tableArticle
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource

api = Api(web_index)


class getUpdateArticle(Resource):

    @check_token
    def get(self):
        '''
        获取动态 和 删除动态
        return 点赞数 评论数
        '''
        status = request.args.get('status', 1)
        # 获取
        if status == 1:
            if g.art_user_id:
                _res = tableArticle.get_user_all_arts(g.art_user_id)
                if _res:
                    retMsg['code'] = 1
                    retMsg['data'] = _res
                else:
                    retMsg['msg'] = '动态获取失败'

            elif g.art_seqid:
                _res = tableArticle.get_user_one_art(g.art_seqid)
                if _res:
                    retMsg['code'] = 1
                    retMsg['data'] = _res
                else:
                    retMsg['msg'] = '动态获取失败'
        # 删除
        else:
            if g.art_seqid:
                _res = tableArticle.delete_art(g.art_seqid)
                if not _res:
                    retMsg['msg'] = '动态删除失败'

        return jsonify(retMsg)

    @check_token
    def post(self):
        '''
        发布动态
        '''

        if g.art_text:
            # 保存动态 获取评论seqid
            _tmp_art_id = tableArticle.insert_art(g.art_text, g.user.seqid)

            # 上传图片
            if _tmp_art_id and g.img_name:
                Q = QiNiuImage(current_app.config['BUCKET'], current_app.config['AK'], current_app.config['SK'])
                _res_upload = Q.upload_image(g.img_name, g.img_path)

                # 保存图片链接
                if _res_upload:
                    head_pic = '七牛云路径' + g.img_name
                    _res = tableImg.insert_img(g.img_name, head_pic, g.user.seqid, img_comment = _tmp_art_id)
                    if not _res:
                        retMsg['msg'] = '动态上传失败'
            
            elif not _tmp_art_id:
                retMsg['msg'] = '动态上传失败'
            
            retMsg['code'] = 1
            retMsg['msg'] = '动态上传成功'
        else:
            retMsg['msg'] = '动态上传失败'
        
        return jsonify(retMsg)

class getLikes(Resource):
    '''
    点赞
    '''
    def get(self):
        artid = request.args.get('artid')
        # 是否点过赞
        if not tableArticle.select_likes(g.user.seqid, artid):
            _resLike = tableArticle.like_art(g.user.seqid, artid)
            if _resLike:
                retMsg['code'] = 1
            else:
                retMsg['msg'] = '点赞失败'
                return jsonify(retMsg)
        else:
            retMsg['code'] = 1

        return jsonify(retMsg)

api.add_resource(getUpdateArticle, '/Article/get', '/Article/delete', 'Article/update', endpoint = 'getUpdateArticle')
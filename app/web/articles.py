from app.web import webIndex, check_token, retMsg, parser
from app.utils.qiNiu import QiNiuImage
from app.libs import TableImg, TableArticle
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource

api = Api(webIndex)


class GetUpdateArticle(Resource):

    @check_token
    def get(self):
        '''
        获取动态 和 删除动态
        return 点赞数 评论数
        '''
        status = request.args.get('status', 1)
        # 获取
        if status == 1:
            if g.artUserId:
                _tmpRes = TableArticle.get_user_all_arts(g.artUserId)
                if _tmpRes:
                    retMsg['code'] = 1
                    retMsg['data'] = _tmpRes
                else:
                    retMsg['msg'] = '动态获取失败'

            elif g.artSeqid:
                _tmpRes = TableArticle.get_user_one_art(g.artSeqid)
                if _tmpRes:
                    retMsg['code'] = 1
                    retMsg['data'] = _tmpRes
                else:
                    retMsg['msg'] = '动态获取失败'
        # 删除
        else:
            if g.artSeqid:
                _tmpRes = TableArticle.delete_art(g.artSeqid)
                if not _tmpRes:
                    retMsg['msg'] = '动态删除失败'

        return jsonify(retMsg)

    @check_token
    def post(self):
        '''
        发布动态
        '''

        if g.artText:
            # 保存动态 获取评论seqid
            _tmpArtId = TableArticle.insert_art(g.artText, g.user.seqid)

            # 上传图片
            if _tmpArtId and g.imgName:
                Q = QiNiuImage(current_app.config['BUCKET'], current_app.config['AK'], current_app.config['SK'])
                _tmpResUpload = Q.upload_image(g.imgName, g.imgPath)

                # 保存图片链接
                if _tmpResUpload:
                    headPic = '七牛云路径' + g.imgName
                    _tmpRes = TableImg.insert_img(g.imgName, headPic, g.user.seqid, imgComment = _tmpArtId)
                    if not _tmpRes:
                        retMsg['msg'] = '动态上传失败'
            
            elif not _tmpArtId:
                retMsg['msg'] = '动态上传失败'
            
            retMsg['code'] = 1
            retMsg['msg'] = '动态上传成功'
        else:
            retMsg['msg'] = '动态上传失败'
        
        return jsonify(retMsg)

class GetLikes(Resource):
    '''
    点赞
    '''
    @check_token
    def get(self):
        artid = request.args.get('artid')
        # 是否点过赞
        if not TableArticle.select_likes(g.user.seqid, artid):
            _tmpResLike = TableArticle.like_art(g.user.seqid, artid)
            if _tmpResLike:
                retMsg['code'] = 1
            else:
                retMsg['msg'] = '点赞失败'
        else:
            # 取消点赞
            _tmpResResetLike = TableArticle.reset_like_art(g.user.seqid, artid)
            if _tmpResResetLike:
                retMsg['code'] = 1
            else:
                retMsg['msg'] = '取消点赞失败'

        return jsonify(retMsg)

class SetPublicArt(Resource):
    '''
    设置动态公开效果
    '''
    @check_token
    def get(self):
        artid = request.args.get('artid')
        artStatus = request.args.get('artStatus')
        _tmpResSet = TableArticle.set_public_art(artid, artStatus)
        if _tmpResSet:
            retMsg['code'] = 1
        else:
            retMsg['msg'] = '动态状态设置失败'

        return jsonify(retMsg)


api.add_resource(GetUpdateArticle, '/Article/get', '/Article/delete', 'Article/update', endpoint = 'GetUpdateArticle')
api.add_resource(GetLikes, '/Article/like', endpoint = 'GetLikes')
api.add_resource(SetPublicArt, '/Article/set', endpoint = 'SetPublicArt')
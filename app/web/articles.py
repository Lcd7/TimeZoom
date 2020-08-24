from app.web import webIndex, check_token
from app.utils.qiNiu import QiNiuImage
from app.libs import TableImg, TableArticle
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource

api = Api(webIndex)


class GetUpdateArticle(Resource):
    @check_token
    def get(self):
        '''
        获取动态
        params: artUserId   获取用户所有动态
        params: artSeqid    获取单个动态
        '''
        # 获取
        if g.artUserId:
            _tmpRes = g.tableArticle.get_user_all_arts(g.artUserId)
            if _tmpRes:
                g.retMsg['code'] = 1
                g.retMsg['data'] = _tmpRes
            else:
                g.retMsg['msg'] = '动态获取失败'

        elif g.artSeqid:
            _tmpRes = g.tableArticle.get_user_one_art(g.artSeqid)
            if _tmpRes:
                g.retMsg['code'] = 1
                g.retMsg['data'] = _tmpRes
                # 获取评论数
            else:
                g.retMsg['msg'] = '动态获取失败'

        return jsonify(g.retMsg)

    @check_token
    def post(self):
        '''
        发布动态
        params: artText
        params: *imgName
        params: *imgPath
        '''
        if g.artText:
            # 保存动态 获取评论seqid
            _tmpArtId = g.tableArticle.insert_art(g.artText, g.user.seqid)

            # 上传图片
            if _tmpArtId and g.imgName:
                Q = QiNiuImage(current_app.config['BUCKET'], current_app.config['AK'], current_app.config['SK'])
                _tmpResUpload = Q.upload_image(g.imgName, g.imgPath)

                # 保存图片链接
                if _tmpResUpload:
                    headPic = current_app.config['QN_URL'] + g.imgName
                    _tmpRes = g.tableImg.insert_img(g.imgName, headPic, g.user.seqid, imgComment = _tmpArtId)
                    if not _tmpRes:
                        g.retMsg['msg'] = '动态上传失败'
            
            elif not _tmpArtId:
                g.retMsg['msg'] = '动态上传失败'
            
            g.retMsg['code'] = 1
            g.retMsg['msg'] = '动态上传成功'
        else:
            g.retMsg['msg'] = '动态上传失败'
        
        return jsonify(g.retMsg)

class DeleteArticle(Resource):
    '''
    删除动态
    params: artSeqid
    '''
    @check_token
    def post(self):
        if g.artSeqid:
            _tmpRes = g.tableArticle.delete_art(g.artSeqid)
            if not _tmpRes:
                g.retMsg['msg'] = '动态删除失败'

class GetLikes(Resource):
    '''
    点赞
    params: artSeqid
    '''
    @check_token
    def post(self):
        # 是否点过赞
        if not g.tableArticle.select_likes(g.user.seqid, g.artSeqid):
            _tmpResLike = g.tableArticle.like_art(g.user.seqid, g.artSeqid)
            if _tmpResLike:
                g.retMsg['code'] = 1
            else:
                g.retMsg['msg'] = '点赞失败'
        else:
            # 取消点赞
            _tmpResResetLike = g.tableArticle.reset_like_art(g.user.seqid, g.artSeqid)
            if _tmpResResetLike:
                g.retMsg['code'] = 1
            else:
                g.retMsg['msg'] = '取消点赞失败'

        return jsonify(g.retMsg)

class SetPublicArt(Resource):
    '''
    设置动态公开效果
    params: artStatus 01
    '''
    @check_token
    def post(self):
        artStatus = request.args.get('artStatus')
        _tmpResSet = g.tableArticle.set_public_art(g.artSeqid, artStatus)
        if _tmpResSet:
            g.retMsg['code'] = 1
        else:
            g.retMsg['msg'] = '动态状态设置失败'

        return jsonify(g.retMsg)


api.add_resource(GetUpdateArticle, '/Article/get', '/Article/delete', '/Article/update', endpoint = 'GetUpdateArticle')
api.add_resource(DeleteArticle, '/DeleteArticle', endpoint = 'DeleteArticle')
api.add_resource(GetLikes, '/Article/like', endpoint = 'GetLikes')
api.add_resource(SetPublicArt, '/Article/set', endpoint = 'SetPublicArt')
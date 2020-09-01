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
        params: artUserid   获取用户所有动态
        params: artSeqid    获取单个动态
        params: *isPublic    是否公开
        '''
        if not g.isPublic:
            if g.user.seqid != g.artUserid:
                g.isPublic = 1
            else:
                g.isPublic = 2

        # 获取
        if g.artUserid and not g.artSeqid:            
            _tmpRes = g.tableArticle.get_user_all_arts(g.artUserid, g.isPublic)
            if _tmpRes:
                g.retMsg['status'] = 1
                g.retMsg['data'] = _tmpRes
            elif isinstance(_tmpRes, str):
                g.retMsg['status'] = 1
                g.retMsg['msg'] = '暂无动态'
            else:
                g.retMsg['msg'] = '动态获取失败'

        elif g.artSeqid:
            _resDict = g.tableArticle.get_user_one_art(g.artSeqid, 2)
            if _resDict.get('relationUserId') == g.user.seqid:
                g.isPublic = 2
            _tmpRes = g.tableArticle.get_user_one_art(g.artSeqid, g.isPublic)
            if _tmpRes:
                g.retMsg['status'] = 1
                g.retMsg['msg'] = _tmpRes
                # 获取评论数
            else:
                g.retMsg['msg'] = '动态获取失败'

        return jsonify(g.retMsg)

    @check_token
    def post(self):
        '''
        发布动态
        params: artText
        params: *isPublic
        params: *imgName
        params: *imgPath
        '''
        if g.artText:
            # 保存动态 获取评论seqid
            if g.isPublic:
                _tmpArtId = g.tableArticle.insert_art(g.artText, g.user.seqid, g.isPublic)
            else:
                _tmpArtId = g.tableArticle.insert_art(g.artText, g.user.seqid)

            # 上传图片
            if _tmpArtId and g.imgName:
                Q = QiNiuImage(current_app.config['QN_BUCKET'], current_app.config['QN_AK'], current_app.config['QN_KEY'])
                _tmpResUpload = Q.upload_image(g.imgName, g.imgPath)

                # 保存图片链接
                if _tmpResUpload:
                    headPic = current_app.config['QN_URL'] + g.imgName
                    _tmpRes = g.tableImg.insert_img(g.imgName, headPic, g.user.seqid, imgArticle = _tmpArtId)
                    if not _tmpRes:
                        g.retMsg['msg'] = '动态上传失败'
            
            elif not _tmpArtId:
                g.retMsg['msg'] = '动态上传失败'
            
            g.retMsg['status'] = 1
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
        else:
            g.retMsg['msg'] = '无效动态id'
        return jsonify(g.retMsg)

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
                g.retMsg['status'] = 1
                g.retMsg['code'] = 200
            else:
                
                g.retMsg['msg'] = '点赞失败'
        else:
            # 取消点赞
            _tmpResResetLike = g.tableArticle.reset_like_art(g.user.seqid, g.artSeqid)
            if _tmpResResetLike:
                g.retMsg['status'] = 1
                g.retMsg['code'] = 200
            else:
                
                g.retMsg['msg'] = '取消点赞失败'

        return jsonify(g.retMsg)

class SetPublicArt(Resource):
    '''
    设置动态公开效果
    params: isPublic 01
    params: artSeqid
    '''
    @check_token
    def post(self):
        _tmpResSet = g.tableArticle.update_article(g.artSeqid, isPublic = g.isPublic)
        if _tmpResSet:
            g.retMsg['status'] = 1
            g.retMsg['code'] = 200
        else:
            
            g.retMsg['msg'] = '动态状态设置失败'

        return jsonify(g.retMsg)

class GetAllArt(Resource):
    '''
    获取所有动态
    '''
    def get(self):
        '''
        params: 获取动态的个数
        '''
        artNum = request.args.get('artNum')
        if artNum:
            _tmpRes = g.tableArticle.get_all_art(artNum)
            if _tmpRes:
                g.retMsg['status'] = 1
                g.retMsg['code'] = 200
                g.retMsg['data'] = _tmpRes
            elif isinstance(_tmpRes, str):
                g.retMsg['status'] = 1
                g.retMsg['code'] = 200
                g.retMsg['msg'] = '暂无动态'
            else:
                
                g.retMsg['msg'] = '动态获取失败'
            
        return jsonify(g.retMsg)


api.add_resource(GetUpdateArticle, '/article/get', '/article/update', '/article/post', endpoint = 'GetUpdateArticle')
api.add_resource(DeleteArticle, '/article/delete', endpoint = 'DeleteArticle')
api.add_resource(GetLikes, '/article/like', endpoint = 'GetLikes')
api.add_resource(SetPublicArt, '/article/set', endpoint = 'SetPublicArt')
api.add_resource(GetAllArt, '/article/getall', endpoint = 'GetAllArt')
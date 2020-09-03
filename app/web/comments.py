from app.web import webIndex, check_token
from app.utils.qiNiu import QiNiuImage
from app.libs import TableComment
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource

api = Api(webIndex)

class AddComment(Resource):

    @check_token
    def post(self):
        '''
        提交评论 和 回复评论
        params: commentSeqid  评论seqid
        params: commentText
        params: articlesId
        '''
        commentSeqid = request.form.get('commentSeqid')
        commentText = request.form.get('text')
        relationArtId = g.artSeqid
        
        # 回复评论
        if commentSeqid:
            _tmpRes = g.tableComment.add_comment(g.user.seqid, commentText, g.isPublic, relationArtId, commentSeqid)

        else:
            _tmpRes = g.tableComment.add_comment(g.user.seqid, commentText, g.isPublic, relationArtId)

        if _tmpRes:
            g.retMsg['status'] = 1
            g.retMsg['code'] = 200
            
            # 更新动态表评论数
            if not g.tableArticle.update_article(relationArtId, comments = 1):
                g.retMsg['msg'] = '动态表评论数修改失败'  
        else:
            g.retMsg['msg'] = '评论提交失败'

        return jsonify(g.retMsg)

class DeleteComment(Resource):

    @check_token
    def post(self):
        '''
        删除评论
        params: commentSeqid  评论seqid
        params: articlesId
        '''
        seqid = int(request.args.get('commentSeqid'))
        relationArtId = g.artSeqid
        commentDict = g.tableComment.get_comment(seqid)
        
        if g.user.seqid != commentDict.get('userid'):
            g.retMsg['msg'] = '只能删除自己的评论'
            return jsonify(g.retMsg)

        _tmpRes = g.tableComment.delete_comment(seqid)
        if _tmpRes:
            g.retMsg['status'] = 1
            g.retMsg['code'] = 200
            if not g.tableArticle.update_article(relationArtId, comments = -1):
                g.retMsg['msg'] = '动态表评论数修改失败'  
        else:
            g.retMsg['msg'] = '评论删除失败'
        return jsonify(g.retMsg)

class GetComment(Resource):
    '''
    获取评论
    *params: commentSeqid  评论seqid
    *params: articlesId  动态seqid
    '''
    @check_token
    def get(self):
        commentSeqid = request.args.get('commentSeqid')
        relationArtId = g.artSeqid
        if commentSeqid:
            _tmpDict = g.tableComment.get_comment(commentSeqid)
            if _tmpDict:
                g.retMsg['status'] = 1
                g.retMsg['code'] = 200
                g.retMsg['data'] = _tmpDict
            else:
                g.retMsg['msg'] = '评论获取失败'

        elif relationArtId:
            _tmpDict = g.tableComment.get_all_comments(relationArtId)
            if _tmpDict:
                g.retMsg['status'] = 1
                g.retMsg['code'] = 200
                g.retMsg['data'] = _tmpDict
            else:
                g.retMsg['msg'] = '评论获取失败'
        
        return jsonify(g.retMsg)


api.add_resource(AddComment, '/comment/add', endpoint = 'AddComment')
api.add_resource(DeleteComment, '/comment/delete', endpoint = 'DeleteComment')
api.add_resource(GetComment, '/comment/get', endpoint = 'GetComment')
from app.web import webIndex, check_token, retMsg, parser
from app.utils.qiNiu import QiNiuImage
from app.libs import TableComment
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource

api = Api(webIndex)

class ActComment(Resource):
    '''
    评论
    '''
    @check_token
    def post(self):
        '''
        提交评论
        '''
        commentText = request.args.get('text')
        isPublic = request.args.get('isPublic')
        relationArtId = request.args.get('relationArticlesId')
        _tmpRes = TableComment.add_comment(commentText, isPublic, relationArtId)
        if _tmpRes:
            retMsg['code'] = 1
        else:
            retMsg['msg'] = '评论提交失败'
        return jsonify(retMsg)

    @check_token
    def get(self):
        '''
        删除评论
        '''
        seqid = request.args.get('seqid')
        _tmpRes = TableComment.delete_comment(seqid)
        if _tmpRes:
            retMsg['code'] = 1
        else:
            retMsg['msg'] = '评论删除失败'
        return jsonify(retMsg)

class GetComment(Resource):
    '''
    获取评论
    '''
    def get(self):
        seqid = request.args.get('seqid')
        relationArtId = request.args.get('relationArticlesId')
        if seqid:
            _tmpDict = TableComment.get_comment(seqid)
            if _tmpDict:
                retMsg['code'] = 1
                retMsg['data'] = _tmpDict
            else:
                retMsg['msg'] = '评论获取失败'

        elif relationArtId:
            _tmpDict = TableComment.get_all_comments(relationArtId)
            if _tmpDict:
                retMsg['code'] = 1
                retMsg['data'] = _tmpDict
            else:
                retMsg['msg'] = '评论获取失败'
        
        return jsonify(retMsg)

api.add_resource(ActComment, '/comment/act', endpoint = 'ActComment')
api.add_resource(GetComment, '/comment/get', endpoint = 'GetComment')
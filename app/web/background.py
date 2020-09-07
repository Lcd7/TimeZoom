from app.web import create_token, webBack, admin_login
from app.libs import TableComment
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource

api = Api(webBack)

class AdminLogin(Resource):
    '''
    管理员登录
    params: *phoneNumber
    params: *email
    params: password
    params: timenow
    '''
    def post(self):
        userName = request.args.get('userName')
        admin = g.tableAdmin.get_admin(userName = userName)
        if not admin:
            g.retMsg['msg'] = '没有此用户'
            return jsonify(g.retMsg)

        if admin.password != g.password:
            g.retMsg['msg'] = '密码错误'
            return jsonify(g.retMsg)

        payload = {
            'userName': admin.userName,
        }
        token = create_token(payload)
        g.tableAdmin.update_token(admin['seqid'], token)
        g.retMsg['status'] = 1
        g.retMsg['code'] = 200
        g.retMsg['msg'] = '成功登录'        
        g.retMsg['data']['token'] = token
        
        return jsonify(g.retMsg)

class AddAdmin(Resource):
    '''
    新增管理员
    '''
    @admin_login
    def post(self):
        userName = request.form.get('userName')
        password = request.form.get('password')
        superadmin = request.form.get('superadmin')
        _tmpRes = g.tableAdmin.add_admin(userName, password, superadmin)
        if not _tmpRes:
            g.retMsg['msg'] = '添加失败'
        
        g.retMsg['status'] = 1
        g.retMsg['code'] = 200
        g.retMsg['msg'] = '成功登录'        
        return jsonify(g.retMsg)

class ChangePassw(Resource):
    @admin_login
    def post(self):
        # 修改密码
        if g.password and g.newpassw:
            if g.admin.password == g.password:
                if not g.tableAdmin.change_passw(g.admin.seqid, g.newpassw):
                    g.retMsg['msg'] = '密码修改失败'
                    return jsonify(g.retMsg)
            else:
                g.retMsg['code'] = 400
                g.retMsg['msg'] = '原密码错误'
                return jsonify(g.retMsg)

        g.retMsg['status'] = 1 
        g.retMsg['code'] = 200
        g.retMsg['msg'] = '修改成功'
        return jsonify(g.retMsg)

class BanAdmin(Resource):
    @admin_login
    def post(self):
        ban = request.args.get('ban')
        userSeqid = request.args.get('userSeqid')
        _tmpRes = g.tableAdmin.ban_admin(userSeqid, ban)
        if not _tmpRes:
            g.retMsg['msg'] = '设置失败'
        
        g.retMsg['status'] = 1
        g.retMsg['code'] = 200
        return jsonify(g.retMsg)

class BanUser(Resource):
    @admin_login
    def post(self):
        ban = request.args.get('ban')
        userSeqid = request.args.get('userSeqid')
        _tmpRes = g.tableAdmin.ban_user(userSeqid, ban)
        if not _tmpRes:
            g.retMsg['msg'] = '设置失败'
        
        g.retMsg['status'] = 1
        g.retMsg['code'] = 200
        return jsonify(g.retMsg)

class BanArticle(Resource):
    @admin_login
    def post(self):
        ban = request.args.get('ban')
        artSeqid = g.artSeqid
        _tmpRes = g.tableAdmin.ban_art(artSeqid, ban)
        if not _tmpRes:
            g.retMsg['msg'] = '设置失败'
        
        g.retMsg['status'] = 1
        g.retMsg['code'] = 200
        return jsonify(g.retMsg)


api.add_resource(AdminLogin, '/login', 'AdminLogin')
api.add_resource(AddAdmin, '/add', 'AddAdmin')
api.add_resource(BanAdmin, '/banadmin', 'BanAdmin')
api.add_resource(BanArticle, '/Banart', 'BanArticle')
api.add_resource(BanUser, '/Banuser', 'BanUser')
api.add_resource(ChangePassw, '/changeinfo', 'ChangePassw')
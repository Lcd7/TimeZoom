TimeZoom 需求文档
================
1. 用户登录以及注册模块
    * 包含图片验证码
    * 登录时长超过30分钟无操作自动退出
2. 动态发表及评论模块
    * 用户发表默认动态仅自己可见，用户可选择公开动态（暂时不考虑图片信息，仅文字即可）
    * 用户只可评论自己的动态（评论前缀为发表评论时间）
    * 用户之间可以相互点赞动态
3. 添加好友模块
    * 用户可添加好友，好友上限50人，添加好友之后才能发私信
4. 用户设置模块
    * 用户可修改密码（需要确认旧密码，新密码填写两次）
    * 用户不可修改昵称（昵称必须唯一）
    * 用户可修改头像
    * 用户可设置性别

TimeZoom 接口文档
================
根据操作不同的数据表来分类接口
1. 用户表
	* 注册				Register				o
	* 登录				Login					o
    * 获取用户信息      getInfo        			o
    * 修改用户信息      changeInfo      		o
    * 更换头像          ChangeAvatar      		o
    * 登出              Logout           		o
    * 添加好友          AddFriend       		o
    * 删除好友          DeleteFriend    		o
    * 回应好友请求      AnswerFriend      		o
	* 获取好友列表		GetFriends				o
	
2. 动态表
	* 获取用户所有动态	GetUpdateArticle/get	o
	* 获取单个动态		GetUpdateArticle/get	o
	* 发布动态			GetUpdateArticle/post	o
	* 删除动态			DeleteArticle			o
	* 点赞动态			GetLikes				o
	* 设置动态是否公开  SetPublicArt			o
	
3. 评论表
	* 提交/回复评论		ActComment/post			o
	* 删除评论			ActComment/get			o
	* 获取动态所有评论	GetComment				o
	* 获取单个评论		GetComment				o 
    



TimeZoom 编码规范
================
数据库名命规则
------------
1. 数据表名命规则 
    * 模块+功能点 如：UserInfo
    * 表名采用驼峰命名法，首字母大写，最长不超过三个英语单词
2. 表字段名命规则
    * 名词+宾语 如：imgName
    * 字段采用驼峰命名法，最长不超过三个英语单词
    >##### 注：所有字段不可使用数字，不可缩写
代码名命规则
------------
1. 包名命规则 
    * 仅小写英文字母且以下划线分割 如：package_name
2. 类 
    * 采用大驼峰名命法即帕斯卡 如：MyClass
    * 内部类使用使用一个下划线作为前导符号 如：_MyClass
3. 函数以及方法
    * 小写+下划线，最长不超三个英语单词 如：function_name
    * 私有方法添加一个下划线作为前导符  如： _function_name
4. 变量
    * 驼峰+下划线，最长不超三个英语单词 如：varName, _tmpVarName
    * 私有变量(private)：使用两个下划线作为前导符 如：__varName
    * 保护变量(protected)：使用一个下划线作为前导符 如： _varName
    * 全局变量以及常量名命规则：使用大写字母+下划线 如： GLOBAL_VAR_NAME
>5.变量常用缩写：
>   * function => fn
>   * text => txt
>   * object => obj
>   * count => cnt
>   * number => num

6. 文件夹名命规则
    * 采用小写字母+下划线，最长不超过三个英文字母
    
7. 文件名命规则
    * 采用驼峰命名法，最长不超过三个英文字母
    * 比如getName.py
    

生成依赖命令：pipreqs ./ --encoding=utf8


from app.libs import DB

class CreateTable:
    '''
    创建SQL数据表
    '''
    @classmethod
    def Table_User(cls):
        strSql = """
            CREATE TABLE [User]
            {
                seqid int NOT NULL PRIMARY KEY,
                phone_number varchar(11) NOT NULL,
                email varchar(25),
                password varchar(100) NOT NULL,
                nickname varchar(20) NOT NULL,
                sex varchar(2),
                relationships varchar(120),
                register_time varchar(100) NOT NULL,
                token varchar(255),
            }
        """
        DB.ExecSqlNoQuery(strSql)

    @classmethod
    def Table_Article(cls):
        strSql = """
            CREATE TABLE Article
            {
                seqid int NOT NULL PRIMARY KEY,
                text varchar(2000) NOT NULL,
                is_public bool DEFAULT False,
                like int DEFAULT 0,
                relation_id int FOREIGN KEY REFERENCES [User](seqid),
            }
        """
        DB.ExecSqlNoQuery(strSql)

    @classmethod
    def Table_Letter(cls):
        strSql = """
            CREATE TABLE Letter
            {
                seqid int NOT NULL PRIMARY KEY,
                userid int NOT NULL FOREIGN KEY REFERENCES [User](seqid),
                friendid int NOT NULL FOREIGN KEY REFERENCES [User](seqid),
                senderid int NOT NULL FOREIGN KEY REFERENCES [User](seqid),
                receiverid int NOT NULL FOREIGN KEY REFERENCES [User](seqid),
                msg_type int NOT NULL,
                text varchar(1000) NOT NULL,
                send_time datetime NOT NULL,
                read_time datetime NOT NULL,
                status bool NOT NULL DEFAULT 0,
            }
        """
        DB.ExecSqlNoQuery(strSql)

    @classmethod
    def Table_Comment(cls):
        strSql = """
            CREATE TABLE T_Comment
            {
                seqid int NOT NULL PRIMARY KEY,
                text varchar(200) NOT NULL,
                is_public bool DEFAULT True,
                relation_id int FOREIGN KEY REFERENCES Article(seqid),
            }
        """
        DB.ExecSqlNoQuery(strSql)
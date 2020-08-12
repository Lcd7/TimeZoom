from app import creat_app
app = creat_app()

if __name__ == "__main__":
    app.run('0.0.0.0', 8058, debug = True)

    # from app.libs.tableUser import get_user_by_phone
    # print(get_user_by_phone('15182696451'))

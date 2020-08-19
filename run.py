from app import creat_app
app = creat_app()

if __name__ == "__main__":
    app.run('0.0.0.0', 8058, debug = True)
from app import create_app
from settings import ROOT_PATH
from bottle import static_file

app = create_app()


@app.get("/statics/<path:path>")
def statics(path):
    return static_file(path, root=f"{ROOT_PATH}/statics/")


@app.get("/favicon.ico")
def favicon():
    return static_file("favicon.png", root=f"{ROOT_PATH}/statics/img/favicon/")


if __name__ == '__main__':
    app.run(debug=True, reloader=True)

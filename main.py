from sanic import Sanic
from routes import bp
from db import init_db

app = Sanic("BookAPI")

app.blueprint(bp)

@app.before_server_start
async def setup_db(app):
    await init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True, single_process=True)
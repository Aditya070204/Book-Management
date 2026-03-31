from sanic import Sanic
from routes import bp
from db import init_db
from redis_client import init_redis, close_redis

app = Sanic("BookAPI")

app.blueprint(bp)

@app.before_server_start
async def setup(app):
    await init_db()
    await init_redis()

@app.after_server_stop
async def shutdown(app):
    await close_redis()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True, single_process=True)

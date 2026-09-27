import aiopg
from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/feed")
async def feed(request):
    tag = request.query.get("tag", "")
    pool = request.app["pg"]
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT id, body FROM posts WHERE '" + tag + "' = ANY(tags) ORDER BY id DESC LIMIT 20"
            )
            rows = await cur.fetchall()
    return web.json_response([{"id": r[0], "body": r[1]} for r in rows])


async def pg_context(app):
    app["pg"] = await aiopg.create_pool("dbname=feed user=feed")
    yield
    app["pg"].close()
    await app["pg"].wait_closed()


def create_app():
    app = web.Application()
    app.add_routes(routes)
    app.cleanup_ctx.append(pg_context)
    return app

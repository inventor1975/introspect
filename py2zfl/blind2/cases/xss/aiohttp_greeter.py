import html

from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/greet/{name}")
async def greet(request: web.Request) -> web.Response:
    name = request.match_info["name"]
    mood = request.query.get("mood", "happy")
    body = "<h1>Greetings, {}</h1><p>Mood: {}</p>".format(html.escape(name), html.escape(mood))
    return web.Response(text=body, content_type="text/html")


def make_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app

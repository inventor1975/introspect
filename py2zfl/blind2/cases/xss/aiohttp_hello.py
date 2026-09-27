from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/hello")
async def hello(request: web.Request) -> web.Response:
    name = request.query.get("name", "world")
    lang = request.query.get("lang", "en")
    greeting = {"en": "Hello", "de": "Hallo", "fr": "Bonjour"}.get(lang, "Hello")
    return web.Response(text=f"<h1>{greeting}, {name}</h1>", content_type="text/html")


app = web.Application()
app.add_routes(routes)

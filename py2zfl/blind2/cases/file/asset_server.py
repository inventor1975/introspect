import os

from aiohttp import web

ASSETS = "/opt/game/assets"


async def asset(request: web.Request) -> web.StreamResponse:
    name = request.match_info["name"]
    location = os.path.join(ASSETS, name)
    if not os.path.exists(location):
        raise web.HTTPNotFound()
    return web.FileResponse(location)


def build_app() -> web.Application:
    application = web.Application()
    application.router.add_get("/assets/{name:.+}", asset)
    return application


if __name__ == "__main__":
    web.run_app(build_app(), port=8081)

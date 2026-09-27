import os

from aiohttp import web

DOWNLOAD_ROOT = os.path.realpath("/srv/mirror/pub")

routes = web.RouteTableDef()


@routes.get("/pub/{tail:.*}")
async def mirror_file(request: web.Request) -> web.StreamResponse:
    tail = request.match_info.get("tail", "")
    candidate = os.path.realpath(os.path.join(DOWNLOAD_ROOT, tail))
    if os.path.commonpath([DOWNLOAD_ROOT, candidate]) != DOWNLOAD_ROOT:
        raise web.HTTPForbidden(text="outside mirror")
    if not os.path.isfile(candidate):
        raise web.HTTPNotFound()
    return web.FileResponse(candidate)


app = web.Application()
app.add_routes(routes)

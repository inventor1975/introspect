import os

from aiohttp import web

DOWNLOAD_ROOT = "/srv/downloads"
routes = web.RouteTableDef()


@routes.get("/download/{name}")
async def download(request):
    name = request.match_info["name"]
    category = request.query.get("category", "general")
    location = os.path.join(DOWNLOAD_ROOT, category, name)
    if not os.path.isfile(location):
        raise web.HTTPNotFound()
    return web.FileResponse(location)


app = web.Application()
app.add_routes(routes)

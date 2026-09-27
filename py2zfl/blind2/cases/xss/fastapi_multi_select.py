from typing import List

from fastapi import FastAPI, Query, Response

app = FastAPI()


@app.get("/filters")
def active_filters(tag: List[str] = Query(default=[])):
    chips = []
    for t in tag:
        chips.append("<span class='chip'>" + t + "</span>")
    html_doc = "<div class='filters'>" + "".join(chips) + "</div>"
    return Response(content=html_doc, media_type="text/html")

from flask import Flask, jsonify, request

app = Flask(__name__)

DEFAULT_SCORE = "likes * 2 + comments * 3"


@app.route("/feed/ranked")
def ranked_feed():
    posts = [
        {"id": 1, "likes": 10, "comments": 2},
        {"id": 2, "likes": 4, "comments": 9},
    ]
    score_expr = DEFAULT_SCORE
    if request.args.get("custom_score"):
        score_expr = request.args["custom_score"]
    for post in posts:
        post["score"] = eval(score_expr, {}, post)
    return jsonify(sorted(posts, key=lambda p: p["score"], reverse=True))

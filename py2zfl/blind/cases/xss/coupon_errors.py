from flask import Flask, request

app = Flask(__name__)

VALID_CODES = {"WELCOME10", "SPRING24", "FREESHIP"}


class InvalidCoupon(Exception):
    def __init__(self, code):
        super().__init__(f"Coupon <code>{code}</code> is not valid")
        self.code = code


@app.errorhandler(InvalidCoupon)
def invalid_coupon(err):
    return f"<div class='error'>{err}</div>", 400


@app.route("/cart/coupon")
def apply_coupon():
    code = request.args.get("code", "")
    if code not in VALID_CODES:
        raise InvalidCoupon(code)
    return f"<p>Coupon {code} applied.</p>"

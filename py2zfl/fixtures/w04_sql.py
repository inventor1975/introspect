from django.db import connection
from myapp.models import Item

def items(request):
    q = request.GET["q"]
    with connection.cursor() as cur:
        cur.execute(f"SELECT * FROM t WHERE n='{q}'", [])   # EXPECT: REFUTED (bind params do not clean the text)
        cur.execute("SELECT * FROM t WHERE n=%s", [q])      # clean
    Item.objects.raw("SELECT * FROM item WHERE n='" + q + "'")   # EXPECT: REFUTED

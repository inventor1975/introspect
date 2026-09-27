from django.http import JsonResponse

COLUMNS = ["sku", "title", "price", "stock"]

ROWS = [
    {"sku": "A-1", "title": "Lamp", "price": 30, "stock": 4},
    {"sku": "B-7", "title": "Desk", "price": 220, "stock": 0},
]


def pick_column(request):
    wanted = request.GET.get("col", "sku")
    expr = "row['sku']"
    for col in COLUMNS:
        if col == wanted:
            expr = f"row['{col}']"
            break
    values = [eval(expr, {}, {"row": row}) for row in ROWS]
    return JsonResponse({"column": wanted, "values": values})

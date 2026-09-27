from django.db import connection
from django.http import JsonResponse
from django.views import View


class RevenueReportView(View):
    base_sql = "SELECT region, SUM(amount) FROM sales_sale WHERE {filter} GROUP BY region"

    def build_filter(self, region):
        if not region:
            return "1=1"
        return "region = '{}'".format(region)

    def get(self, request):
        region = request.GET.get("region", "")
        sql = self.base_sql.format(filter=self.build_filter(region))
        with connection.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchall()
        return JsonResponse({"rows": [[r[0], float(r[1])] for r in data]})

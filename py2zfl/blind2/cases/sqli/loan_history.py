from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Loan


@login_required
def loan_history(request, member_id):
    title = request.GET.get("title", "")
    loans = Loan.objects.raw(
        f"SELECT * FROM library_loan WHERE member_id = %s AND title_snapshot LIKE '%%{title}%%' "
        "ORDER BY borrowed_at DESC",
        [member_id],
    )
    return render(request, "library/loans.html", {"loans": loans, "title": title})

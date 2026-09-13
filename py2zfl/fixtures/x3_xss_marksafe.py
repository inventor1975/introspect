from django.utils.safestring import mark_safe
import html
def view(request):
    name = request.GET.get("name")           # source
    good = mark_safe(html.escape(name))       # EARNED: escaped before marked safe
    bad = mark_safe("<b>" + name + "</b>")    # REFUTED [xss]: raw tainted marked safe
    return good, bad

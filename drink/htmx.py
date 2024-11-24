import drink.models as drinkmodels
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def submit_brand(request):
    name = request.POST.get("brand_name")
    if name:
        brand = drinkmodels.Brand.objects.filter(
            Q(approved=True) | Q(submitted_by=request.user), name=name
        ).first()
        if not brand:
            brand = drinkmodels.Brand.objects.create(
                name=name,
                # approved=False, this will be false when going live
                approved=True,
                submitted_by=request.user,
            )
        context = {
            "brands": drinkmodels.Brand.objects.filter(
                Q(approved=True) | Q(submitted_by=request.user)
            ),
            "selected_brand": brand,
        }
        return render(request, f"drink/htmx/brand_select_htmx.html", context)
    return HttpResponse("Please enter a valid Brand Name", status=400)

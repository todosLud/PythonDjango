from django.shortcuts import render, redirect 
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplicaForm
# Create your views here.

@require_POST
def coupon_applica(request):
    now = timezone.now() #ricordo ora e data di aplicare cupon
    form = CouponApplicaForm(request.POST)
    if form.is_valid():
        codice = form.cleaned_data['codice']
        #verifico se esiste codice inserito e se e valido
        try:
            coupon = Coupon.objects.get(codice__iexact=codice,# exact ==
                                        valido_da__lte=now,#less <=
                                        valido_a__gte=now,# gtreater >=
                                        attivo=True)
            #usando carello, ricordiamo che sta nella sesione
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
        return redirect('cart:cart_detail')
    
            
        
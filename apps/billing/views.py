from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Transaction
from .forms import PurchaseForm, CREDIT_PACKAGES

PACKAGE_PRICES = {
    '100': Decimal('1.00'), '500': Decimal('4.50'),
    '1000': Decimal('8.00'), '5000': Decimal('35.00'),
}

@login_required
def billing_view(request):
    form = PurchaseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        package = form.cleaned_data['package']
        credits = int(package)
        amount = PACKAGE_PRICES.get(package, Decimal('0'))
        profile = request.user.profile
        profile.sms_balance += credits
        profile.save()
        Transaction.objects.create(
            user=request.user, amount=amount, credits=credits,
            transaction_type='purchase', status='completed',
            description=f'Purchased {credits} SMS credits'
        )
        messages.success(request, f'Successfully purchased {credits} SMS credits!')
        return redirect('billing:billing')
    recent_transactions = Transaction.objects.filter(user=request.user)[:5]
    return render(request, 'billing/billing.html', {'form': form, 'recent_transactions': recent_transactions, 'packages': CREDIT_PACKAGES})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    paginator = Paginator(transactions, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'billing/transaction_history.html', {'page_obj': page_obj})

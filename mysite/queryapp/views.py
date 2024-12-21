# queryapp/views.py
from django.shortcuts import render
from .forms import QueryForm
from .models import Product

def query_view(request):
    products = []  # Initialize products list
    query = ""  # Initialize query string

    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Execute the raw SQL query to fetch matching products
            products = Product.objects.raw("SELECT * FROM queryapp_product WHERE name LIKE %s", ['%' + query + '%'])
    else:
        form = QueryForm()

    return render(request, 'queryapp/query_form.html', {
        'form': form,
        'products': products,
        'query': query,
    })

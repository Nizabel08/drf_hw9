# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from .models import Product
from .forms import ProductForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# def product_list(request) :
#     products = Product.objects.all()
#     return render(request, 'products/product_list.html', {'products' : products})

from .mixins import QueryParamsMixin

class ProductListView(ListView, QueryParamsMixin) :
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset =  super().get_queryset()
    
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if query :
            queryset = queryset.filter(Q(name__icontains = query)) 

        if category :
            queryset = queryset.filter(category__name = category)

        if min_price :
            queryset = queryset.filter(price__gte = min_price) 

        if max_price :
            queryset = queryset.filter(price__lte = max_price) 

        print(self.request.GET)
        # return queryset

        order_by = self.request.GET.get('order_by')
        if order_by in ['name', '-name', 'price', '-price', 'id', '-id'] :
            queryset - queryset.order_by(order_by)

        else :
            queryset = queryset.order_by('id')

        return queryset


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     querydict = self.request.GET.copy()
    #     if 'page' in querydict:
    #         querydict.pop('page')  # remove page param
    #     context['querystring'] = querydict.urlencode()
    #     return context




# def product_detail(request, pk) :
#     product = get_object_or_404(Product, pk = pk)
#     return render (request, 'products/product_detail.html', {'product' : product})

class ProductDetailView(DetailView) :
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        recent = self.request.session.get('recent_products', [])
        if product.id not in recent :
            recent.append(product.id)

        recent = recent[-5:]
        self.request.session['recent_products'] = recent
        context['recent_products'] = Product.objects.filter(id__in = recent).exclude(id = product.id)

        recent_products = list(Product.objects.filter(id__in = recent))
        recent_products_sorted = sorted(
            recent_products, key = lambda x: recent.index(x.id), reverse=True
        )

        recent_products_sorted = [p for p in recent_products_sorted if p.id != product.id]
        context['recent_products'] = recent_products_sorted
        return context



# @ login_required
# def add_product(request) :
#     if request.method == 'POST' :
#         form = ProductForm(request.POST)
#         if form.is_valid() :
#             product = form.save(commit = False)
#             product.user = request.user
#             product.save()
#             return redirect('product_list')
#     else :
#         form = ProductForm()
#     return render(request, 'products/add_product.html', {'form' : form})

class AddProductView(LoginRequiredMixin, CreateView) :
    model = Product
    form_class = ProductForm
    template_name = 'products/add_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



# @ login_required
# def admin_update_product(request, pk) :
#     product = get_object_or_404(Product, pk = pk)
#     if request.method == 'POST' :
#         method = request.POST.get('_method', '').upper()
#         if method == 'PUT' :
#             if not request.user.is_superuser :
#                 return HttpResponseForbidden('Only admin can change this product')
#             form = ProductForm(request.POST, instance=product)
#             if form.is_valid():
#                 form.save()
#                 return redirect('product_detail', pk = product.pk)
#         else :
#             return HttpResponseNotAllowed(['PUT'])
        
#     else :
#         form = ProductForm(instance=product)

#     return render(request, 'products/admin_update_product.html', {'form' : form, 'product' : product})


class AdminUpdateProductView(UpdateView, LoginRequiredMixin, UserPassesTestMixin) :
    model = Product
    form_class = ProductForm
    template_name = 'products/admin_update_product.html'
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        method = request.POST.get('_method', '').upper()
        if method != 'PUT' :
            return HttpResponseNotAllowed(['PUT'])

        return super().post(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated :
            return HttpResponseForbidden('Only admin can change this product')
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs = {'pk' : self.object.pk})
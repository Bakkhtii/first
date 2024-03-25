from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from product.models import CategoryModel, ProductModel, CartModel
from product.forms import SearchForm
from product.handler import bot


# def home_page(request):
#     categories = CategoryModel.objects.all()
#     products = ProductModel.objects.all()
#     form = SearchForm
#     context = {'categories': categories, 'products': products}
#     return render(request, template_name='index.html', context=context)


class HomePage(ListView):
    form = SearchForm
    template_name = 'index.html'
    model = ProductModel
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = CategoryModel.objects.all()
        context["products"] = ProductModel.objects.all()
        return context


class MyLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/'


# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('home')


def search(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')
        try:
            exact_product = ProductModel.objects.get(product_title__icontains=get_product)
            return redirect(f'/products/{exact_product.id}')
        except:
            return redirect('/')


def product_page(request, pk):
    product = ProductModel.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'product.html', context)


def category_page(request, pk):
    category = CategoryModel.objects.get(id=pk)
    current_products = ProductModel.objects.filter(product_category=category)
    context = {'product': current_products}
    return render(request, 'category.html', context)


def add_product_to_user_cart(request, pk):
    if request.method == 'POST':
        checker = ProductModel.objects.get(pk=pk)  # 4

        if checker.product_count >= int(request.POST.get('pr_count')):
            CartModel.objects.create(user_id=request.user.id,
                                     user_product=checker,
                                     user_product_quantity=int(request.POST.get('pr_count'))
                                     ).save()
            return redirect('/user_cart')
        else:
            return redirect('/')


def user_cart(request):
    cart = CartModel.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        main_text = 'Новый заказ\n'

        for i in cart:
            main_text += f'Товар: {i.user_product}\n' \
                         f'Кол-во: {i.user_product_quantity}\n' \
                         f'Покупатель: {i.user_id}\n' \
                         f'Цена товара: {i.user_product.product_price}\n'
            bot.send_message(-1002143243562, main_text)
            cart.delete()
            return redirect('/')
    else:
        return render(request, template_name='cart.html', context={'cart': cart})


def delete_user_cart(request, pk):
    product_delete = ProductModel.objects.get(pk=pk)
    CartModel.object.filter(user_id=request.user.id, user_product=product_delete).delete()
    return redirect('/user_cart')

    # -1002143243562
    # 6497247306:AAH5jv4gUp8NiAdsc8iCFQ8hv9u8MLCXTFk

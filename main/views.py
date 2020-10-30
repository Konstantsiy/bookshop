from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import View

from django.http import HttpResponseRedirect

from .models import Book, Author, Genre, Order, OrderItem, Customer
from .forms import ReviewForm


def get_cart_items_count(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item_count = order.get_cart_items
        return order_item_count
    else:
        return 0


def about(request):
    count = get_cart_items_count(request)
    return render(request, 'home/about.html', {'cart_items_count': count})


class GenreAuthor:
    def get_genres(self):
        return Genre.objects.all()

    def get_authors(self):
        # return Book.objects.filter(draft=False).values_list('author__name')
        return Author.objects.all()
        # return Book.objects.filter(draft=False).values('year')


class BookView(GenreAuthor, ListView):
    model = Book
    queryset = Book.objects.filter(draft=False)
    template_name = 'home/home.html'

    # paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['model_name'] = self.model._meta.model_name
        return context


class BookDetailView(GenreAuthor, DetailView):
    model = Book
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddReview(GenreAuthor, View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        book = Book.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.book_id = pk
            form.book = book
            form.save()
        return redirect(book.get_absolute_url())


class AuthorView(DetailView):
    model = Author
    template_name = 'main/author.html'
    slug_field = 'name'


class FilterBooksView(GenreAuthor, ListView):
    # paginate_by = 2

    def get_queryset(self):
        queryset = Book.objects.filter(
            Q(author__in=self.request.GET.getlist("author")) |
            Q(genre__in=self.request.GET.getlist("genre"))
        )
        return queryset


class Search(ListView):
    paginate_by = 2

    def get_queryset(self):
        return Book.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class CartView(View):
    def get(self, request, *args, **kwargs):
        order = None
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
        count = get_cart_items_count(request)
        context = {'items': items, 'order': order, 'order_items_count': count}
        return render(request, 'main/cart.html', context)
        # books = Book.objects.filter(url=kwargs.get('slug'))
        # total_price = 0
        # for book in books:
        #     total_price += book.price
        # return render(request, 'main/cart.html', {'books': books, 'total_price': total_price})


class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        book_slug = kwargs.get('slug')
        book = Book.objects.get(url=book_slug)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order_item, created = OrderItem.objects.get_or_create(order=order, book=book)

            items = order.orderitem_set.all()

            flag = False
            for item in items:
                if book.__eq__(item.book):
                    item.quantity += 1
                    item.save()
                    flag = True

            if not flag:
                new_order_item = OrderItem(book=book, order=order, quantity=1)
                new_order_item.save()
                order.save()

            return render(request, 'main/cart.html', {'order': order, 'items': items})


class DeleteFromCartView(View):
    def get(self, request, *args, **kwargs):
        books_slug = kwargs.get('slug')
        book = Book.objects.get(url=books_slug)
        print(book.title)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            # items = order.orderitem_set.filter(book=book).delete()
            order.orderitem_set.get(book=book).delete()
            items = order.orderitem_set.all()
            print(items)
            return render(request, 'main/cart.html', {'order': order, 'items': items})


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "main/registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "main/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

# def registrationView(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             # form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             return render(request, 'main/login.html')
#     else:
#         form = UserCreationForm
#     return render(request, 'main/registration.html', {'form': form})
#
#
# def loginView(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#
#             user = authenticate(username=username, password=password)
#             login(request, user)
#
#             return render(request, '/')
#     else:
#         form = LoginForm
#     return render(request, 'main/login.html', {'form': form})

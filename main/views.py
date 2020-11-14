from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import View

from django.http import HttpResponseRedirect, HttpResponse

from .models import Book, Author, Genre, Order, OrderItem, Customer
from .forms import ReviewForm, LoginForm


def get_cart_items_count(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item_count = order.get_cart_items
        return order_item_count
    else:
        return 0


def about(request):
    # count = get_cart_items_count(request)
    return render(request, 'main/about.html')


def filter_by_genre(request, slug):
    queryset = Book.objects.filter(genre__url=slug)
    return render(request, 'main/home.html', {'book_list': queryset})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


class IteratorBase(object):
    def first(self):
        raise NotImplementedError()

    def last(self):
        raise NotImplementedError()

    def next(self):
        raise NotImplementedError()

    def prev(self):
        raise NotImplementedError()

    def current_item(self):
        raise NotImplementedError()

    def is_done(self, index):
        raise NotImplementedError()

    def get_item(self, index):
        raise NotImplementedError()


class Iterator(IteratorBase):
    def __init__(self, list_=None):
        self._list = list_ or []
        self._current = 0

    def first(self):
        return self._list[0]

    def last(self):
        return self._list[-1]

    def current_item(self):
        return self._list[self._current]

    def is_done(self, index):
        last_index = len(self._list) - 1
        return 0 <= index <= last_index

    def next(self):
        self._current += 1
        if not self.is_done(self._current):
            self._current = 0
        return self.current_item()

    def prev(self):
        self._current -= 1
        if not self.is_done(self._current):
            self._current = len(self._list) - 1
        return self.current_item()

    def get_item(self, index):
        if not self.is_done(index):
            raise IndexError('No item with index: %d' % index)
        return self._list[index]


class Memento(object):
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state


class Caretaker(object):
    def __init__(self):
        self._memento = None

    def get_memento(self):
        return self._memento

    def set_memento(self, memento):
        self._memento = memento


class Originator(object):
    def __init__(self):
        self._state = None

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state

    def save_state(self):
        return Memento(self._state)

    def restore_state(self, memento):
        self._state = memento.get_state()


class GenreAuthor:
    def get_genres(self):
        return Genre.objects.all()

    def get_authors(self):
        return Author.objects.all()


class BookView(GenreAuthor, ListView):
    model = Book
    queryset = Book.objects.filter(draft=False)
    template_name = 'main/home.html'

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
    # template_name = 'main/author.html'
    slug_field = 'name'


class FilterBooksView(GenreAuthor, ListView):
    # paginate_by = 2

    slug_field = 'url'
    queryset = Book.objects.filter(genre__url=slug_field)
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Search(ListView):
    paginate_by = 2
    template_name = 'main/home.html'

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

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order.orderitem_set.get(book=book).delete()
            items = order.orderitem_set.all()
            return render(request, 'main/cart.html', {'order': order, 'items': items})


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "account/registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "account/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

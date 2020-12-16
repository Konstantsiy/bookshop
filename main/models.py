from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Category', max_length=150)
    url = models.SlugField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Author(models.Model):
    name = models.CharField('Author', max_length=150)
    biography = models.TextField('Biography')
    image = models.ImageField('Image', upload_to='authors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Genre(models.Model):
    title = models.CharField('Genre', max_length=150)
    url = models.SlugField(max_length=60, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Book(models.Model):
    title = models.CharField('Title', max_length=100)
    price = models.DecimalField('Price', max_digits=9, decimal_places=2)
    year = models.PositiveIntegerField('Release year', default=0)
    description = models.TextField('Description')
    size = models.PositiveIntegerField('Number of pages')
    image = models.ImageField('Cover image', upload_to='books/')
    cover = models.CharField('Cover type', max_length=100)
    author = models.ManyToManyField(Author, verbose_name='Author', related_name='book_author')
    genre = models.ManyToManyField(Genre, verbose_name='Genre', related_name='book_genre')
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField('Draft', default=False)

    def __str__(self):
        return self.title

    def __eq__(self, other):
        return self.title == other.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Name', max_length=100)
    text = models.TextField('Message', max_length=3000)
    parent = models.ForeignKey('self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True)
    book = models.ForeignKey(Book, verbose_name="Book", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.book}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='Name', null=True)
    email = models.CharField(max_length=200, verbose_name='Email', null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=False, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return 'for_' + str(self.customer.name) + str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.book.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    cvv = models.CharField(max_length=200, null=True)
    card_number = models.CharField(max_length=100, null=True)
    date_added = models.CharField(max_length=200, null=True)
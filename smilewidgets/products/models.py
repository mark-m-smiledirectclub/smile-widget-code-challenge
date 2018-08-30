from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class GiftCardManager(models.Manager):
    def get_valid_giftcard(self, gift_card_code, date):
        """Given a coupon code and date, return gift card if one exists"""
        return self.filter(
            models.Q(code=gift_card_code),
            models.Q(date_end__isnull=True, date_start__lte=date) |
            models.Q(date_end__gte=date, date_start__lte=date)
        ).first()


class GiftCard(models.Model):
    code = models.CharField(max_length=30, unique=True)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    objects = GiftCardManager()

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)

class ProductPriceManager(models.Manager):
    def get_product_price_for_date(self, date, product):
        """Given a date and product, return a product price if one exists"""
        product_price = self.filter(
            date_start__lte=date,
            date_end__gte=date,
            product=product,
        ).first()

        return product_price

class ProductPrice(models.Model):
    price = models.PositiveIntegerField(help_text='Price of product in cents')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    objects = ProductPriceManager()


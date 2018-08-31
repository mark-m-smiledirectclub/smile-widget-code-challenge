from django.test import TestCase, Client

from products.models import Product, ProductPrice, GiftCard
from products.views import NO_PRODUCT_FOUND_MSG

import json


class ProductBaseTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.cool_product = Product.objects.create(name='Cool Product 1', code='COOL', price=100000)
        self.awesome_product = Product.objects.create(name='Awesome Product', code='AWESOME', price=1000)
        self.crappy_product = Product.objects.create(name='Crappy Product', code='CRAPPY', price=9900000)

        self.future_cool_price_product = ProductPrice.objects.create(
            price=20000, product=self.cool_product, date_start='2050-01-01', date_end='2050-12-31'
        )
        self.near_future_cool_price_product =ProductPrice.objects.create(
            price=500, product=self.cool_product, date_start='2020-05-01', date_end='2020-05-28'
        )
        self.future_awesome__price_product = ProductPrice.objects.create(
            price=90000, product=self.awesome_product, date_start='2019-11-16', date_end='2019-11-20'
        )

        self.ten_off = GiftCard.objects.create(
            code='10OFF', amount=1000, date_start='2050-06-22'
        )
        self.one_fifty_off = GiftCard.objects.create(
            code='150OFF', amount=15000, date_start='2022-07-01'
        )
        self.two_hundred_off = GiftCard.objects.create(
            code='200OFF', amount=20000, date_start='2017-01-15', date_end=None
        )


class TestGetPriceAPI(ProductBaseTestCase):

    def test_get_product_price(self):
        """Given a valid date and product code, return the products corresponding price"""
        expected_data = {'price': self.crappy_product.price}
        url = '/api/get_price/?productCode={}&date=1990-02-20'.format(self.crappy_product.code)

        response = self.client.get(url)

        self.assertJSONEqual(response.content, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_get_product_price_with_related_product_price(self):
        """Given a valid date and product code, return the products corresponding price when a product price exists"""
        expected_data = {'price': self.future_cool_price_product.price}
        url = '/api/get_price/?productCode={}&date=2050-05-28'.format(self.cool_product.code)

        response = self.client.get(url)

        self.assertJSONEqual(response.content, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_get_product_price_with_giftcard(self):
        """Given a valid date, product code, and gift card return the products corresponding price"""
        expected_price = self.crappy_product.price - self.two_hundred_off.amount
        expected_data = {'price': expected_price}
        url = '/api/get_price/?productCode={}&date=2017-05-28&giftCardCode={}'.format(
            self.crappy_product.code, self.two_hundred_off.code
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_data)

    def test_get_product_price_when_no_product_exists(self):
        """Given a invalid product code return 404 error"""
        expected_data = {'price': NO_PRODUCT_FOUND_MSG}
        url = '/api/get_price/?productCode={}&date=2017-05-28'.format(
            'THISCODEDOESNTEXIST'
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, expected_data)

    def test_valid_date_param_required(self):
        """GetPrice should throw an error when the date query parameter is badly formatted"""
        expected_error = {"date":["Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]]."]}
        response = self.client.get('/api/get_price/?date=202@@20-0111115-15&productCode=COOL')

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, expected_error)

    def test_product_param_required(self):
        """GetPrice should throw an error when no product_code is given"""
        expected_error = {"product_code":["This field may not be null."]}
        response = self.client.get('/api/get_price/?date=2020-05-15')

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, expected_error)

    def test_date_param_required(self):
        """GetPrice should throw an error when no date is given"""
        expected_error = {"date":["This field may not be null."]}
        response = self.client.get('/api/get_price/?productCode=COOL')

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, expected_error)


class TestGiftCardModel(ProductBaseTestCase):

    def test_giftcard_get_valid_coupon(self):
        """get_valid_giftcard should return a valid coupon when date falls in range and code exists"""
        expected_gift_card = self.two_hundred_off
        giftcard = GiftCard.objects.get_valid_giftcard('200OFF', '2018-09-09')

        self.assertEqual(giftcard, expected_gift_card)

    def test_giftcard_get_valid_coupon_with_fake_code(self):
        """get_valid_giftcard should return None when there is no gift card for a given code"""
        giftcard = GiftCard.objects.get_valid_giftcard('FAKECODEEEEEE', '2018-09-09')

        self.assertIsNone(giftcard)


class TestProductPriceModel(ProductBaseTestCase):

    def test_get_product_price_when_exist(self):
        """Given a product and date, return a product price when it exists"""
        expected_product_price = self.future_cool_price_product
        product_price = ProductPrice.objects.get_product_price_for_date('2050-08-01', self.cool_product)

        self.assertEqual(product_price, expected_product_price)

    def test_get_product_price_when_doesnt_exist(self):
        """Given a product and date, return None when date out of range"""
        expected_product_price = self.future_cool_price_product
        product_price = ProductPrice.objects.get_product_price_for_date('2018-08-01', self.cool_product)

        self.assertIsNone(product_price)



from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response

from products.models import GiftCard, Product, ProductPrice


NO_PRODUCT_FOUND_MSG = 'No product was found for that product code'


class ProductDateSerializer(serializers.Serializer):
    date = serializers.DateField()
    product_code = serializers.CharField()

class GetPriceView(APIView):
    def get(self, request, format=None):
        gift_card_code = request.query_params.get('giftCardCode', None)
        product_code = request.query_params.get('productCode')
        date = request.query_params.get('date')

        serializer = ProductDateSerializer(data={
            'product_code': product_code,
            'date': date
        })

        if serializer.is_valid(raise_exception=True):
            product = Product.objects.filter(code=product_code).first()

            if not product:
                content = {'price': NO_PRODUCT_FOUND_MSG}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            product_price = ProductPrice.objects.get_product_price_for_date(date, product)

            if product_price:
                price = product_price.price
            else:
                price = product.price

            if gift_card_code:
                gift_card = GiftCard.objects.get_valid_giftcard(gift_card_code, date)
                if gift_card:
                    price -= gift_card.amount

            return Response({
                'price': price
            })


import time

from rest_framework.serializers import (
    ModelSerializer, FloatField,
    DateTimeField,
    CharField
)

from mutual_funds.finance.models import Fund, NAV


class UnixEpochDateField(DateTimeField):
    def to_representation(self, value):
        try:
            return int(time.mktime(value.timetuple())) * 1000
        except (AttributeError, TypeError):
            return None

    def to_internal_value(self, value):
        import datetime
        return datetime.datetime.fromtimestamp(int(value))


class NAVDetailSerializer(ModelSerializer):
    date = UnixEpochDateField()
    price = FloatField()

    class Meta:
        model = NAV
        fields = ['date', 'price']

    def to_representation(self, instance):
        representation = super(NAVDetailSerializer, self).to_representation(instance)
        return [representation['date'], representation['price']]


class FundDetailSerializer(ModelSerializer):
    navs = NAVDetailSerializer(many=True)

    class Meta:
        model = Fund
        fields = ['navs']


class FundListSerializer(ModelSerializer):
    finance_sector_name = CharField(source='finance_sector.name', read_only=True)

    class Meta:
        model = Fund
        service_name = 'mycustom name'
        fields = ['name', 'finance_sector_name', 'get_newest_price']

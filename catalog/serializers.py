from rest_framework import serializers
from .models import Branch, Product, Category
from decimal import Decimal
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    image = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # Make these fields optional for updates
    stock_quantity = serializers.IntegerField(required=False)
    low_stock_threshold = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    last_modified_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'price', 'unit', 
            'on_sale', 'sale_price', 'branch', 'image', 'stock_quantity', 
            'low_stock_threshold', 'is_active', 'created_by', 'last_modified_by'
        ]
       
        extra_kwargs = {
            'sale_price': {'required': False, 'allow_null': True},
            'created_by': {'required': False, 'allow_null': True},
            'last_modified_by': {'required': False, 'allow_null': True},
        }

    def validate(self, data):
        # Custom validation: if on_sale is True, sale_price should be provided
        if data.get('on_sale', False) and not data.get('sale_price'):
            raise serializers.ValidationError("Sale price is required when product is on sale")
        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['category'] = CategorySerializer(instance.category).data
        ret['branch'] = BranchSerializer(instance.branch).data
        try:
            if instance.image:
                ret['image'] = instance.image.url
            else:
                ret['image'] = None
        except Exception as e:
            # Optional: log error
            ret['image'] = None
        return ret
from rest_framework import serializers
from .models import SubVariant, Variant, ProductVariant, ProductSubVariant, Products
from versatileimagefield.serializers import VersatileImageFieldSerializer
from decimal import Decimal


class SubVariantSerializer(serializers.ModelSerializer):
    """To validate sub variants"""

    name = serializers.CharField(required=True, max_length=255)

    class Meta:
        model = SubVariant
        fields = ["id", "name"]
        read_only_fields = ["id"]


class VariantSerializer(serializers.ModelSerializer):
    """To validate variants"""

    options = serializers.ListField(
        child=serializers.CharField(max_length=255), required=True
    )

    class Meta:
        model = Variant
        fields = ["id", "name", "options"]
        read_only_fields = ["id"]

    def validate_options(self, value):
        if not value:
            raise serializers.ValidationError("At least one option is required.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    """To validate sub variants"""

    variants = VariantSerializer(many=True, write_only=True)
    name = serializers.CharField(source="ProductName", required=True)
    ProductImage = VersatileImageFieldSerializer(
        sizes=[
            ("thumbnail", "crop__100x100"),
            ("medium", "thumbnail__500x500"),
        ],
        required=False,
    )

    class Meta:
        model = Products
        fields = [
            "id",
            "name",
            "variants",
            "ProductID",
            "ProductCode",
            "TotalStock",
            "ProductImage",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        variants_data = validated_data.pop("variants")
        user = self.context["request"].user
        validated_data["CreatedUser"] = user
        product = Products.objects.create(**validated_data)

        for variant_data in variants_data:
            sub_variants_data = variant_data.pop("options")
            variant_name = variant_data["name"]
            variant, _ = Variant.objects.get_or_create(name=variant_name.upper())
            product_variant = ProductVariant.objects.create(
                product=product, variant=variant
            )

            for sub_variant_name in sub_variants_data:
                sub_variant, _ = SubVariant.objects.get_or_create(
                    name=sub_variant_name.upper(), variant=variant
                )
                ProductSubVariant.objects.create(
                    product_variant=product_variant, sub_variant=sub_variant
                )

        return product


class ListProductSerializer(serializers.ModelSerializer):
    """To list all products"""
    CreatedUser = serializers.CharField(source="CreatedUser.username")
    ProductImage = VersatileImageFieldSerializer(
        sizes=[
            ("thumbnail", "crop__100x100"),
            ("medium", "thumbnail__500x500"),
        ]
    )

    class Meta:
        model = Products
        fields = [
            "id",
            "ProductID",
            "ProductCode",
            "ProductName",
            "CreatedUser",
            "TotalStock",
            "ProductImage",
        ]

class UpdateTotalStockSerializer(serializers.ModelSerializer):
    """To add/deduct the TotalStock"""
    newStock = serializers.DecimalField(max_digits=20, decimal_places=8, write_only=True)
    action = serializers.ChoiceField(choices=["add", "deduct"], write_only=True)
    TotalStock = serializers.DecimalField(max_digits=20, decimal_places=8, read_only=True)

    class Meta:
        model = Products
        fields = ['newStock', 'action', 'TotalStock']

    def validate_newStock(self, value):
        if value <= 0:
            raise serializers.ValidationError("Enter a valid quantity.")
        return value

    def update(self, instance, validated_data):
        action = validated_data.get("action")
        new_stock = validated_data.get("newStock")

        if isinstance(new_stock, (float, int)):
            new_stock = Decimal(str(new_stock))

        if action == "add":
            instance.TotalStock += new_stock
        elif action == "deduct":
            if instance.TotalStock < new_stock:
                raise serializers.ValidationError("Insufficient total stock.")
            instance.TotalStock -= new_stock

        instance.save()
        return instance
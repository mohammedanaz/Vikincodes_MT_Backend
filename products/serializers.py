from rest_framework import serializers
from .models import SubVariant, Variant, ProductVariant, ProductSubVariant, Products

class SubVariantSerializer(serializers.ModelSerializer):
    '''To validate sub variants'''
    name = serializers.CharField(required=True, max_length=255)

    class Meta:
        model = SubVariant
        fields = ["id", "name"]
        read_only_fields = ['id']

class VariantSerializer(serializers.ModelSerializer):
    '''To validate variants'''
    options = serializers.ListField(
        child=serializers.CharField(max_length=255), required=True
    )

    class Meta:
        model = Variant
        fields = ["id", "name", "options"]
        read_only_fields = ['id']

    def validate_options(self, value):
        if not value:
            raise serializers.ValidationError("At least one option is required.")
        return value
    
class ProductSerializer(serializers.ModelSerializer):
    '''To validate sub variants'''
    variants = VariantSerializer(many=True, write_only=True)
    name = serializers.CharField(source='ProductName', required=True)

    class Meta:
        model = Products
        fields = ["id", "name", "variants"]
        read_only_fields = ['id']

    def create(self, validated_data):
        variants_data = validated_data.pop("variants")
        user = self.context['request'].user
        validated_data['CreatedUser'] = user
        product = Products.objects.create(**validated_data)

        for variant_data in variants_data:
            sub_variants_data = variant_data.pop("options")
            variant_name = variant_data["name"]
            variant, _ = Variant.objects.get_or_create(name=variant_name.upper())
            product_variant = ProductVariant.objects.create(product=product, variant=variant)

            for sub_variant_name in sub_variants_data:
                sub_variant, _ = SubVariant.objects.get_or_create(
                    name=sub_variant_name.upper(), variant=variant
                )
                ProductSubVariant.objects.create(
                    product_variant=product_variant, sub_variant=sub_variant
                )

        return product

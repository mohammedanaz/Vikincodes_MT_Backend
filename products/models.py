import uuid
from django.db import models
from django.utils.translation import gettext as _
from versatileimagefield.fields import VersatileImageField

class Products(models.Model):
    '''To store product details'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ProductID = models.BigIntegerField(unique=True, blank=True, null=True)
    ProductCode = models.CharField(max_length=255, unique=True, blank=True, null=True)
    ProductName = models.CharField(max_length=255)
    ProductImage = VersatileImageField(upload_to="uploads/", blank=True, null=True)    
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    CreatedUser = models.ForeignKey(
        "auth.User", related_name="user%(class)s_objects", on_delete=models.CASCADE
    )
    IsFavourite = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)
    HSNCode = models.CharField(max_length=255, blank=True, null=True)
    TotalStock = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )

    class Meta:
        db_table = "products_product"
        verbose_name = _("product")
        verbose_name_plural = _("products")
        unique_together = (("ProductCode", "ProductID"),)
        ordering = ("-CreatedDate", "ProductID")

    def save(self, *args, **kwargs):
        self.ProductName = self.ProductName.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ProductName}'

class Variant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "products_variants"
        ordering = ("name",)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

class SubVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(
        Variant, related_name="sub_variants", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "products_sub_variants"
        ordering = ("name",)
        unique_together = (("variant", "name"),)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

class ProductVariant(models.Model):
    product = models.ForeignKey(
        Products, related_name="product_variants", on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        Variant, related_name="product_variants", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "products_product_variants"
        unique_together = ("product", "variant")

    def __str__(self):
        return f'{self.product}-{self.variant}'

class ProductSubVariant(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant, related_name="product_sub_variants", on_delete=models.CASCADE
    )
    sub_variant = models.ForeignKey(
        SubVariant, related_name="product_sub_variants", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "products_product_sub_variants"
        unique_together = ("product_variant", "sub_variant")
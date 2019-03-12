""" Main structure """
from io import BytesIO
from wand.image import Image
from django.core.files.base import ContentFile
from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Category(models.Model):
    """ Category structure """
    name = models.CharField(max_length=200,
                            db_index=True,
                            verbose_name="商品分類")
    attr = models.CharField(max_length=200,
                            db_index=True,
                            blank=True,
                            verbose_name="分類屬性")
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            default='')

    parent = models.ForeignKey('self',
                               blank=True,
                               null=True,
                               related_name='children',
                               default=None,
                               verbose_name="上層分類")
    ordering = models.IntegerField(
        default=100,
        verbose_name="顯示順序")
    available = models.BooleanField(default=True,
                                    verbose_name="顯示")

    class Meta:
        ordering = ('name',)
        verbose_name = "商品分類"
        verbose_name_plural = "商品分類"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Get absolute url """
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

def thumb_folder(instance, filename):
    """ Generate thumb folder """
    return '/'.join(['thumbs', instance.no, filename])

def image_folder(instance, filename):
    """ Generate thumb folder """
    return '/'.join(['products', instance.no, filename])

def images_folder(instance, filename):
    """ Generate thumb folder """
    return '/'.join(['products', instance.product.no, filename])

class Product(models.Model):
    """ Product structure """
    def number():
        """ Generate Porduct No """
        product_no = Product.objects.latest('id').id + 1
        return "CMD-" + str(product_no).zfill(9)

    no = models.CharField(max_length=20,
                          db_index=True,
                          blank=True,
                          unique=True,
                          default=number,
                          verbose_name="商品編號")
    name = models.CharField(max_length=200,
                            db_index=True,
                            verbose_name="商品名稱")
    category = models.ManyToManyField(Category,
                                      verbose_name="商品類別")
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to=image_folder,
                              default='products/no_image.png',
                              verbose_name="商品主圖")
    thumbnail = models.ImageField(null=True,
                                  blank=True,
                                  upload_to=thumb_folder,
                                  default='',
                                  verbose_name="商品縮圖")
    description = models.TextField(blank=True,
                                   verbose_name="商品描述")
    price = models.DecimalField(max_digits=10, decimal_places=0,
                                verbose_name="商品價格")
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="商品庫存")
    available = models.BooleanField(default=True,
                                    verbose_name="上/下架")
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="建立日期")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="最後修改日期")
    views = models.PositiveIntegerField(default=0,
                                        verbose_name="瀏覽次數")

    class Meta:
        ordering = ("name",)
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Overridding save method """
        if self.thumbnail == "":
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail')

        super(Product, self).save(*args, **kwargs)

    def make_thumbnail(self):
        """ Generate thumbnail """
        image = Image(file=self.image)
        image.resize(220, 220)

        thumb_name, thumb_extension = str(self.image).split('/')[-1].split('.')

        thumb_filename = thumb_name + '_thumb.' + thumb_extension

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(file=temp_thumb)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        image.close()

        return True

    def get_absolute_url(self):
        """ Get absolute url """
        return reverse('shop:product_detail',
                       args=[self.id, self.no])

    def increase_views(self):
        """ Views function """
        self.views += 1
        self.save(update_fields=['views'])

    def image_data(self):
        """ Generate thumbnail in admin """
        return '<img src="{}" width="100px"/>'.format(self.thumbnail.url)

    image_data.allow_tags = True
    image_data.short_description = '產品縮圖'


class ProductImage(models.Model):
    """ ProductImage structure """
    product = models.ForeignKey(Product,
                                related_name='product_images',
                                on_delete=models.CASCADE,
                                verbose_name="商品")
    image = models.ImageField(upload_to=images_folder,
                              null=True,
                              blank=True,
                              verbose_name="圖片")
    ordering = models.PositiveIntegerField(
        default=1,
        verbose_name="圖片順序")

    class Meta:
        verbose_name = "商品圖片"
        verbose_name_plural = "商品圖片"

    def image_data(self):
        """ Generate thumbnail in admin """
        return '<img src="{}" width="100px"/>'.format(self.image.url)

    image_data.allow_tags = True
    image_data.short_description = '縮圖'

    def __str__(self):
        return str(self.product.no) + '-' + str(self.ordering)


class ProductVideo(models.Model):
    """ ProductVideo structure """
    product = models.ForeignKey(Product,
                                related_name='product_videos',
                                on_delete=models.CASCADE,
                                verbose_name="商品")
    url = models.URLField(max_length=200,
                          verbose_name="影片")
    ordering = models.PositiveIntegerField(
        default=1,
        verbose_name="影片順序")

    class Meta:
        verbose_name = "商品影片"
        verbose_name_plural = "商品影片"

    def __str__(self):
        return str(self.product.no) + '-' + str(self.ordering)


class Supplier(models.Model):
    """ Supplier structure """
    SUPPLIER_CHOICES = (
        ('000', '自批貨'),
        ('001', '大盤大'),
        ('002', '享愛網'),
    )
    product = models.ForeignKey(Product,
                                related_name='product_suppliers',
                                on_delete=models.CASCADE)
    supplier = models.CharField(max_length=40,
                                choices=SUPPLIER_CHOICES,
                                verbose_name="廠商名稱")
    no = models.CharField(max_length=20,
                          db_index=True,
                          blank=True,
                          verbose_name="廠商編號")
    url = models.URLField(max_length=250,
                          blank=True,
                          default="",
                          verbose_name="商品網址")
    available = models.BooleanField(default=True,
                                    verbose_name="上/下架")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="最後確認日期")

    class Meta:
        verbose_name = "廠商管理"
        verbose_name_plural = "廠商管理"

    def __str__(self):
        return self.supplier

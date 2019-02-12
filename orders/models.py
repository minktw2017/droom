from django.db import models
from shop.models import Product


# Create your models here.
class Order(models.Model):
    GENDER_CHOICES = (
        ('male', '先生'),
        ('female', '小姐'),
        ('not-specified', '不指定'),
    )

    STATUS_CHOICES = (
        ('unhandled', '未處理'),
        ('ordered', '已叫貨'),
        ('handling', '處理中'),
        ('return', '退貨'),
    )

    def number():
        no = Order.objects.latest('id').id + 1
        return "CMO-" + str(no).zfill(6)

    no = models.CharField(max_length=20,
                          db_index=True,
                          unique=True,
                          default=number,
                          verbose_name="訂單編號")
    name = models.CharField(max_length=50,
                            db_index=True,
                            verbose_name="姓名")
    gender = models.CharField(max_length=20,
                              choices=GENDER_CHOICES,
                              verbose_name="性別")
    email = models.EmailField(verbose_name="E-mail")
    address = models.CharField(max_length=250,
                               verbose_name="住址")
    postal_code = models.CharField(max_length=20,
                                   verbose_name="郵遞區號")
    city = models.CharField(max_length=100,
                            verbose_name="城市")
    phone = models.CharField(max_length=100,
                             db_index=True,
                             default='',
                             verbose_name="連絡電話")
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="建立時間")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="上次修改")
    paid = models.BooleanField(default=False,
                               verbose_name="查帳完成")
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0],
                              verbose_name="訂單狀態")

    class Meta:
        ordering = ("-created",)
        verbose_name = "訂單"
        verbose_name_plural = "訂單"

    def __str__(self):
        return self.no

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              verbose_name="訂單")
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                verbose_name="訂購商品")
    price = models.DecimalField(max_digits=10,
                                decimal_places=0,
                                verbose_name='商品單價')
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name="訂購數量")

    class Meta:
        verbose_name = "訂購商品"
        verbose_name_plural = "訂購商品"

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

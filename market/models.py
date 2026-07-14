from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Store(models.Model):
    CATEGORIES = [
        ("肉类","肉类"),("海鲜","海鲜"),("素食","素食"),("甜点","甜点"),
    ]
    name = models.CharField("店铺名", max_length=100)
    slug = models.SlugField("URL标识", max_length=100, unique=True)
    category = models.CharField("分类", max_length=10, choices=CATEGORIES)
    description = models.TextField("描述")
    address = models.CharField("地址", max_length=200, blank=True)
    latitude = models.DecimalField("纬度", max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField("经度", max_digits=10, decimal_places=7, null=True, blank=True)
    rating = models.DecimalField("评分", max_digits=2, decimal_places=1, default=0)
    opening_hours = models.CharField("营业时间", max_length=50, default="17:00-02:00")
    phone = models.CharField("电话", max_length=20, blank=True)
    image_url = models.URLField("封面图片", max_length=500, blank=True)
    popularity = models.IntegerField("人气", default=0)
    waiting = models.CharField("排队时间", max_length=20, default="约5分钟")
    spicy = models.BooleanField("辣味", default=False)
    vegetarian = models.BooleanField("素食", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "店铺"
        verbose_name_plural = "店铺"
        ordering = ["-popularity"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store-detail", kwargs={"slug": self.slug})


class Certificate(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="certificates", verbose_name="所属店铺")
    name = models.CharField("证书名称", max_length=100)
    issuer = models.CharField("颁发机构", max_length=100)
    issue_date = models.DateField("颁发日期", null=True, blank=True)
    image_url = models.URLField("证书图片", max_length=500, blank=True)
    description = models.TextField("描述", blank=True)

    class Meta:
        verbose_name = "经营证书"
        verbose_name_plural = "经营证书"

    def __str__(self):
        return f"{self.store.name} - {self.name}"


class StaffMember(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="staff", verbose_name="所属店铺")
    name = models.CharField("姓名", max_length=30)
    role = models.CharField("职位", max_length=30, default="老板")
    avatar_url = models.URLField("头像", max_length=500, blank=True)
    bio = models.TextField("简介", blank=True)
    is_primary = models.BooleanField("主要联系人", default=False)

    class Meta:
        verbose_name = "经营人员"
        verbose_name_plural = "经营人员"

    def __str__(self):
        return f"{self.store.name} - {self.name}({self.role})"


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products", verbose_name="所属店铺")
    name = models.CharField("商品名", max_length=50)
    description = models.TextField("描述", blank=True)
    price = models.CharField("价格", max_length=30, default="¥10/份")
    special_price = models.CharField("优惠价", max_length=30, blank=True)
    image_url = models.URLField("图片", max_length=500, blank=True)
    is_recommended = models.BooleanField("招牌推荐", default=False)
    spicy_level = models.SmallIntegerField("辣度(0-3)", default=0)
    is_vegetarian = models.BooleanField("素食", default=False)

    class Meta:
        verbose_name = "售卖商品"
        verbose_name_plural = "售卖商品"

    def __str__(self):
        return f"{self.store.name} - {self.name}"


class Review(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="reviews", verbose_name="所属店铺")
    nickname = models.CharField("昵称", max_length=30)
    avatar = models.CharField("头像标识", max_length=100, blank=True)
    rating = models.SmallIntegerField("评分(1-5)")
    food = models.CharField("所点美食", max_length=50, blank=True)
    comment = models.TextField("评价内容")
    created_at = models.DateTimeField("评价时间", auto_now_add=True)

    class Meta:
        verbose_name = "食客评价"
        verbose_name_plural = "食客评价"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nickname} - {self.store.name}"


class JoinApplication(models.Model):
    TYPES = [
        ("摊位入驻","摊位入驻"),("求职应聘","求职应聘"),("商务合作","商务合作"),("其他咨询","其他咨询"),
    ]
    STATUS_CHOICES = [
        ("pending","待处理"),("contacted","已联系"),("closed","已关闭"),
    ]
    name = models.CharField("姓名/品牌", max_length=100)
    phone = models.CharField("联系电话", max_length=20)
    application_type = models.CharField("申请类型", max_length=10, choices=TYPES, default="摊位入驻")
    message = models.TextField("留言", blank=True)
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField("申请时间", auto_now_add=True)

    class Meta:
        verbose_name = "入驻/求职申请"
        verbose_name_plural = "入驻/求职申请"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.application_type} ({self.get_status_display()})"


class Event(models.Model):
    STATUS_CHOICES = [
        ("pending", "待审批"),
        ("approved", "已审批"),
        ("published", "已发布"),
        ("archived", "已下架"),
    ]
    TAG_CHOICES = [
        ("热门","热门"), ("音乐","音乐"), ("福利","福利"), ("限定","限定"),
    ]
    title = models.CharField("活动标题", max_length=100)
    date = models.CharField("活动日期", max_length=50)
    description = models.TextField("活动描述")
    tag = models.CharField("标签", max_length=10, choices=TAG_CHOICES, blank=True)
    image_url = models.URLField("图片", max_length=500, blank=True)
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default="pending")
    is_past = models.BooleanField("往期活动", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "活动公告"
        verbose_name_plural = "活动公告"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class TodaySpecial(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="specials", verbose_name="所属店铺")
    name = models.CharField("特价名称", max_length=100)
    description = models.TextField("描述")
    price = models.CharField("价格", max_length=30, default="¥28")
    image_url = models.URLField("图片", max_length=500, blank=True)
    tag = models.CharField("标签", max_length=20, default="主厨特选")
    is_active = models.BooleanField("当前生效", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "今日特价"
        verbose_name_plural = "今日特价"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.store.name}"


class MerchantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="merchant_profile", verbose_name="用户")
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, related_name="merchants", verbose_name="管理的店铺")
    phone = models.CharField("联系电话", max_length=20, blank=True)
    is_approved = models.BooleanField("已获批", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "商家信息"
        verbose_name_plural = "商家信息"

    def __str__(self):
        store_name = self.store.name if self.store else "未分配店铺"
        return f"{self.user.username} - {store_name}"

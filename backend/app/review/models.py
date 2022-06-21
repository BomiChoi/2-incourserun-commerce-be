from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey('user.User', related_name="reviews", on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name="reviews", on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="별점", validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.CharField(verbose_name="내용", max_length = 1000, null=True, blank=True)
    created = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)

    class Meta:
        verbose_name = "리뷰"
        verbose_name_plural = verbose_name


class Photo(models.Model):
    review = models.ForeignKey('review.Review', related_name="photos", on_delete=models.CASCADE)
    img = models.ImageField(verbose_name="이미지", upload_to=None)

    class Meta:
        verbose_name = "리뷰 사진"
        verbose_name_plural = verbose_name


class Reply(models.Model):
    review = models.OneToOneField('review.Review', related_name="reply", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="내용", max_length = 1000)
    created = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)

    class Meta:
        verbose_name = "리뷰 답글"
        verbose_name_plural = verbose_name
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from hitcount.models import HitCountMixin, HitCount
from datetime import datetime
from accounts.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Board(models.Model, HitCountMixin):
    title       = models.CharField(max_length=200, verbose_name="제목")
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name="작성자")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="최종수정일")
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None)
    recruitment_start_date = models.DateField(default=datetime.today)
    recruitment_end_date = models.DateField(default=datetime.today)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    pw = models.CharField(max_length=4)

    def get_hit_count(self):
        return self.hit_count.hits

    def __str__(self):
        return self.title

    class Meta:
        db_table            = 'boards'
        verbose_name        = '게시판'
        verbose_name_plural = '게시판'

class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Portfolio(models.Model):
    p_title = models.CharField(max_length=200)
    p_content = RichTextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    writer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name="작성자")
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.p_title

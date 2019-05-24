from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone
# Create your models here.


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    # ContentType,包含全部模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 储存id号
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadNumExpandMethod():
    def get_read_num(self):    # 传入Blog的实例，固有pk
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0


class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    # ContentType,包含全部模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 储存id号
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

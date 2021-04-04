from django.db import models

# Create your models here.


class BaseModel(models.Model):
       '''
       排序
       '''
       order=models.IntegerField(null=True,blank=True,verbose_name="排序")
       '''
       上架
       '''
       is_show=models.BooleanField(verbose_name="是否上架",default=False)
       '''
       逻辑删除
       '''
       is_delete=models.BooleanField(verbose_name="是否删除",default=False)
       '''
       上传时间
       '''
       create_time=models.DateField(verbose_name="上传时间",auto_now_add=True,null=True,blank=True)

       '''
       更新时间
       '''
       updated_time = models.DateField(verbose_name='更新时间', auto_now=True, null=True, blank=True)
       class Meta:
              '''
              设置为抽象类，不生成表
              '''
              abstract=True


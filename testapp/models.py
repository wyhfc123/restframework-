from django.db import models

# Create your models here.


class Test(models.Model):
    name=models.CharField(max_length=20,null=True,blank=True)
    age=models.SmallIntegerField(null=True)
    salary=models.DecimalField(max_digits=3,decimal_places=2)
    class Meta:
        db_table="test"
        verbose_name="测试"
        verbose_name_plural=verbose_name


class Department(models.Model):
    title=models.CharField(max_length=20, null=True, blank=True)
    class Meta:
        db_table="deptment"
        verbose_name="部门表"
        verbose_name_plural=verbose_name


class User(models.Model):
    choose=(
            (1,"三好员工"),
            (2,"优秀员工"),
            (3,"一般员工")
    )

    comment=models.IntegerField(choices=choose)
    name = models.CharField(max_length=20, null=True, blank=True)
    age = models.SmallIntegerField(null=True)
    dept=models.ForeignKey("Department",on_delete=models.CASCADE)
    class Meta:
        db_table="user"
        verbose_name="用户表"
        verbose_name_plural=verbose_name

from django.contrib.auth.models import AbstractUser
# class UserInfo(AbstractUser):
#     mobile = models.CharField(max_length=15, verbose_name='手机号码', unique=True,null=True,blank=True)
#
#     class Meta:
#         db_table = 'ly_users'
#         verbose_name = '用户'
#         verbose_name_plural = verbose_name



class User01(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    class Meta:
        db_table="user"
        verbose_name="用户表"
        verbose_name_plural=verbose_name

class Order(models.Model):
    title= models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "title"
        verbose_name = "訂單表"
        verbose_name_plural = verbose_name

'''
过滤两张表数据
'''

from models import BaseModel

class Student(BaseModel):
    name = models.CharField('学生名', max_length=20)
    is_del = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Grade(BaseModel):
    name = models.CharField('年级名', max_length=20)
    student = models.ManyToManyField(Student)
    is_del = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class School(BaseModel):
    name = models.CharField('学校名', max_length=20)
    grade = models.ManyToManyField(Grade)
    is_del = models.IntegerField(default=0)

    def __str__(self):
        return self.name


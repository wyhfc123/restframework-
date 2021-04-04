from rest_framework import serializers

from .models import Test
class TestSerializer(serializers.ModelSerializer):
    '''凡是经过序列化的字段，必须在fields中返回'''
    # name=serializers.CharField()
    # age=serializers.IntegerField()
    # salary=serializers.DecimalField(max_digits=3,decimal_places=2,write_only=True)
    '''不写则直接指定列名即可（自由确定返回内容）'''
    class Meta:
        model=Test
        # fields="__all__"
        fields=["id","name",'salary']


class TestSerializer1(serializers.ModelSerializer):
    '''凡是经过序列化的字段，必须在fields中返回'''
    # name=serializers.CharField()
    # age=serializers.IntegerField()
    # salary=serializers.DecimalField(max_digits=3,decimal_places=2,write_only=True)
    '''不写则直接指定列名即可（自由确定返回内容）'''
    class Meta:
        model=Test
        # fields="__all__"
        fields=["id","name",'salary']



from .models import School,Student,Grade
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('name', 'is_del')


class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=True)

    class Meta:
        model = Grade
        fields = ('name', 'is_del', 'student')


class SchoolSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(many=True)

    class Meta:
        model = School
        fields = ('name', 'is_del', 'grade')
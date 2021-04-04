import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import Test
from rest_framework.response import Response
from rest_framework.views import APIView
from .serialzer import TestSerializer
class TestAPIview(APIView):
   def get(self,*args,**kwargs):
       t = Test.objects.all()
       res = TestSerializer(t, many=True)
       return Response(res.data)



'''
分页

（1）写视图类
（2）写分页类，rest_framework.pagination中分页类   PageNumberPagination,LimitOffsetPagination,CursorPagination
（3）对数据进行序列化
PageNumberPagination,CursorPagination等同于下面写法，只需要再继承的时候修改类属性
'''
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination,CursorPagination
class LimitPagination(LimitOffsetPagination):

    '''default_limit:默认返回条数'''
    default_limit = 3
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 5
from .models import Test

class PaginationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        fields="__all__"
class LimitAPIview(APIView):
    def get(self,request,*args,**kwargs):
        test=Test.objects.all()
        pn=LimitPagination()
        #先序列化后分页
        res=pn.paginate_queryset(test,request=request,view=self)
        page=PaginationSerializer(res,many=True)

        '''
        使用get_paginated_response:返回上一页路径和下一页路径
        '''
        return pn.get_paginated_response(page.data)


'''
    权限
    :param  书写认证类（继承authentication里的认证类） ：包括 BaseAuthentication，
            SessionAuthentication，TokenAuthentication，RemoteUserAuthentication，重写这些类的底层方法
    :param  书写认证视图  get post patch delete put方法均可以使用

'''


'''
token值实际工作可以将其存在redis缓存中
'''
token_list = [
    'sfsfss123kuf3j123',
    'asijnfowerkkf9812',
]
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
class isAuthcation(BaseAuthentication):
    def authenticate(self, request):
        '''
        书写权限逻辑
        :param request:
        :return:
        '''
        val=request.query_params.get('token')
        name=request.query_params.get("name")
        print(name,"81")

        if val not in token_list:
            # return exceptions.AuthenticationFailed("用户认证失败")
            return ('登录用户',"用户认证失败")
        # auth = request.META.get('HTTP_AUTHORIZATION', b'')
        # print(auth,'85')
        #('登录用户', '用户token')
        #(request.user,request.auth)
        return ('登录用户', '用户token')

    def authenticate_header(self, request):
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass
class PermissionAPIview(APIView):

    '''

    权限和认证必须在一块儿
    '''
    authentication_classes = [isAuthcation,]
    permission_classes = []

    def get(self,request,*args,**kwargs):
        print(request.user)
        print(request.auth)
        #打印结果 ('登录用户', '用户token')
        return Response({'res1':request.user,'res2':request.auth})


'''
  认证和权限
  :param 先认证，当认证通过时，验证权限，之后两者都通过才返回结果，由一放不通过，则不返回结果
  
'''

user_list=[
    "管理员",
    '会员'
]
from rest_framework.permissions import BasePermission
#权限类
class isPermission(BasePermission):
    message="权限认证失败"
    def has_permission(self, request, view):
        if request.user == "管理员":
            message = "认证成功"
            # return True
            return message

    def has_object_permission(self, request, view, obj):
        '''
        视图继承GenericAPIView，并在其中使用get_object时获取对象时，触发单独对象权限验证
        :param request:
        :param view:
        :param obj:
        :return:
        '''
        if request.user == "管理员":
            message="认证成功"
            # return True
            return message
class isAuthcations(BaseAuthentication):
    def authenticate(self, request):
        val=request.query_params.get('username')
        if val not in user_list:
            return Response("认证失败")

        return (val,'登陆成功')
    def authenticate_header(self, request):
        pass

class Permission_Auth_APIview(APIView):
    # 认证的动作是由request.user触发
    authentication_classes = [isAuthcations,]
    # 循环执行所有的权限
    permission_classes = [isPermission,]
    def get(self,request,*args,**kwargs):
        user=request.user
        status=request.auth
        print(user)
        print(status)
        return Response({"res1":user,"res2":status})
'''

第二种用法
'''
from rest_framework.permissions import BasePermission
class isAuthtication2(BaseAuthentication):
    def authenticate(self, request):
        #对token进行验证
        token=request.query_params.get("token")
        username=request.query_params.get("name")

        if token not in token_list:
            return (username,"认证失败")
        return (username,token)
    def authenticate_header(self, request):
        pass
class isPerssion2(BasePermission):
    message="对不起，您没有权限"
    def has_permission(self, request, view):

        if request.user == "管理员":
            return True


    def has_object_permission(self, request, view, obj):

        if request.user == "管理员":
            return True


class Auth_Permission(APIView):
    authentication_classes = [isAuthtication2,]
    permission_classes = [isPerssion2,]
    def get(self,request,*args,**kwargs):
        user=request.user
        auth=request.auth
        print(user,'202')
        print(auth,'203')
        return Response({"res1":user,"res2":auth})


'''

数据库结合，实际验证权限和认证
'''

from rest_framework.permissions import BasePermission
class isAuthtication3(BaseAuthentication):
    def authenticate(self, request):
        #对token进行验证
        token=request.query_params.get("token")
        username=request.query_params.get("name")

        if token not in token_list:
            return (username,"认证失败")
        return (username,token)
    def authenticate_header(self, request):
        pass
class isPerssion3(BasePermission):
    message="对不起，您没有权限"
    def has_permission(self, request, view):
        print(request.user)
        t = Test.objects.filter(name=request.user)
        if t:
            return True


    def has_object_permission(self, request, view, obj):

        t = Test.objects.filter(name=request.user)
        print(t)
        if t:
            return True
class Auth_Permission1(APIView):
    authentication_classes = [isAuthtication3,]
    permission_classes = [isPerssion3,]
    def get(self,request,*args,**kwargs):
        user=request.user
        auth=request.auth
        return Response({"res1":user,"res2":auth})


'''
    序列化
    :param 书写序列化类(继承serializers的序列化类)
'''

class TestSerializer1(serializers.ModelSerializer):
    '''书写必须fields返回，否则报错'''
    name=serializers.CharField()
    age=serializers.IntegerField()

    class Meta:
        #对某一个model序列化
        model=Test
        '''
        #返回所有字段
        # fields="__all__"
        #只返回id和name字段
        # fields=["id","name"]
        '''
        '''必须返回name,age'''
        fields=["name","age"]

class SerializerAPIview(APIView):
    def get(self,request,*args,**kwargs):
        print(request.user)
        data=Test.objects.all()
        t=TestSerializer1(data,many=True)
        return Response(t.data)


'''
高级序列化，外键查询
'''

from .models import User
from .models import Department
class TestSerializer2(serializers.Serializer):
    '''书写必须fields返回，否则报错'''
    name=serializers.CharField()
    age=serializers.IntegerField()
    dept_id=serializers.IntegerField()
    # ooo = serializers.CharField(source='comment')  # 因为获取是数字，不再调用

    #comment01不能和source等于的一致  source=的是可选项
    comment01=serializers.CharField(source="comment")  #显示数字123
    xxx=serializers.CharField(source="get_comment_display") #显示 1对应的三好员工,2对应的优秀员工, 3对应的一般员工"

    # 外键查询（如果.后面还可以再次调用，则继续调用）
    title=serializers.CharField(source="dept.title")#获得department表中字段内容


class SerializerAPIview2(APIView):
    def get(self,request,*args,**kwargs):
        data=User.objects.filter(name="zhang3")
        t=TestSerializer2(instance=data,many=True)
        return Response(t.data)




from .models import User
from .models import Department
class TestSerializer3(serializers.Serializer):
    '''

    如果是ManyToMany 需要用关联字段.all获取(未写)
    xxx=serializers.CharField(source="dept.all")#获得department表中字段内容
    '''

    info=serializers.SerializerMethodField()  #自定义显示
    def get_info(self,row):
        alist=[]
        user=User.objects.all()
        for i in user:
            if i not in alist:
                alist.append({"id":i.id,"name":i.name})
        return alist

class SerializerAPIview3(APIView):
    def get(self,request,*args,**kwargs):
        data=User.objects.all()
        t=TestSerializer3(instance=data,many=True)
        res = json.dumps(t.data, ensure_ascii=False)
        return HttpResponse(res)



from .models import User
from .models import Department
class TestSerializer4(serializers.ModelSerializer):
    xxxx=serializers.CharField(source="get_comment_display")
    info=serializers.SerializerMethodField() #自定义方法
    class Meta:
        model=User
        fields = ['xxxx',"info"]

    def get_info(self,row):
        alist=[]
        user=User.objects.all()
        for i in user:
            if i not in alist:
                alist.append({"id":i.id,"name":i.name})
        return alist
class SerializerAPIview4(APIView):
    def get(self,request,*args,**kwargs):
        data=User.objects.all()
        t=TestSerializer4(instance=data,many=True)
        return  Response(t.data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
        # 向里面拿几层
        depth=1 #官方建议不要超过1-10层

class UserAPIview(APIView):
    def get(self,*args,**kwargs):
        user=User.objects.all()
        res=UserSerializer(instance=user,many=True)
        return Response(res.data)








'''

HyperlinkedIdentityField:通过从表id生成路径
'''
class UserInfoSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
    # 把名字换成链接地址,# view_name:路由的别名 # lookup_field:根据表指定字段，来拼路径，生成链接 # lookup_url_kwarg：默认是pk，（urls.py中的 publish/(?P<pk>\d+)，指定的pk）可以不写，反向解析有名分组的名字。

    depart=serializers.HyperlinkedIdentityField(view_name="dp",lookup_field="dept_id",lookup_url_kwarg="pk")
    class Meta:
        model=User
        fields=["id","depart"]


class Userinfo(APIView):
    def get(self,request,*args,**kwargs):
        users=User.objects.all()
        ui=UserInfoSerializer(instance=users,many=True,context={"request":request})
        return Response(ui.data)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields="__all__"

class UserAPIview2(APIView):
    def get(self,request,*args,**kwargs):
        '''
        query_params:相当于request.Get.get()
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        pk=request.query_params.get("pk")
        print(pk,"392")
        d=Department.objects.all()
        ds=DepartmentSerializer(instance=d,many=True)
        return Response(ds.data)



'''
    视图
    :param 第一层 mixins.ListModelMixin,generics.GenericAPIView
    :param 第二层 generics.ListAPIView
    :param 第三层 Router+ModelViewSet
'''

'''
:param 第一层
'''


from rest_framework import mixins
from rest_framework import generics
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
class UserModelAPIview(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer  #必须有，否则不能接收get请求
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

'''
第二层
'''

from rest_framework.generics import ListAPIView
class UserModelSerializer1(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
class UserModelAPIview1(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer1
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

'''
第三层
'''

from rest_framework.viewsets import ModelViewSet
class UserModelSerializer2(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

class UserModelAPIview2(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer2
    def get_queryset(self):
        users=User.objects.all()
        return users


'''
频率访问限制
'''


from rest_framework.throttling import BaseThrottle
from rest_framework.settings import api_settings
import time
RECORD={
    "用户ip":["127.0.0.1"]
}


class UserThrottle(BaseThrottle):
    ctime=time.time()
    print(ctime,"488")
    def get_ident(self, request):
        xff=request.META.get("HTTP_X_FORWARDED_FOR")   #检测代理
        remote_addr=request.META.get("REMOTE_ADDR")  #获得访问主机IP地址
        print("xff",xff)
        # print("remote_addr",remote_addr)
        num_proxies = api_settings.NUM_PROXIES   #设置最大代理数
        # print("num_proxies",num_proxies)
        if num_proxies is not None:
            if num_proxies==0 or xff is None:
                return remote_addr
            addrs=xff.split(",")  #对代理进行切割
            client_addr=addrs[-min(num_proxies, len(addrs))]
            return client_addr.strip()

        return ''.join(xff.split()) if xff else remote_addr   #返回127.0.0.1
    def allow_request(self, request, view):
        """
            是否仍然在允许范围内
            Return `True` if the request should be allowed, `False` otherwise.
            :param request:
            :param view:
            :return: True，表示可以通过；False表示已超过限制，不允许访问
        """
        #允许一分钟访问三次
        num_request=3
        time_request=60
        now=self.ctime
        print(self.ctime,'516')  #拿到的时间戳是一样的
        ident=self.get_ident(request)   #127.0.0.1
        self.ident=ident  #创建类属性
        if ident not in RECORD:
            #存放时间戳{"127.0.0.1":[时间戳,]}
            RECORD[ident]=[now,]
            return True
        print(RECORD)
        history=RECORD[ident]
        print(now - time_request,'524')
        # 当新时间戳-60秒大于旧的时间戳 就从字典中删除（说明新老时间戳已超60秒，可以正常访问）
        while history and history[-1] <= now - time_request:
            history.pop()
        #根据时间列表长度判断请求几次
        #[新时间1，新时间2，旧时间]
        if len(history)<num_request:
            #如果小于，则添加
            history.insert(0,now)
            return True


    def wait(self):
        #取新时间
        last_time=RECORD[self.ident][0]
        now=self.ctime
        print(last_time,'541')
        print(now,'542')
        # 旧时间减去新时间为负数，当相加为0时，限制解除
        return int(60+last_time-now)

class UserView(APIView):
    throttle_classes = [UserThrottle,]
    def get(self, request,*args,**kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')



'''
SimpleRateThrottle 基于缓存

'''
from rest_framework.throttling import SimpleRateThrottle

class TestThrottle(SimpleRateThrottle):
    #seetings文件中全局配置的
    scope = "test_scope"
    def get_cache_key(self, request, view):
        print(request.user,'565')
        if not request.user:
            ident=self.get_ident(request)
            # print(ident,'567')

        else:
            ident=request.user
        # ident :AnonymousUser  走的else
        print(ident,'*********')

        #self.scope   test_scope：settings配置内容
        print(self.scope,'571')
        return self.cache_format%{
            "scope":self.scope,
            'ident':ident
        }
class TestView(APIView):
    throttle_classes = [TestThrottle, ]

    def get(self, request, *args, **kwargs):
        # self.dispatch
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')


    def throttled(self, request, wait):
        """
            访问次数被限制时，定制错误信息
        """

        class Throttled(exceptions.Throttled):
            default_detail = '请求被限制.'
            extra_detail_singular = '请 {wait} 秒之后再重试.'
            extra_detail_plural = '请 {wait} 秒之后再重试.'

        raise Throttled(wait)

'''
view限制请求频率  ScopedRateThrottle
'''
from rest_framework.throttling import ScopedRateThrottle
class Test1Throttle(ScopedRateThrottle):
    def get_cache_key(self, request, view):
        if not request.user:
            ident=self.get_ident(request)
        else:
            ident=request.user
        return self.cache_format%{
            "scope":self.scope,
            "ident":ident
        }

class TestAPIView(APIView):
    throttle_classes = [Test1Throttle,]
    throttle_scope="test_scope"  #写在view当中，而SimpleRateThrottle写在限制类当中
    def get(self, request,*args,**kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')
    def throttled(self, request, wait):
        '''
        访问次数被限制时，定制错误信息
        :param request:
        :param wait:
        :return:
        '''
        class Throtted(exceptions.Throttled):
            default_detail = "请求已被限制"
            extra_detail_singular = '请 {wait} 秒之后再重试.'
            extra_detail_plural = '请 {wait} 秒之后再重试.'
        raise Throtted(wait)


'''
匿名时用IP限制+登录时用Token限制
'''

class Test2Throttle(SimpleRateThrottle):
    scope = "luffy_anon"
    def get_cache_key(self, request, view):
        if request.user:
            return None
        ident=self.get_ident(request)
        return self.cache_format%{
            "scope":self.scope,
            "ident":ident
        }





class Test3Throttle(SimpleRateThrottle):
    scope = "luffy_user"

    def get_ident(self, request):
        """
            认证成功时：request.user是用户对象；request.auth是token对象
            :param request:
            :return:
        """
        return "user_token"

    def get_cache_key(self, request, view):

        # 未登录用户，则跳过 Token限制
        if not request.user:
            return None
        ident=self.get_ident(request)
        return self.cache_format%{
            "scope":self.scope,
            "ident":ident
        }
class Test3View(APIView):
    throttle_classes = [Test3Throttle,Test2Throttle]
    def get(self, request,*args,**kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')


'''
总结
AonRateThrottle
限制所有匿名未认证的用户。
使用DEFAULT_THROTTLE_RATES['anon'] 来设置频次


UserRateThrottle

限制认证用户，使用User id 来区分。
使用DEFAULT_THROTTLE_RATES['user'] 来设置频次



ScopedRateThrottle

限制用户对于每个视图的访问频次，使用ip或user id。


'''



'''
版本

'''
'''
a.基于get传参
'''
from rest_framework.versioning import QueryParameterVersioning

class TestAPIviews(APIView):
    versioning_class = QueryParameterVersioning
    def get(self,request,*args,**kwargs):
        print(request.version)
        print(request.versioning_scheme)
        reverse_url=request.versioning_scheme.reverse("bn",request=request)
        print(reverse_url)
        return Response(reverse_url)
'''
    b.基于正则
'''
from rest_framework.versioning import URLPathVersioning
class VersionView(APIView):
    versioning_class = URLPathVersioning
    def get(self,request,*args,**kwargs):
        print(request.version)
        print(request.versioning_scheme)
        version=request.versioning_scheme.reverse("bn1",request=request)
        print(version)
        return Response(version)

'''
基于请求头的 accept(未获得具体结果)
'''
from rest_framework.versioning import AcceptHeaderVersioning

class VersionHeaderAPIview(APIView):
    versioning_class = AcceptHeaderVersioning
    def get(self,request,*args,**kwargs):
        print(request.version)
        # 获取版本管理的类
        print(request.versioning_scheme)
        # 反向生成URL
        reverse_url = request.versioning_scheme.reverse('bn3', request=request)
        print(reverse_url)
        return Response(reverse_url)

'''

基于主机IP的
'''

from rest_framework.versioning import HostNameVersioning
class VersionHostNameAPIview(APIView):
    versioning_class = HostNameVersioning
    def get(self,request,*args,**kwargs):
        print(request.version)
        print(request.versioning_scheme)
        version_url=request.versioning_scheme.reverse("bn4",request=request)
        return Response(version_url)






'''
解析器
:param 根据请求头 content-type 选择对应的解析器就请求体内容进行处理。
'''
'''
仅处理请求头content-type为application/json的请求体
'''

from rest_framework.parsers import JSONParser
class JsonParserAPIView(APIView):
    parser_classes = [JSONParser]
    def get(self,request,*args,**kwargs):
        # 获取请求的值，并使用对应的JSONParser进行处理
        print(request.data)

        print(request.content_type)   #text/plain

        # application/x-www-form-urlencoded 或 multipart/form-data时，request.POST中才有值
        print(request.POST)
        print(request.FILES)
        return Response('POST请求，响应内容')

'''
b. 仅处理请求头content-type为application/x-www-form-urlencoded 的请求体    FormParser

'''
from rest_framework.parsers import FormParser


'''
 仅处理请求头content-type为multipart/form-data的请求体    MultiPartParser
'''
from rest_framework.parsers import MultiPartParser



'''
d. 仅上传文件   FileUploadParser

'''

from rest_framework.parsers import FileUploadParser

'''
渲染器
'''
'''
a. json
'''
from rest_framework.renderers import JSONRenderer
class TestRenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
class TestRenderAPIView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self,request,*args,**kwargs):
        users=User.objects.all()
        tr=TestRenderSerializer(users,many=True)
        return Response(tr.data)

'''
b. 表格
'''
from rest_framework.renderers import AdminRenderer
class TestRenderSerializer1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
class TestRenderAPIView1(APIView):
    renderer_classes = [AdminRenderer]
    def get(self,request,*args,**kwargs):
        users=User.objects.all()
        tr=TestRenderSerializer1(users,many=True)
        return Response(tr.data)


'''
c. Form表单
'''

from rest_framework.renderers import HTMLFormRenderer
class TestRenderSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
class TestRenderAPIView2(APIView):
    renderer_classes = [HTMLFormRenderer]
    def get(self,request,*args,**kwargs):
        users=User.objects.all().first()
        tr=TestRenderSerializer2(users,many=False)
        return Response(tr.data)

'''
d. 自定义显示模板 TemplateHTMLRenderer（未做）
'''

from rest_framework.renderers import TemplateHTMLRenderer
class TestRenderSerializer3(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TestView3(APIView):
    renderer_classes = [TemplateHTMLRenderer, ]

    def get(self, request, *args, **kwargs):
        user_list =User.objects.all().first()
        ser = TestRenderSerializer3(instance=user_list, many=False)
        #写一个user_detail.html文件
        return Response(ser.data, template_name='user_detail.html')
'''
路由
'''

class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RouterAPIview(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RouterSerializer





'''
频率访问限制，权限，认证结合

'''
from rest_framework.throttling import SimpleRateThrottle

class BaseAuthtications(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token")
        name = request.query_params.get("name")
        if token not in token_list:
            return (name, "认证失败")
        return (name, "认证成功！")
    def authenticate_header(self, request):
        token = request.query_params.get("token")
        name = request.query_params.get("name")

        password = request.query_param.get("pwd")
        if token not in token_list :
            return (name, "认证失败")
        return (name,"认证成功！")

class BasePermissions(BasePermission):
    message="请获取权限"
    def has_permission(self, request, view):
        name=request.query_params.get("name")
        users=User.objects.filter(name=name).first()

        if users:
            return True
    def has_object_permission(self, request, view, obj):
        name = request.query_params.get("name")
        users = User.objects.filter(name=name)
        if users:
            return True
class TestThrottle01(SimpleRateThrottle):
    #seetings文件中全局配置的
    scope = "test_scope"
    def get_cache_key(self, request, view):
        print(request.user,'565')
        if not request.user:
            ident=self.get_ident(request)
            # print(ident,'567')

        else:
            ident=request.user
        # ident :AnonymousUser  走的else
        print(ident,'*********')

        #self.scope   test_scope：settings配置内容
        print(self.scope,'571')
        return self.cache_format%{
            "scope":self.scope,
            'ident':ident
        }

class TestSerialzizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
class TestView01(APIView):
    authentication_classes = [BaseAuthtications,]
    permission_classes = [BasePermissions]
    throttle_classes = [TestThrottle01, ]

    def get(self, request, *args, **kwargs):
        user=User.objects.all()
        ts=TestSerialzizer(instance=user,many=True)
        print(request.user)
        print(request.auth)
        if request.user:
            if request.auth == "认证失败":
                return Response({"res1": request.user, "res2": request.auth})
            return Response(ts.data)
    def throttled(self, request, wait):
        """
            访问次数被限制时，定制错误信息
        """
        class Throttled(exceptions.Throttled):
            default_detail = '请求被限制.'
            extra_detail_singular = '请 {wait} 秒之后再重试.'
            extra_detail_plural = '请 {wait} 秒之后再重试.'
        raise Throttled(wait)

from rest_framework.generics import ListAPIView
from .models import Test
from .serialzer import TestSerializer1
class Test5APIview(ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer1






    







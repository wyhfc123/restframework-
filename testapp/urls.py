from django.urls import path,re_path,include
from .views import TestAPIview,LimitAPIview,PermissionAPIview,Permission_Auth_APIview,\
    Auth_Permission,Auth_Permission1,SerializerAPIview,SerializerAPIview2,SerializerAPIview3,\
    SerializerAPIview4,UserAPIview,UserAPIview2,Userinfo,UserModelAPIview,UserModelAPIview1\
    ,UserModelAPIview2,UserView,TestView,TestAPIView,Test3View,TestAPIviews,VersionView,\
    VersionHeaderAPIview,VersionHostNameAPIview,JsonParserAPIView,TestRenderAPIView,\
    TestRenderAPIView1,TestRenderAPIView2,TestView3,RouterAPIview,TestView01,Test5APIview

''' 
    路由
    :param  全自动路由
'''
from rest_framework import routers
router=routers.DefaultRouter()
router.register("last_test",RouterAPIview)

urlpatterns=[
    path("testview/",TestAPIview.as_view()),

    #分页
    path("page/",LimitAPIview.as_view()),
    #权限
    path("per/",PermissionAPIview.as_view()),
    #认证
    path("per_auth/",Permission_Auth_APIview.as_view()),
    path("per_auth2/",Auth_Permission.as_view()),
    path("per_auth3/",Auth_Permission1.as_view()),
    #序列化
    path("ser/",SerializerAPIview.as_view()),
    path("ser2/",SerializerAPIview2.as_view()),
    path("ser3/",SerializerAPIview3.as_view()),
    path("ser4/",SerializerAPIview4.as_view()),
    path("ser5/",UserAPIview.as_view()),
    path("ser6/",Userinfo.as_view()),
    #反向生成url
    re_path(r"^(?P<pk>\d+)",UserAPIview2.as_view(),name="dp"),
    #视图
    path(r"uma/",UserModelAPIview.as_view()),
    path(r"uma1/",UserModelAPIview1.as_view()),
    path(r"uma2/",UserModelAPIview2.as_view({"get":"list"})),
    #访问频率限制
    path(r"uview/",UserView.as_view()),
    path(r"tview/",TestView.as_view()),
    path(r"taview/",TestAPIView.as_view()),
    path(r"tsview/",Test3View.as_view()),
    #版本
    path(r"bn/",TestAPIviews.as_view(),name="bn"),
    #声明版本[v1|v2]
    re_path(r"^(?P<version>[v1|v2]+)/bn1/",VersionView.as_view(),name="bn1"),
    path(r"bn3/",VersionHeaderAPIview.as_view(),name="bn3"),
    path(r"bn4/",VersionHostNameAPIview.as_view(),name="bn4"),
    #解析器
    path(r"jp/",JsonParserAPIView.as_view(),name="jp"),
    #渲染器
    re_path(r'(?P<version>[v1|v2]+)/tr/', TestRenderAPIView.as_view()),
    path('tr1/',TestRenderAPIView1.as_view()),
    path('tr2/',TestRenderAPIView2.as_view()),
    path('tr3/',TestView3.as_view()),


    #注册全自动路由
    path('',include(router.urls)),

    #测试 权限+认证+频率访问限制
    path("tvi/",TestView01.as_view()),
    path("ttt/",Test5APIview.as_view()),




]

# from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view



from HRCS.api import  ForgetPassword, ResetPassword, Login, \
    RefreshJWTToken, getEmpdata, getEmpdata2, getUserdata, getCompanydata, getGroupdata, delGroupdata, getDepdata, \
    verifyReset, getWorkpositionList, delWorkposition, putLocationdata, getLocationdata, delLocationdata, \
    getEmpLocationdata, getEmpGroupdata, delLineIddata, getUserMenu, getUserMenuList, getAuthdata, delAuthdata, \
    getAuthMenudata, putAuthMenudata, getAttendancedata, getPunchTableQuery, getPunchOvertimeQuery,reset_all_password

urlpatterns = [
    path('clockInlinebot/', include('clockInlinebot.urls')), #包含應用程式的網址


    path('HRCS/ForgetPassword', ForgetPassword),
    path('HRCS/ResetPassword', ResetPassword),
    path('HRCS/Login', Login),
    path('HRCS/RefreshJWTToken', RefreshJWTToken),
    path('HRCS/getShiftsAttendanceEmpViewQuery', getPunchTableQuery),#上下班打卡查詢
    path('HRCS/getWorkOvertimeQuery', getPunchOvertimeQuery),#簽到退打卡查詢
    path('HRCS/getEmpdata', getEmpdata),
    path('HRCS/getEmpdata2', getEmpdata2),
    path('HRCS/getUserdata', getUserdata),
    path('HRCS/getCompanydata', getCompanydata),
    path('HRCS/getGroupdata', getGroupdata),
    path('HRCS/delGroupdata/<slug:group_no>', delGroupdata),#del
    path('HRCS/getDepdata', getDepdata),
    path('HRCS/verifyReset', verifyReset),
    path('HRCS/getWorkpositionList', getWorkpositionList),
    path('HRCS/delWorkposition/<slug:wp_code>', delWorkposition),#del
    path('HRCS/putLocationdata', putLocationdata),
    path('HRCS/getLocationdata', getLocationdata),
    path('HRCS/delLocationdata/<slug:id>', delLocationdata),#del
    path('HRCS/getEmpLocationdata/<slug:location_id>', getEmpLocationdata),
    path('HRCS/getEmpGroupdata/<slug:location_id>', getEmpGroupdata),



    path('HRCS/delLineIddata', delLineIddata),#del
    path('HRCS/menu/<slug:emp_no>', getUserMenu),
    path('HRCS/menu', getUserMenuList),
    path('HRCS/getAuthdata', getAuthdata),
    path('HRCS/delAuthdata/<slug:auth_no>', delAuthdata),#del
    path('HRCS/getAuthMenudata/<slug:auth_no>', getAuthMenudata),
    path('HRCS/getAuthMenudata', putAuthMenudata),
    path('HRCS/getAttendancedata/<slug:attendance_type>', getAttendancedata),

    path('HRCS/reset_all_password', reset_all_password)


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
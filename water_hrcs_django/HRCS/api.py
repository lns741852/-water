from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
import json
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.db.models import Q
from datetime import datetime as dt, timedelta
from functools import reduce
import operator
import datetime
import jwt
import secrets
import calendar
from django.core.mail import send_mail
from HRCS import Geocoding
from HRCS.apis import get_attendance, insert_user_data, update_user_data, jwt_verify
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from HRCS.log import record_action_log
from HRCS.models import  Token, EmpTable, EmpLocationTable, MenuTable, AuthMenu, AuthTable, EmpAndGroupTable, JwtToken,\
     CompanyTable, EmpTable_AUTH, GroupTable, DepTable, WorkpositionList, LocationTable, PunchTable, PunchOvertime


gmap = Geocoding()

@require_GET
def reset_all_password(request):#重設所有密碼
    # all_emptable=EmpTable.objects.all()
    # try:
    #     for emp in all_emptable:
    #
    #         first_password = "QhrGVE%sVDdYgdM" % str(emp.emp_no)
    #         print(first_password)
    #         password = make_password(first_password)
    #         emp.user_pwd=password
    #         emp.save()
    #     return JsonResponse({'status': "success"})
    # except Exception as e:
    #     return e
    return JsonResponse({'status': "cant use"})


@require_GET
def getDepdata(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_dep_data(request)})

@csrf_exempt
@require_http_methods(["POST"])
def verifyReset(request: WSGIRequest):
    if request.method == 'POST':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _verify_reset(request)})


@csrf_exempt
@require_http_methods(["POST","GET","PUT"])
def getGroupdata(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_group_data(request)})
    if request.method == 'POST':
        return JsonResponse({'status': _insert_group_data(request)})
    if request.method == 'PUT':
        return JsonResponse({'status': _update_group_data(request)})


@require_GET
def getAuthMenudata(request: WSGIRequest,auth_no):
    if request.method == 'GET':
        return JsonResponse({'Response': _get_auth_menu_data(request,auth_no)})

@csrf_exempt
def putAuthMenudata(request: WSGIRequest):
        return JsonResponse({'status': _update_auth_menu_data(request)})


@csrf_exempt
@require_http_methods(["POST","GET","PUT"])
def getAuthdata(request: WSGIRequest):
    if request.method == 'GET':
        return JsonResponse({'Response': _get_auth_data(request)})
    if request.method == 'POST':
        return JsonResponse({'Response': _insert_auth_data(request)})
    if request.method == 'PUT':
        return JsonResponse({'status': _update_auth_data(request)})

@csrf_exempt
def delAuthdata(request: WSGIRequest,auth_no):
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _del_auth_data(request,auth_no)})

@csrf_exempt
def delGroupdata(request: WSGIRequest,group_no):
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _del_group_data(request,group_no)})


@csrf_exempt
@require_http_methods(["POST","GET","PUT"])
def getWorkpositionList(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_WorkpositionList(request)})
    if request.method == 'POST':
        return JsonResponse({'status': _insert_WorkpositionList(request)})
    if request.method == 'PUT':
        return JsonResponse({'status': _update_WorkpositionList(request)})
@csrf_exempt
def delWorkposition(request: WSGIRequest,wp_code):
        return JsonResponse({'status': _delete_WorkpositionList(request,wp_code)})


@require_GET
def getCompanydata(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_company_data(request)})

@require_GET
def getPunchOvertimeQuery(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_punch_overtime_query(request)})


@require_GET
def getPunchTableQuery(request: WSGIRequest):
    if request.method == 'GET':
        return JsonResponse({'Response': _get_punchtable_query(request)})

@csrf_exempt
@require_POST
def Login(request: WSGIRequest):  # 登入測試
    if request.method == 'POST':
        return JsonResponse({'Response': _login(request)})
@csrf_exempt
@require_http_methods(["POST","GET","PUT"])
def getEmpdata(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_emp_data(request)})
    if request.method == 'POST':
        return JsonResponse({'status': _insert_emp_data(request)})
    if request.method == 'PUT':
        return JsonResponse({'status': _update_emp_data(request)})


@require_GET
def getEmpdata2(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_emp_data2(request)})

@csrf_exempt
@require_http_methods(["POST","PUT"])
def getUserdata(request: WSGIRequest):
    if request.method == 'POST':
        return JsonResponse(insert_user_data(request))
    if request.method == 'PUT':
        return JsonResponse(update_user_data(request))



@require_GET
def getAttendancedata(request: WSGIRequest, attendance_type):
    if request.method == 'GET':
        return JsonResponse(get_attendance(request, attendance_type))



@csrf_exempt
@require_POST
def RefreshJWTToken(request: WSGIRequest):  # 登入測試
    if request.method == 'POST':
        return JsonResponse({'Response': _refresh_jwt_token(request)})
@csrf_exempt
@require_POST
def ForgetPassword(request: WSGIRequest):
    if request.method == 'POST':
        return JsonResponse({'status': _forget_password(request)})
    else:
        return JsonResponse({'status': 'error'})

@csrf_exempt
@require_POST
def ResetPassword(request: WSGIRequest):
    if request.method == 'POST':
        return JsonResponse({'status': _reset_password(request)})
    else:
        return JsonResponse({'status': 'error'})

@csrf_exempt
@require_http_methods(["PUT"])
def putLocationdata(request: WSGIRequest):
    if request.method == 'PUT':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _update_location_check_data(request)})

@csrf_exempt
@require_http_methods(["POST","GET","PUT"])
def getLocationdata(request: WSGIRequest):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_location_data(request)})
    if request.method == 'POST':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _insert_location_data(request)})
    if request.method == 'PUT':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _update_location_data(request)})

@csrf_exempt
def delLocationdata(request: WSGIRequest, id):
    if request.method == 'DELETE':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _delete_location_data(request, id)})

@csrf_exempt
@require_http_methods(["PUT","GET"])
def getEmpLocationdata(request: WSGIRequest, location_id):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_emp_location_data(request, location_id)})
    if request.method == 'PUT':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _update_emp_location_data(request, location_id)})

@csrf_exempt
@require_http_methods(["GET"])
def getEmpGroupdata(request: WSGIRequest, location_id):
    if request.method == 'GET':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _get_emp_group_data(request, location_id)})

       
@csrf_exempt
@require_http_methods(["PUT"])
def delLineIddata(request: WSGIRequest):
    if request.method == 'PUT':
        # 如果要用到其他資料表的，在這裡再多一個逗號對應不同的資料表就行
        return JsonResponse({'Response': _delete_line_id_data(request)})


@require_GET
def getUserMenu(request: WSGIRequest,emp_no):
    if request.method == 'GET':
        return JsonResponse({'Response': _get_userMenu_data(request,emp_no)})


@require_GET
def getUserMenuList(request: WSGIRequest):
    if request.method == 'GET':
        return JsonResponse({'Response': _get_userMenuList_data(request)})


def _get_dep_data(request):
    try:
        jwt_verify(request)
        all_posts = DepTable.objects.all()
        posts = []

        for _post in all_posts:  # 按照api格式塞進去
            post_data = {  # 按照api格式塞進去
            'dep_no':_post.dep_no,
            'dep_name':_post.dep_name,
             }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
        return Response


def _login(request):
    requestBody = request.body
    requestData = json.loads(requestBody)
    username = requestData['username']
    password = requestData['password']
    errorMsg='error!'
    posts = []
    try:
        user = authenticate(username=username, password=password)
        if user is not None and user.working:
            payload = {
            'iss': 'CGPT',#改
            'sub': user.emp_name,
            'aud': 'CGPT',#改
            'iat': dt.utcnow(),
            'username': user.emp_name,
            'password':user.user_pwd
            }
            try:
                token=jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')#遠端
            except:
                token=jwt.encode(payload, 'secret', algorithm='HS256')

            #於雲端主機進行回傳時 必須轉換成字串 否則會觸發500error
            #最大肇因是因為python3跟python2encode時的差異 但本地端python3不知道為啥跑不起來
            exp_time=(dt.utcnow()+datetime.timedelta(days=1)+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")#一天有效時間&時區補正
            created = JwtToken.objects.get_or_create(username=username)
            if created:#如果已經存在jwt_token
                _post =  JwtToken.objects.filter(username=username)
                _post.update(
                token=token,
                exp_time=exp_time
                )
            else:#如果資料庫尚未存在此jwt_tokem
                JwtToken.objects.create(
                    username=username,
                    token=token,
                    exp_time=exp_time
                )
            # person just refers to the existing one
            post_data={
                    'emp_no': user.emp_no,
                    'emp_name': user.emp_name,
                    'auth': user.auth,
                    'group_no': user.group_no,
                    'dep_no': user.dep_no,
                    'group_leader': user.group_leader,
                    'token': token,
            }
            posts.append(post_data)
        else:
            raise Exception('list index out of range')
        return posts

    except Exception as e:
        if 'list index out of range' in str(e):
            errorMsg += '請重新確認輸入內容!'
        else:
            errorMsg += str(e)
        return errorMsg


def _get_auth_menu_data(request,auth_no):
    print("========")
    print(auth_no)
    try:
        jwt_verify(request)

        all_posts = AuthMenu.objects.filter(auth_no=auth_no)
        posts = []

        for _post in all_posts:  # 按照api格式塞進去
            posts.append(_post.menu_no)


        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
            #return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
    return Response



def _update_auth_menu_data(request):


    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response

    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'
    try:

        AuthMenu.objects.filter(auth_no=requestData['auth_no']).delete()

        for menu_no in requestData['menuList']:
            AuthMenu.objects.create(
                id=0,
                auth_no =requestData['auth_no'],
                menu_no=menu_no,
            )

    except Exception as e:
        errorMsg += str(e)
        return errorMsg

    return 'Succeed'


def _get_group_data(request):
    try:
        jwt_verify(request)
        all_posts = GroupTable.objects.all()
        posts = []

        for _post in all_posts:  # 按照api格式塞進去
            post_data = {  # 按照api格式塞進去
            'group_no': _post.group_no,
            'group_name': _post.group_name,
             }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
                }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
        return Response


def _insert_group_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response

    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = 'ERROR!'

    try:
        GroupTable.objects.create(
            group_no =requestData['group_no'],
            group_name=requestData['group_name'],
        )
    except Exception as e:
        if 'Duplicate entry' in str(e):
            errorMsg += '該編號重複，請再確認編號'
        else:
            errorMsg += str(e)
        return errorMsg

    return 'Succeed'


def _update_group_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response

    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'

    try:
        _post = GroupTable.objects.filter(group_no=requestData['group_no'])
        _post.update(
            group_name=requestData['group_name'],
        )
    except Exception as e:
        errorMsg += str(e)
        return errorMsg
    return 'Succeed'


def _del_group_data(request, group_no):
    try:
        jwt_verify(request)
    except Exception as e:
        Response = {
                'status': 'Error',
                'msg': str(e)
            }
        return Response

    errorMsg = '刪除錯誤!'

    try:
        _posts = EmpTable.objects.filter(group_no=group_no)

        if len(_posts) > 0:
            errorMsg += '群組被使用中'
            raise Exception("group is using!")
        GroupTable.objects.filter(group_no=group_no).delete()
        # _post = ShiftsTable.objects.filter(shift_no=shiftno)
        # print(_post)
    except Exception as e:
        return errorMsg

    return 'Succeed'



def _get_auth_data(request):
    try:
        jwt_verify(request)

        all_posts = AuthTable.objects.all()
        posts = []

        for _post in all_posts:  # 按照api格式塞進去
            post_data = {  # 按照api格式塞進去
            'id':_post.id,
            'auth_no':_post.auth_no,
            'auth_name':_post.auth_name,
             }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
            #return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
    return Response

def _insert_auth_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response

    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = 'ERROR!'

    try:
        AuthTable.objects.create(
            id =0,
            auth_no=requestData['auth_no'],
            auth_name=requestData['auth_name'],
            create_date = dt.utcnow()
        )
    except Exception as e:
        if 'Duplicate entry' in str(e):
            errorMsg += '該編號重複，請再確認編號'
        else:
            errorMsg += str(e)
        return errorMsg

    return 'Succeed'



def _update_auth_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response

    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'

    try:
        _post = EmpTable.objects.filter(emp_no=requestData['emp_no'])
        _post.update(
            auth=requestData['auth'],
        )
    except Exception as e:
        errorMsg += str(e)
        return errorMsg
    return 'Succeed'

def _del_auth_data(request, auth_no):
    try:
        jwt_verify(request)
    except Exception as e:
        Response = {
                'status': 'Error',
                'msg': str(e)
            }
        return Response

    errorMsg = '刪除錯誤!'

    try:
        _posts = EmpTable.objects.filter(auth=auth_no)


        if len(_posts) > 0:
            raise Exception("auth is using!")

        AuthTable.objects.filter(auth_no=auth_no).delete()
        AuthMenu.objects.filter(auth_no=auth_no).delete()

        # _post = ShiftsTable.objects.filter(shift_no=shiftno)
        # print(_post)
    except Exception as e:
        return errorMsg

    return 'Succeed'



def _get_company_data(request):
    try:
        jwt_verify(request)
        all_posts = CompanyTable .objects.all()

        posts = []

        for _post in all_posts:  # 按照api格式塞進去
            post_data = {  # 按照api格式塞進去
            'comp_no':_post.comp_no,
            'comp_name':_post.comp_name,
            'main':_post.main
            }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
        return Response


def _get_userMenuList_data(request):
    try:
        jwt_verify(request)

        all_posts = MenuTable.objects.filter(Q(parent_no=None))
        posts = []

        for _post in all_posts:  # 按照api格式塞進去

            children_posts = MenuTable.objects.filter(Q(parent_no=_post.menu_no))
            posts2 = []

            for children in children_posts:
                post_data2 = {  # 按照api格式塞進去
                'id':children.id,
                'menu_no':children.menu_no,
                'menu_name':children.menu_name,
                'url':children.url,
                }

                posts2.append(post_data2)

            post_data = {  # 按照api格式塞進去
            'id':_post.id,
            'menu_no':_post.menu_no,
            'menu_name':_post.menu_name,
            'url':_post.url,
            'children':posts2,
            }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
            #return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
    return Response

def _get_userMenu_data(request,emp_no):
    try:
        jwt_verify(request)

        empSet = EmpTable.objects.filter(Q(emp_no=emp_no))

        menuSet = AuthMenu.objects.filter(Q(auth_no=empSet[0].auth))

        menuList = []

        for menu in menuSet:
            menuList.append(menu.menu_no)

        Response = {
            'status': 'Succeed',
            'data': menuList
        }

    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }


    return Response





def _refresh_jwt_token(request):  # 更新jwttoken
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '無法更新token有效時間!'

    try:
        _post = JwtToken.objects.filter(token=requestData['token'])
        exp_time= dt.strptime(_post[0].exp_time.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
        nowtime = dt.strptime(str((dt.utcnow()+datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
        print(exp_time)
        print(nowtime)
        if nowtime-exp_time<timedelta(seconds=0):#現在時間減去過期時間 大於0代表已過期
            exp_time=(dt.utcnow()+datetime.timedelta(days=1)+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")#一天有效時間&時區補正
            _post.update(
                exp_time=exp_time
            )
        else:
            raise Exception("over limit!")

    except Exception as e:
        if 'over limit!' in str(e):
            errorMsg+="token已過期!"
        elif 'list index out of range' in str(e):
            errorMsg+="查無此token!"
        else:
            errorMsg += str(e)
        return errorMsg

    return 'Succeed'



def _verify_reset(request):

    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '驗證失敗!'
    # print("in")
    try:
        _token= Token.objects.filter(token=requestData['token'])#從token資料表取出該名員工的token
        nowtime = dt.strptime(str((dt.utcnow()+datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
        deadline=dt.strptime(str(_token[0].deadline.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
        if nowtime-deadline<timedelta(seconds=0):
            Response = {
                'status': 'Succeed',
                'emp_no': _token[0].emp_no
            }
        else:
            errorMsg += '驗證碼已過期!'
            Response = {
                'status': 'Error',
                'msg': errorMsg
            }

    except Exception as e:
        if 'list index out of range' in str(e):
            errorMsg += '驗證碼不存在!'
        else:
            errorMsg += str(e)
        Response = {
            'status': 'Error',
            'msg': errorMsg
        }
    return Response


def _reset_password(request):  # 忘記密碼重設請求_驗證
    try:
        jwt_verify(request)
    except Exception as e:
        Response = {
                'status': 'Error',
                'msg': str(e)
            }
        return Response
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改失敗!'
    # print("in")
    try:
        _post = EmpTable.objects.filter(emp_no=requestData['emp_no'])
        print("yes")
        _post.update(user_pwd=make_password(requestData['password']))  # 更新密碼
        return 'Succeed'
    except Exception as e:
        if 'list index out of range' in str(e):
            errorMsg += '查無此帳號!請重新確認輸入內容!'
        else:
            errorMsg += str(e)
        return errorMsg


def _forget_password(request):#忘記密碼驗證&寄出驗證信
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '寄送失敗!'
    # print("in")
    try:
        _post = EmpTable.objects.filter(Q(emp_no=requestData['emp_no']) & Q(mail=requestData['mail']))
        email=_post[0].mail#確保是使用者的信箱
        deadline=requestData['deadline']
        token=secrets.token_urlsafe(20)#產生亂數token
        url=requestData['url']
        created = Token.objects.get_or_create(emp_no=requestData['emp_no'])
        if created:#如果已經存在jwt_token
            _post =  Token.objects.filter(emp_no=requestData['emp_no'])
            _post.update(
            token=token,
            deadline=deadline
            )
        else:#如果資料庫尚未存在此jwt_tokem
            Token.objects.create(#紀錄重置密碼的token
            emp_no=requestData['emp_no'],
            token=token,
            deadline=deadline
            )

        print(token)
        send_mail('密碼重設信件', '您好，請透過以下連結進行密碼重設的動作:\n'+url+token+'\n如果無法點擊連結，請將網址複製貼上至瀏覽器即可。 ', 'cgptiot@gmail.com', [email])
        #標題.內容.寄信者的信箱.收信者的信箱


        print("發送成功!")
    except Exception as e:
        if 'list index out of range' in str(e):
            errorMsg += '帳號或信箱輸入錯誤!請重新確認輸入內容!'
        else:
            errorMsg += str(e)
        return errorMsg

    return 'Succeed'

def _get_punch_overtime_query(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
        return Response
    status = ''
    Response = {}
    emp_no = request.GET.get('emp_no')
    emp_name = request.GET.get('emp_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    _emp_no = None
    try:
        if start_date is None:
            start_date = dt.now().date()
        if end_date is None:
            end_date = dt.now().date()
        filter_list = [Q(date__range=(start_date, end_date))]
        if emp_no or emp_name:
            if emp_name:
                _emp_no = EmpTable.objects.filter(emp_name=emp_name).get().emp_no
            filter_list.append(operator.or_(Q(emp_no=_emp_no), Q(emp_no=emp_no)))
        all_posts = PunchOvertime.objects.filter(*filter_list)  # 自模型取出資料
        posts = []
        for _post in all_posts:  # 按照api格式塞進去
            work_time = _post.work_time.strftime("%Y-%m-%d %H:%M:%S") if _post.work_time else None  # 三元運算子
            _emp_name = EmpTable.objects.filter(emp_no=_post.emp_no).get().emp_name
            post_data = {  # 按照api格式塞進去
                'id': _post.id,
                'emp_no': _post.emp_no,
                'emp_name': _emp_name,
                'date': _post.date,
                'section': _post.section,
                'work_time': work_time,
                'gps': _post.gps,
                'gps_address': _post.gps_address,
                'distance': _post.distance,
                'in_type': _post.in_type,
                'u_ip': _post.u_ip
            }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }

    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }

    return Response

def _get_punchtable_query(request):  # 取得出勤管理 基礎頁面的資料 需求emp_no,year,month
    try:
        jwt_verify(request)
    except Exception as e:
        Response = {
                'status': 'Error',
                'msg': str(e)
            }
        return Response
    status = ''
    Response = {}
    emp_no = request.GET.get('emp_no')
    emp_name = request.GET.get('emp_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    _emp_no = None

    try:
        if start_date is None:
            start_date = dt.now().date()
        if end_date is None:
            end_date = dt.now().date()
        filter_list = [Q(date__range=(start_date, end_date))]
        if emp_no or emp_name:
            if emp_name:
                _emp_no = EmpTable.objects.filter(emp_name=emp_name).get().emp_no
            filter_list.append(operator.or_(Q(emp_no=_emp_no), Q(emp_no=emp_no)))
        all_posts = PunchTable.objects.filter(*filter_list)  # 自模型取出資料
        posts = []
        for _post in all_posts:  # 按照api格式塞進去
            work_time = _post.work_time.strftime("%Y-%m-%d %H:%M:%S") if _post.work_time else None  # 三元運算子
            _emp_name = EmpTable.objects.filter(emp_no=_post.emp_no).get().emp_name
            post_data = {  # 按照api格式塞進去
                    'id':_post.id,
                    'emp_no': _post.emp_no,
                    'emp_name': _emp_name,
                    'date': _post.date,
                    'section': _post.section,
                    'work_time': work_time,
                    'gps': _post.gps,
                    'gps_address': _post.gps_address,
                    'distance': _post.distance,
                    'in_type': _post.in_type,
                    'u_ip': _post.u_ip
                }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }

    except Exception as e:
        Response = {
                'status': 'Error',
                'msg': str(e)
        }

    return Response

def _insert_emp_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response
    requestBody = request.body
    requestData = json.loads(requestBody)

    errorMsg = 'ERROR!'
    try:
        password = make_password(requestData['user_pwd'])
        EmpTable.objects.create(
            emp_id = None,
            emp_no=requestData['emp_no'],
            emp_name=requestData['emp_name'],
            comp_no="COMP01",
            dep_no="B",
            work_position=requestData['work_position'],
            user_pwd=password,
            tel=requestData['tel'],
            group_no=requestData['group_no'],
            group_leader=requestData['group_leader'],
            working=requestData['working'],
            auth='U',
            mail=requestData['mail'],
            location_switch=requestData['locationCheck'],
            )
        record_action_log('web_insert_emp_data',requestData['emp_no'],requestBody)

    except Exception as e:
        if 'Duplicate entry' in str(e):
            errorMsg += '該編號重複，請再確認編號'
        else:
            errorMsg += str(e)
        return errorMsg

    return 'Succeed'

def _update_emp_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'
    try:
        _post = EmpTable.objects.filter(emp_no=requestData['emp_no'])
        _post.update(
            working=requestData['working'],
            emp_name=requestData['emp_name'],
            comp_no="COMP01",
            work_position=requestData['work_position'],
            tel=requestData['tel'],
            group_no=requestData['group_no'],
            group_leader=requestData['group_leader'],
            mail=requestData['mail'],
            location_switch=requestData['locationCheck'],
        )
        record_action_log('web_update_emp_data', requestData['emp_no'], requestBody)
        if requestData['user_pwd']:
            print('change')
            _post.update(
                user_pwd=make_password(requestData['user_pwd'])
            )
    except Exception as e:
        errorMsg += str(e)
        return errorMsg
    return 'Succeed'


def _get_emp_data(request):  # 員工
    try:
        jwt_verify(request)
        all_posts = EmpTable.objects.all()
        posts = []

        for _post in all_posts:  # 按照api格式塞進去
            post_data = {  # 按照api格式塞進去
            'emp_no':_post.emp_no,
            'emp_id':_post.emp_id,
            'emp_name':_post.emp_name,
            'comp_no':_post.comp_no,
            'dep_no':_post.dep_no,
            'work_position':_post.work_position,
            'tel':_post.tel,
            'line_id':_post.line_id,
            'group_no':_post.group_no,
            'group_leader':_post.group_leader,
            'working':_post.working,
            'auth':_post.auth,
            'mail':_post.mail,
            'locationCheck':_post.location_switch,
            'selected':False
            }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
    return Response


def _get_emp_data2(request):  # 員工
    try:
        jwt_verify(request)

        all_posts = EmpTable_AUTH.objects.all()
        posts=[]

        for _post in all_posts:  # 按照api格式塞進去
            post_data = {  # 按照api格式塞進去
                'emp_no':_post.emp_no,
                'emp_name':_post.emp_name,
                'auth':_post.auth,
                'auth_name':_post.auth_name
            }

            posts.append(post_data)

        if all_posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
    return Response



def _get_WorkpositionList(request):
    try:
        jwt_verify(request)
        all_posts = WorkpositionList.objects.all()
        posts = []

        for _post in all_posts:  # 按照api格式塞進去
            post_data = {  # 按照api格式塞進去
            'wp_name':_post.wp_name,
            'wp_code':_post.wp_code,
             }
            posts.append(post_data)

        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
        return Response

def _insert_WorkpositionList(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response

    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = 'ERROR!'

    try:
        newWorkpositiondata = WorkpositionList.objects.create(
            wp_code=requestData['wp_code'],
            wp_name=requestData['wp_name'],
        )
    except Exception as e:
        if 'Duplicate entry' in str(e):
            errorMsg += '該編號重複，請再確認編號'
        else:
            errorMsg += str(e)
        return errorMsg

    return 'Succeed'


def _update_WorkpositionList(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response

    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'

    try:
        _post = WorkpositionList.objects.filter(wp_code=requestData['wp_code'])
        _post.update(
            wp_name=requestData['wp_name'],
        )
    except Exception as e:
        errorMsg += str(e)
        return errorMsg
    return 'Succeed'

def _delete_WorkpositionList(request, wp_code):
    try:
        jwt_verify(request)
    except Exception as e:
        Response = {
                'status': 'Error',
                'msg': str(e)
            }
        return Response

    errorMsg = '刪除錯誤!'

    try:
        _posts = EmpTable.objects.filter(work_position=wp_code)

        if len(_posts) > 0:
            errorMsg += '職位被使用中'
            raise Exception("work_position is using!")
        WorkpositionList.objects.filter(wp_code=wp_code).delete()
    except Exception as e:
        return errorMsg

    return 'Succeed'




def _update_location_check_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response=str(e)
        return Response
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'
    location = requestData['locationCheck']
    emp_no_list = requestData['emp_no']
    try:
        for _emp_no in emp_no_list:
            _post = EmpTable.objects.filter(emp_no=_emp_no)
            _post.update(
                location_switch=location,
            )
    except Exception as e:
        errorMsg += str(e)
        return errorMsg
    return 'Succeed'


def _get_location_data(request):
    try:
        jwt_verify(request)
        all_posts = LocationTable.objects.all()
        posts = []
        for _post in all_posts:
            post_data = {
                'id': _post.id,
                'no': _post.no,
                'txt': _post.txt,
                'select': _post.select,
                'location_lng': _post.location_lng,
                'location_lat': _post.location_lat,
                'location_range': _post.location_range,
                'note':_post.note
            }
            posts.append(post_data)
        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
    return Response


def _insert_location_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response = str(e)
        return Response
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = "ERROR!"
    try:
        _txt = requestData['txt']
        _select = requestData['select']
        if '0' in _select:
            location = gmap.geocode(_txt)
        else:
            location = gmap.decode(_txt)
    except Exception as e:
        errorMsg += str(e)
        return errorMsg

    errorMsg = '新增錯誤!'

    try:
        no = LocationTable.objects.filter(no=requestData['no'])
        if no.exists():
            errorMsg += str("重複名稱")
            return errorMsg
        LocationTable.objects.create(
            id=None,
            no=requestData['no'],
            txt=_txt,
            select=_select,
            location_range=requestData['location_range'],
            location_lat=location['lat'],
            location_lng=location['lng'],
            note = requestData['note']
        )
    except Exception as e:
        errorMsg += str(e)
        return errorMsg
    return 'Succeed'


def _update_location_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response = str(e)
        return Response
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = "ERROR!"
    try:
        _txt = requestData['txt']
        _select = requestData['select']
        if '0' in _select:
            location = gmap.geocode(_txt)
        else:
            location = gmap.decode(_txt)
    except Exception as e:
        errorMsg += str(e)
        return errorMsg

    errorMsg = '修改錯誤!'

    try:
        no = LocationTable.objects.filter(no=requestData['no']).exclude(id=requestData['id'])
        if no.exists():
            errorMsg += str("重複名稱")
            return errorMsg
        _post = LocationTable.objects.filter(id=requestData['id'])
        _post.update(
            no=requestData['no'],
            txt=_txt,
            select=_select,
            location_range=requestData['location_range'],
            location_lat=location['lat'],
            location_lng=location['lng'],
            note=requestData['note']

        )
    except Exception as e:
        errorMsg += str(e)
        return errorMsg
    return 'Succeed'


def _delete_location_data(request, id):
    try:
        jwt_verify(request)
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
        return Response

    errorMsg = '刪除錯誤!'

    try:
        _posts = EmpLocationTable.objects.filter(location_id=id)

        if len(_posts) > 0 or id==1:
            errorMsg += '地點被使用中'
            raise Exception(errorMsg)
        LocationTable.objects.filter(id=id).delete()
    except Exception as e:
        errorMsg += str(e)
        return errorMsg

    return 'Succeed'


def  _get_emp_group_data(request, location_id):
    try:
        jwt_verify(request)
        all_posts = EmpAndGroupTable.objects.filter(location_id=location_id).all()
        posts = []
        for _post in all_posts:
            post_data = {
                'emp_name': _post.emp_name,
                'group_name': _post.group_name,
                'location_id': _post.location_id
            }
            posts.append(post_data)
        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
    return Response
   

def _get_emp_location_data(request, location_id):
    try:
        jwt_verify(request)
        all_posts = EmpLocationTable.objects.filter(location_id=location_id).all()
        posts = []
        for _post in all_posts:
            post_data = {
                'id': _post.id,
                'emp_no': _post.emp_no,
                'group_no': _post.group_no,
                'location_id': _post.location_id
            }
            posts.append(post_data)
        if posts == []:
            Response = {
                'status': 'Null',
                'data': posts
            }
        else:
            Response = {
                'status': 'Succeed',
                'data': posts
            }
        return Response
    except Exception as e:
        Response = {
            'status': 'Error',
            'msg': str(e)
        }
    return Response


def _update_emp_location_data(request, location_id):
    try:
        jwt_verify(request)
    except Exception as e:
        Response = str(e)
        return Response
    requestBody = request.body
    requestDatas = json.loads(requestBody)

    errorMsg = '修改錯誤!'

    try:
        EmpLocationTable.objects.filter(location_id=location_id).all().delete()
        for requestData in requestDatas:
            EmpLocationTable.objects.create(
                id=None,
                emp_no=requestData['emp_no'],
                group_no=requestData['group_no'],
                location_id=location_id
            )
    except Exception as e:
        errorMsg += str(e)
        return errorMsg
    return 'Succeed'


def _delete_line_id_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        Response = str(e)
        return Response
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = '修改錯誤!'
    emp_no_list = requestData['emp_no']
    try:
        for _emp_no in emp_no_list:
            _post = EmpTable.objects.filter(emp_no=_emp_no)
            _post.update(
                line_id=''
            )
    except Exception as e:
        errorMsg += str(e)
        return errorMsg
    return 'Succeed'

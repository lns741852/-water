from django.contrib.auth.hashers import make_password
from HRCS.models import EmpTable, DepTable, WorkpositionList, GroupTable
from HRCS.log import record_action_log
from .token import jwt_verify
import random
import string
import json




def insert_user_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        if 'token未輸入' in str(e):
            Response = {
                'code': 401,
                'message': str(e)
            }
        else:
            Response = {
                'code': 403,
                'message': str(e)
            }
        return Response
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = 'ERROR!'

    try:
        _dep_no = requestData['d_number']
        _wp_code = requestData['title_id']
        d_nos = DepTable.objects.filter(dep_no=_dep_no)
        g_nos = GroupTable.objects.filter(group_no=_dep_no)
        if not d_nos.exists():
            DepTable.objects.create(
                dep_no=_dep_no,
                dep_name=requestData['d_name']
            )
        if not g_nos.exists():
            GroupTable.objects.create(
                group_no=_dep_no,
                group_name=requestData['d_name']
            )
        if _wp_code:
            wp_code = WorkpositionList.objects.filter(wp_code=_wp_code)
            if not wp_code.exists():
                wp_code.create(
                    id=None,
                    wp_code=_wp_code,
                    wp_name=requestData['title_name']
                )
        else:
            wp_name = WorkpositionList.objects.filter(wp_name=requestData['title_name'])
            if wp_name.exists():
                for wp_code in wp_name:
                    _wp_code = wp_code.wp_code
            else:
                while True:
                    wp_code = ''.join(random.sample(string.ascii_uppercase, 1)) + ''.join(
                        random.sample(string.digits, 2))
                    print(wp_code)
                    _wp_code = str(wp_code)
                    wp_code = WorkpositionList.objects.filter(wp_code=wp_code)
                    print(wp_code.exists())
                    if not wp_code.exists():
                        wp_code.create(
                            id=None,
                            wp_code=_wp_code,
                            wp_name=requestData['title_name']
                        )
                        break
        first_password="QhrGVE%sVDdYgdM"%str(requestData['u_no'])
        password = make_password(first_password)
        EmpTable.objects.create(
            emp_id=None,
            emp_no=requestData['u_no'],
            emp_name=requestData['c_name'],
            comp_no="COMP01",
            dep_no=_dep_no,
            group_no=_dep_no,
            group_leader=0,
            location_switch=1,
            work_position=_wp_code,
            user_pwd=password,
            working=requestData['work_status'],
            auth=requestData['identity']

        )
        record_action_log('insert_user_data',requestData['u_no'],requestBody)
        Response = {
            'code': 200,
            'message': 'Succeed',
            'data': requestData
        }

    except Exception as e:
        Response = None
        if 'Duplicate entry' in str(e):
            if 'PRIMARY' in str(e):
                errorMsg += '該編號重複，請再確認編號'
                Response = {
                    'code': 400,
                    'message': errorMsg,
                    'data': requestData
                }
            elif 'EMP_NAME_UNIQUE' in str(e):
                errorMsg += '該姓名重複，請再確認姓名'
                Response = {
                    'code': 400,
                    'message': errorMsg,
                    'data': requestData
                }

        else:
            errorMsg += str(e)
            Response = {
                'code': 500,
                'message': errorMsg,
                'data': requestData
            }
        return Response

    return Response


def update_user_data(request):
    try:
        jwt_verify(request)
    except Exception as e:
        if 'token未輸入' in str(e):
            Response = {
                'code': 401,
                'message': str(e)
            }
        else:
            Response = {
                'code': 403,
                'message': str(e)
            }
        return Response
    requestBody = request.body
    requestData = json.loads(requestBody)
    errorMsg = 'ERROR!'

    try:
        _dep_no = requestData['d_number']
        _wp_code = requestData['title_id']
        d_nos = DepTable.objects.filter(dep_no=_dep_no)
        if not d_nos.exists():
            print("?")
            DepTable.objects.create(
                dep_no=_dep_no,
                dep_name=requestData['d_name']
            )
        if _wp_code:
            wp_code = WorkpositionList.objects.filter(wp_code=_wp_code)
            if not wp_code.exists():
                wp_code.create(
                    id=None,
                    wp_code=_wp_code,
                    wp_name=requestData['title_name']
                )
        else:
            wp_name = WorkpositionList.objects.filter(wp_name=requestData['title_name'])
            if wp_name.exists():
                for wp_code in wp_name:
                    _wp_code = wp_code.wp_code
            else:
                while True:
                    wp_code = ''.join(random.sample(string.ascii_uppercase, 1)) + ''.join(
                        random.sample(string.digits, 2))
                    print(wp_code)
                    _wp_code = str(wp_code)
                    wp_code = WorkpositionList.objects.filter(wp_code=wp_code)
                    print(wp_code.exists())
                    if not wp_code.exists():
                        wp_code.create(
                            id=None,
                            wp_code=_wp_code,
                            wp_name=requestData['title_name']
                        )
                        break
        EmpTable.objects.get(emp_no=requestData['u_no'])
        _post = EmpTable.objects.filter(emp_no=requestData['u_no'])
        _post.update(
            emp_name=requestData['c_name'],
            comp_no="COMP01",
            dep_no=_dep_no,
            group_no=_dep_no,
            work_position=_wp_code,
            auth=requestData['identity'],
            working=requestData['work_status'],

        )
        record_action_log('update_user_data',requestData['u_no'],requestBody)

        Response = {
            'code': 200,
            'message': 'Succeed',
            'data': requestData
        }

    except Exception as e:
        if 'does not exist' in str(e):
            errorMsg += '查無此編號，請再確認編號'
            Response = {
                'code': 400,
                'message': errorMsg,
                'data': requestData
            }
        elif 'EMP_NAME_UNIQUE' in str(e):
            errorMsg += '該姓名重複，請再確認姓名'
            Response = {
                'code': 400,
                'message': errorMsg,
                'data': requestData
            }

        else:
            errorMsg += str(e)
            Response = {
                'code': 500,
                'message': errorMsg,
                'data': requestData
            }
        return Response

    return Response

from django.db.models import Q
from datetime import datetime as dt
from functools import reduce
from HRCS.models import LocationTable, PunchTable, PunchOvertime
from .token import jwt_verify

import operator


def get_attendance(request, attendance_type):
    try:
        if attendance_type == 'punch':
            jwt_verify(request)
            return _get_attendance_punch(request)
        elif attendance_type == 'sign':
            jwt_verify(request)
            return _get_attendance_sign(request)
        else:
            raise Exception("路徑錯誤")
    except Exception as e:
        if '路徑錯誤' in str(e):
            Response = {
                'code': 500,
                'message': str(e)
            }
        elif 'token未輸入' in str(e):
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


def _get_attendance_punch(request):  # 取得出勤管理 基礎頁面的資料 需求emp_no,year,month
    emp_no = request.GET.get('emp_no')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        if start_date is None:
            start_date = dt.now().date()
        if end_date is None:
            end_date = dt.now().date()
        filter_list = [Q(date__range=(start_date, end_date))]
        if emp_no:
            filter_list.append(Q(emp_no=emp_no))
        all_posts = PunchTable.objects.filter(reduce(operator.and_, filter_list))

        # 自模型取出資料
        posts = []
        for _post in all_posts:  # 按照api格式塞進去
            address = "未比對到地址!"
            work_time = _post.work_time.strftime("%Y-%m-%d %H:%M:%S") if _post.work_time else None  # 三元運算子
            location = LocationTable.objects.filter(id=_post.location_id)
            if location.exists():
                address = location.get().txt
            post_data = {
                'u_no': _post.emp_no,
                'work_time': work_time,
                'section': _post.section,
                'gps': _post.gps,
                'gps_address': _post.gps_address,
                'u_ip': _post.u_ip,
                'in_type': _post.in_type,
                'address': address,
                'distance': _post.distance,
            }
            posts.append(post_data)
        if not posts:
            Response = {
                'code': 400,
                'message': '查無資料',
                'data': posts
            }
        else:
            Response = {
                'code': 200,
                'data': posts
            }

    except Exception as e:
        Response = {
                'code': 500,
                'message': str(e)
        }

    return Response


def _get_attendance_sign(request):  # 取得出勤管理 基礎頁面的資料 需求emp_no,year,month
    emp_no = request.GET.get('emp_no')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        if start_date is None:
            start_date = dt.now().date()
        if end_date is None:
            end_date = dt.now().date()
        filter_list = [Q(date__range=(start_date, end_date))]
        if emp_no:
            filter_list.append(Q(emp_no=emp_no))
        all_posts = PunchOvertime.objects.filter(reduce(operator.and_, filter_list))

        # 自模型取出資料
        posts = []
        for _post in all_posts:  # 按照api格式塞進去
            work_time = _post.work_time.strftime("%Y-%m-%d %H:%M:%S") if _post.work_time else None  # 三元運算子
            post_data = {
                'u_no': _post.emp_no,
                'work_time': work_time,
                'type': _post.section,
                'gps': _post.gps,
                'gps_address': _post.gps_address,
                'u_ip': _post.u_ip,
                'work_report': "",
                'remark': ""
            }
            posts.append(post_data)

        if not posts:
            Response = {
                'code': 400,
                'message': '查無資料',
                'data': posts
            }
        else:
            Response = {
                'code': 200,
                'data': posts
            }

    except Exception as e:
        Response = {
            'code': 500,
            'message': str(e)
        }

    return Response

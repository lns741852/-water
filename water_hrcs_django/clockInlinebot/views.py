
from datetime import datetime
import googlemaps
from urllib.parse import urlparse, parse_qs
from math import cos,sin
import math
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q
from django.templatetags.static import static
from django.views.decorators.http import  require_GET

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, PostbackEvent, TextSendMessage , FlexSendMessage, LocationSendMessage

from .models import ZzEmpTable, CompanyTable,LocationTable,EmpLocationTable,PunchTable,PunchOvertime, LineEmpError

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

gmaps = googlemaps.Client(key='AIzaSyC9OYTu-eCoyoAKfUsFabZx-k-yA_Wg8fw')

# 本機
# myurl = 'https://12d0-61-219-235-222.ngrok.io'

# 測試
myurl = 'https://water-hrcs-django.azurewebsites.net'

# 正式
# myurl = 'https://hrcslinebot.justright.com.tw'




@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        message = []
        # 在這裡將body寫入機器人回傳的訊息中，可以更容易看出你收到的webhook長怎樣#
        message.append(TextSendMessage(text=str(body)))
        try:
            events = parser.parse(str(body), signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
#MessageEvent訊息
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print(event.message.type)
                line_id = event.source.user_id
                hasuser_id = ZzEmpTable.objects.filter(
                    line_id=line_id).count()

                if event.message.type == 'text':
                    get_tel = ZzEmpTable.objects.filter(
                        emp_no=event.message.text).count()
                    has_tel = ZzEmpTable.objects.filter(
                        Q(emp_no=event.message.text, line_id__gt='') | Q(emp_no=event.message.text,
                                                                      line_id__isnull=True)).count()
                    if hasuser_id == 0 and get_tel == 0:
                        LineEmpError.objects.create(line_id=event.source.user_id,error=event.message.text)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入您的員工編號')

                        )
                    elif hasuser_id == 0 and get_tel > 0 and has_tel == 0:
                        ZzEmpTable.objects.filter(
                            emp_no=event.message.text).update(line_id=event.source.user_id)
                        user_name = ZzEmpTable.objects.get(
                            emp_no=event.message.text, line_id=event.source.user_id)
                        user_name = user_name.emp_no

                        backtext = '檢測到員工中有【' + event.message.text + '】員工編號，已將您的LINE綁定，可以開始使用打卡鐘功能了'
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(backtext)
                        )
                    elif hasuser_id == 0 and get_tel > 0 and has_tel > 0:
                        user_name = ZzEmpTable.objects.get(
                            emp_no=event.message.text)
                        user_name = user_name.emp_no
                        backtext = '檢測到員工中有【' + event.message.text + '】員工編號，但此號碼已被綁定，請洽公司詢問是否為誤綁'
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(backtext)
                        )
                    else:
                        # 先從line_id獲取員工資料emp.emp_no獲取員工編號
                        emp = ZzEmpTable.objects.filter(
                            line_id=line_id)[:1].get()
                        company = CompanyTable.objects.filter(  # 確認是登記在資料表內的公司
                            comp_no=emp.comp_no)
                        if not company:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='員工公司編屬有誤')
                            )
                            break

                        if emp.working !=1:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='非在職狀態無法使用')
                            )
                            break
                        # maincompany = company[0].main  # 判斷是否為此資料庫主公司員工
                        # nowtime取傳訊息時間； nowtime = datetime.now()-timedelta(seconds=5)取現在時間
                        # nowtime = datetime.fromtimestamp(
                        #     event.timestamp / 1000)
                        # nowtimestamp = event.timestamp
                        if event.message.text == 'help':
                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                                event.reply_token,
                                allhelp()

                            )
                        else:  # 其他奇奇怪怪的字輸入

                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                                event.reply_token,
                                default_jsoncontent()

                            )
                # image訊息
                elif event.message.type == 'image':
                    if hasuser_id == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入您的員工編號')

                        )
                    else:
                        messagetext = '無效訊息'
                        if event.message.content_provider.original_content_url:
                            # 先從line_id獲取員工資料emp.emp_no獲取員工編號
                            emp = ZzEmpTable.objects.filter(
                                line_id=line_id)[:1].get()
                            company = CompanyTable.objects.filter(  # 確認是登記在資料表內的公司
                                comp_no=emp.comp_no)
                            if not company:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text='員工公司編屬有誤')
                                )
                                break
                            if emp.working != 1:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text='非在職狀態無法使用')
                                )
                                break
                            maincompany = company[0].main
                            # nowtime取傳訊息時間； nowtime = datetime.now()-timedelta(seconds=5)取現在時間
                            imgdata = event.message.content_provider.original_content_url
                            urlquery = parse_qs(urlparse(imgdata).query)
                            imgfunc = urlquery['type'][0]
                            # image-上班卡
                            if imgfunc == 'punchin':  # 上班卡

                                if urlquery['emp_no'][0] == line_id:
                                    gettime = datetime.fromtimestamp(
                                        int(urlquery['punch'][0]) / 1000)
                                    showtime = gettime.strftime(
                                        '%Y年%m月%d日 %H:%M:%S')
                                    location_str_list = urlquery['location'][0].split(',')

                                    if maincompany == 1:
                                        if emp.location_switch == 1:#應檢查地點距離
                                            # 預設值
                                            over_distance=0#超過距離
                                            location_table=LocationTable.objects
                                            group_location = EmpLocationTable.objects.filter(group_no=emp.group_no.group_no)
                                            emp_location=EmpLocationTable.objects.filter(emp_no=emp.emp_no)
                                            all_location=(group_location.values('location_id') |emp_location.values('location_id')).distinct().values('location_id')

                                            if not emp_location and not group_location:#要規範地點但找不到設定
                                                # print('要規範地點但找不到設定')
                                                messagetext=return_nolocation()

                                                line_bot_api.reply_message(
                                                    event.reply_token,
                                                    messagetext
                                                )
                                                break
                                            if group_location :#群組有設定地點
                                                # print('群組有設定地點')
                                                for g_location in group_location:

                                                    location = location_table.filter(id=g_location.location_id).first()
                                                    distance = getDistance(float(location_str_list[0]),
                                                                           float(location_str_list[1]),
                                                                           float(location.location_lat),
                                                                           float(location.location_lng))

                                                    messagetext = punch_distance(1,distance, location, location_str_list,
                                                                                 emp, gettime, showtime, urlquery)

                                                    if messagetext:
                                                        break
                                                    else:
                                                        messagetext = False
                                                        # 取超過範圍下最近的距離
                                                        if over_distance == 0:
                                                            over_distance = int(distance)
                                                        elif (over_distance != 0) and (int(over_distance) > int(distance)):
                                                            over_distance = int(distance)

                                            if emp_location and (not messagetext or str(messagetext)=='無效訊息'):#個人有設定地點
                                                # print('個人有設定地點')
                                                for e_location in emp_location:
                                                    location = location_table.filter(id=e_location.location_id).first()
                                                    distance = getDistance(float(location_str_list[0]),
                                                                           float(location_str_list[1]),
                                                                           float(location.location_lat),
                                                                           float(location.location_lng))
                                                    messagetext = punch_distance(1,distance, location, location_str_list,
                                                                                 emp, gettime, showtime, urlquery)

                                                    if messagetext:
                                                        break
                                                    else:
                                                        # 取超過範圍下最近的距離
                                                        if over_distance == 0:
                                                            over_distance = int(distance)
                                                        elif (over_distance != 0) and (int(over_distance) > int(distance)):
                                                            over_distance = int(distance)

                                            if not messagetext:
                                                #所有打卡距離都不符
                                                messagetext=return_toofarflex(urlquery['location'][0],all_location,over_distance)
                                                line_bot_api.reply_message(
                                                    event.reply_token,
                                                    messagetext
                                                )
                                                break
                                        else:# 不用檢查地點距離直接打卡
                                            reverse_geocode_result = gmaps.reverse_geocode(
                                                (float(location_str_list[0]), float(location_str_list[1])),
                                                language='zh-TW')
                                            PunchTable.objects.create(emp_no=emp.emp_no, date=gettime.date(), section=1,location_id=0,
                                                                      work_time=gettime,
                                                                      gps=urlquery['location'][0],
                                                                        gps_address=reverse_geocode_result[0][
                                                                          'formatted_address'], distance=0,u_ip=urlquery['u_ip'][0])
                                            messagetext = LocationSendMessage(
                                                title=('【%s】上班打卡成功' % (emp.emp_name)),
                                                address=str(showtime),
                                                latitude=location_str_list[0],
                                                longitude=location_str_list[1]
                                            )

                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        messagetext
                                    )
                                    break
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    default_jsoncontent()
                                )
                            # image-下班卡
                            if imgfunc == 'punchout':  # 下班卡
                                if urlquery['emp_no'][0] == line_id:
                                    gettime = datetime.fromtimestamp(
                                        int(urlquery['punch'][0]) / 1000)
                                    showtime = gettime.strftime(
                                        '%Y年%m月%d日 %H:%M:%S')
                                    location_str_list = urlquery['location'][0].split(',')

                                    if maincompany == 1:
                                        if emp.location_switch == 1:#應檢查地點距離
                                            # 預設值
                                            over_distance=0#超過距離
                                            location_table=LocationTable.objects
                                            group_location = EmpLocationTable.objects.filter(group_no=emp.group_no.group_no)
                                            emp_location=EmpLocationTable.objects.filter(emp_no=emp.emp_no)
                                            all_location=(group_location.values('location_id') |emp_location.values('location_id')).distinct().values('location_id')

                                            if not emp_location and not group_location:#要規範地點但找不到設定
                                                # print('要規範地點但找不到設定')
                                                messagetext = return_nolocation()

                                                line_bot_api.reply_message(
                                                    event.reply_token,
                                                    messagetext
                                                )
                                                break

                                            if group_location :#群組有設定地點
                                                # print('群組有設定地點')
                                                for g_location in group_location:

                                                    location = location_table.filter(id=g_location.location_id).first()
                                                    distance = getDistance(float(location_str_list[0]),
                                                                           float(location_str_list[1]),
                                                                           float(location.location_lat),
                                                                           float(location.location_lng))

                                                    messagetext = punch_distance(2,distance, location, location_str_list,
                                                                                 emp, gettime, showtime, urlquery)

                                                    if messagetext:
                                                        break
                                                    else:
                                                        # 取超過範圍下最近的距離
                                                        if over_distance == 0:
                                                            over_distance = int(distance)
                                                        elif (over_distance != 0) and (int(over_distance) > int(distance)):
                                                            over_distance = int(distance)


                                            if emp_location and (not messagetext or str(messagetext)=='無效訊息'):#個人有設定地點
                                                # print('個人有設定地點')
                                                for e_location in emp_location:
                                                    location = location_table.filter(id=e_location.location_id).first()

                                                    distance = getDistance(float(location_str_list[0]),
                                                                           float(location_str_list[1]),
                                                                           float(location.location_lat),
                                                                           float(location.location_lng))
                                                    messagetext = punch_distance(2,distance, location, location_str_list,
                                                                                 emp, gettime, showtime, urlquery)

                                                    if messagetext:
                                                        break
                                                    else:
                                                        # 取超過範圍下最近的距離
                                                        if over_distance == 0:
                                                            over_distance = int(distance)
                                                        elif (over_distance != 0) and (int(over_distance) > int(distance)):
                                                            over_distance = int(distance)

                                            if not messagetext:
                                                #所有打卡距離都不符
                                                messagetext=return_toofarflex(urlquery['location'][0],all_location,over_distance)
                                                line_bot_api.reply_message(
                                                    event.reply_token,
                                                    messagetext
                                                )
                                                break
                                        else:# 不用檢查地點距離直接打卡
                                            reverse_geocode_result = gmaps.reverse_geocode(
                                                (float(location_str_list[0]), float(location_str_list[1])),
                                                language='zh-TW')
                                            PunchTable.objects.create(emp_no=emp.emp_no, date=gettime.date(), section=2,
                                                                      work_time=gettime,
                                                                      gps=urlquery['location'][0],
                                                                        gps_address=reverse_geocode_result[0][
                                                                          'formatted_address'], distance=0,u_ip=urlquery['u_ip'][0])
                                            messagetext = LocationSendMessage(
                                                title=('【%s】下班打卡成功' % (emp.emp_name)),
                                                address=str(showtime),
                                                latitude=location_str_list[0],
                                                longitude=location_str_list[1]
                                            )

                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        messagetext
                                    )
                                    break
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    default_jsoncontent()
                                )
                            # image-加班上班卡
                            if imgfunc == 'overin':  # 加班上班卡
                                if urlquery['emp_no'][0] == line_id:
                                    gettime = datetime.fromtimestamp(
                                        int(urlquery['punch'][0]) / 1000)
                                    showtime = gettime.strftime(
                                        '%Y年%m月%d日 %H:%M:%S')
                                    location_str_list = urlquery['location'][0].split(',')

                                    if maincompany == 1:
                                    # 不用檢查地點距離直接打卡
                                        reverse_geocode_result = gmaps.reverse_geocode(
                                            (float(location_str_list[0]), float(location_str_list[1])),
                                            language='zh-TW')
                                        PunchOvertime.objects.create(emp_no=emp.emp_no, date=gettime.date(), section=1,
                                                                  work_time=gettime,
                                                                  gps=urlquery['location'][0],
                                                                    gps_address=reverse_geocode_result[0][
                                                                      'formatted_address'], distance=0,u_ip=urlquery['u_ip'][0])
                                        messagetext = LocationSendMessage(
                                            title=('%s處外加班簽到打卡成功【%s】' % (str(showtime), emp.emp_name)),
                                            address=reverse_geocode_result[0]['formatted_address'],
                                            latitude=location_str_list[0],
                                            longitude=location_str_list[1]
                                        )

                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        messagetext
                                    )
                                    break
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    default_jsoncontent()
                                )
                            # image-加班下班卡
                            if imgfunc == 'overout':  # 加班下班卡
                                if urlquery['emp_no'][0] == line_id:
                                    gettime = datetime.fromtimestamp(
                                        int(urlquery['punch'][0]) / 1000)
                                    showtime = gettime.strftime(
                                        '%Y年%m月%d日 %H:%M:%S')
                                    location_str_list = urlquery['location'][0].split(',')

                                    if maincompany == 1:
                                    # 不用檢查地點距離直接打卡
                                        reverse_geocode_result = gmaps.reverse_geocode(
                                            (float(location_str_list[0]), float(location_str_list[1])),
                                            language='zh-TW')
                                        PunchOvertime.objects.create(emp_no=emp.emp_no, date=gettime.date(), section=2,
                                                                  work_time=gettime,
                                                                  gps=urlquery['location'][0],
                                                                    gps_address=reverse_geocode_result[0][
                                                                      'formatted_address'], distance=0,u_ip=urlquery['u_ip'][0])
                                        messagetext = LocationSendMessage(
                                            title=('%s處外加班簽退打卡成功【%s】' % (str(showtime), emp.emp_name)),
                                            address=reverse_geocode_result[0]['formatted_address'],
                                            latitude=location_str_list[0],
                                            longitude=location_str_list[1]
                                        )

                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        messagetext
                                    )
                                    break
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    default_jsoncontent()
                                )
                elif event.message.type == 'location':
                    if hasuser_id == 0:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='請輸入您的員工編號')

                        )
                    else:
                        message.append(TextSendMessage(text='位置訊息'))
                        line_bot_api.reply_message(event.reply_token, message)
                else:
                    print(event.message.type)
#post訊息
            elif isinstance(event, PostbackEvent):
                print('PostbackEvent')
                print(event.postback.data)
                getpostdata = event.postback.data
                messagejson = default_jsoncontent()
                # punch_help()

                if getpostdata == 'punch_help':
                    messagejson = punch_help()
                elif getpostdata == 'lineAccessRights' or getpostdata == 'LocationAuthorization':
                    messagejson = help_punch_alert()
                elif getpostdata == 'help':
                    messagejson = allhelp()


                elif getpostdata == 'line_help':
                    line_id = event.source.user_id
                    hasuser_id = ZzEmpTable.objects.filter(
                        line_id=line_id)
                    if hasuser_id:
                        hasuser_id=hasuser_id.first()
                        messagejson = TextSendMessage(('你已經綁定【%s】%s 帳號了。'%(hasuser_id.emp_no,hasuser_id.emp_name)))
                    else:
                        messagejson = TextSendMessage('輸入員工編號，就能幫你綁定囉')

                line_bot_api.reply_message(
                    event.reply_token,
                    messagejson
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def punch_help():
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_stap1.png') + '?v=1220v2',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "1.按下打卡",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "上班下班打卡 或 處外簽到退 步驟皆相同",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_stap2.png') + '?v=2',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "2.將會直接開啟打卡位置搜尋頁面",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "等待位置傳送，傳送成功即會自行關閉頁面",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "手機定位請記得開啟",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xxs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "micro",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_stap3.png') + '?v=3',
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "3.如果發生錯誤",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "檢查GPS授權",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "text",
                                            "text": "手機定位請記得開啟",
                                            "wrap": True,
                                            "color": "#993311",
                                            "size": "xxs",
                                            "flex": 5
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "存取權限?",
                                        "data": "lineAccessRights"
                                    },
                                    "height": "sm",
                                    "margin": "none",
                                    "offsetTop": "5px"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "授權問題?",
                                        "data": "LocationAuthorization"
                                    },
                                    "margin": "none",
                                    "height": "sm"
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px",
                    "paddingBottom": "0px"
                }
            }
        ]
    }
    content={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "image",
        "url": myurl + static('img/punch_stap1.png') + '?v=1220v2',
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "4:3"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "1.按下打卡",
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "上班下班打卡 或 處外簽到退 步驟皆相同",
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs"
                  }
                ]
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "image",
        "url": myurl + static('img/punch_stap2.png') + '?v=1220v2',
        "aspectMode": "cover",
        "aspectRatio": "4:3",
        "size": "full"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "2.將會直接開啟打卡位置搜尋頁面",
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "等待位置傳送",
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs"
                  },
                  {
                    "type": "text",
                    "text": "傳送成功會自行關閉頁面",
                    "wrap": True,
                    "color": "#993311",
                    "size": "xxs"
                  }
                ]
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "image",
        "url": myurl + static('img/punch_stap3.png') + '?v=1220v2',
        "aspectMode": "cover",
        "aspectRatio": "6:5",
        "size": "full"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "3.如果發生錯誤",
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "檢查是否沒有GPS授權",
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs"
                  },
                  {
                    "type": "text",
                    "text": "手機定位請記得開啟",
                    "wrap": True,
                    "color": "#993311",
                    "size": "xxs"
                  }
                ]
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "存取權限?",
                  "data": "lineAccessRights"
                },
                "height": "sm",
                "margin": "none",
                "offsetTop": "5px"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "授權問題?",
                  "data": "LocationAuthorization"
                },
                "margin": "none",
                "height": "sm"
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px",
        "paddingBottom": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "image",
        "url": myurl + static('img/punch_stap4.png') + '?v=1220v2',
        "aspectMode": "cover",
        "aspectRatio": "1:1",
        "size": "full"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "4.傳送打卡地點-成功",
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "成功會顯示打卡時間、地點、地圖",
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs"
                  }
                ]
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "image",
        "url": myurl + static('img/punch_stap5.png') + '?v=1220v2',
        "aspectMode": "cover",
        "aspectRatio": "1:1",
        "size": "full"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "4.傳送打卡地點-失敗",
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "距離過遠 :看到可以在哪打卡 與 離最近可以打卡地點有多遠",
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs"
                  }
                ]
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    {
      "type": "bubble",
      "size": "micro",
      "hero": {
          "type": "image",
          "url": myurl + static('img/punch_stap6.png') + '?v=1220v2',
          "aspectMode": "cover",
          "aspectRatio": "1:1",
          "size": "full"
      },
      "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
              {
                  "type": "text",
                  "text": "4.傳送打卡地點-失敗",
                  "weight": "bold",
                  "size": "sm",
                  "wrap": True
              },
              {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                      {
                          "type": "box",
                          "layout": "vertical",
                          "spacing": "sm",
                          "contents": [
                              {
                                  "type": "text",
                                  "text": "沒有可以打卡的地點",
                                  "wrap": True,
                                  "color": "#8c8c8c",
                                  "size": "xs"
                              }
                          ]
                      }
                  ]
              }
          ],
          "spacing": "sm",
          "paddingAll": "13px"
        }
      }

  ]
}
    message = FlexSendMessage(alt_text='打卡教學', contents=content)
    return message


def help_punch_alert():
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "kilo",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_alert1.png') + '?v=1220v2',
                    "size": "full",
                    "aspectRatio": "320:213",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "LINE存取權限",
                            "weight": "bold",
                            "size": "md",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "第一次使用打卡功能會跳出程式授權請求存取權限，請按許可",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            },
            {
                "type": "bubble",
                "size": "kilo",
                "hero": {
                    "type": "image",
                    "url": myurl + static('img/punch_alert2.png') + '?v=2',
                    "size": "full",
                    "aspectRatio": "320:213",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "打卡位置資訊授權",
                            "weight": "bold",
                            "size": "md",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "打卡網頁會搜尋您所在的位置，並會跳出請求授權，請按確定",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
            }
        ]
    }
    message = FlexSendMessage(alt_text='驗證及授權幫助', contents=content)
    return message


def allhelp():
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "kilo",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "幫助",
                            "weight": "bold",
                            "size": "md",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "你想問什麼問題?",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "打卡教學",
                                                "data": "punch_help"
                                            },
                                            "height": "sm"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "程式授權與存取",
                                                "data": "lineAccessRights"
                                            },
                                            "height": "sm",
                                            "style": "primary",
                                            "color": "#226699"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "line綁定問題",
                                                "data": "line_help"
                                            },
                                            "height": "sm"
                                        }

                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px",
                    "paddingBottom": "8px"
                }
            }
        ]
    }
    message = FlexSendMessage(alt_text='需要幫助嗎?', contents=content)
    return message


def default_jsoncontent():  # 我不懂你的意思
    content = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "micro",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "我不懂你的意思",
                            "weight": "bold",
                            "size": "md",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "你需不需要",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 5
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "postback",
                                                "label": "尋求幫助",
                                                "data": "help"
                                            },
                                            "height": "sm"
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px",
                    "paddingBottom": "0px"
                }
            }
        ]
    }
    message = FlexSendMessage(alt_text='需要幫助嗎?', contents=content)
    return message


def return_nolocation():
    content = {
      "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": myurl + static('img/waring.png') + '?v=1',
        "size": "md",
        "aspectRatio": "1:1",
        "aspectMode": "fit",
        "offsetTop": "8px"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "查無打卡權限",
            "weight": "bold",
            "size": "xxl",
            "align": "center",
            "color": "#960808"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "你已被開啟打卡需要偵測範圍地點，但尚未被歸入任何可打卡地點",
                    "color": "#aaaaaa",
                    "size": "lg",
                    "wrap": True
                  }
                ]
              }
            ]
          }
        ]
      }
    }

    message = FlexSendMessage(alt_text='查無打卡範圍歸入', contents=content)
    return message
def return_toofarflex(gps,all_location,over_distance):
    canpunch_text=""
    location_table=LocationTable.objects.filter(id__in=all_location)
    for index , location in enumerate(location_table):

        if index==0:
            canpunch_text += location.no
        else:
            canpunch_text+='、'+location.no

    content = {
      "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": myurl + static('img/waring.png') + '?v=1',
        "size": "md",
        "aspectRatio": "1:1",
        "aspectMode": "fit",
        "offsetTop": "8px"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "距離過遠",
            "weight": "bold",
            "size": "3xl",
            "align": "center",
            "color": "#960808"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": 'GPS '+gps,
                    "wrap": True,
                    "color": "#aaaaaa",
                    "size": "sm",
                    "offsetStart": "16px"
                  },
                  {
                    "type": "text",
                    "text": "可以打卡地點",
                    "color": "#aaaaaa",
                    "size": "lg",
                    "wrap": True,
                    "decoration": "underline"
                  },
                  {
                    "type": "text",
                    "text": canpunch_text,
                    "wrap": True,
                    "color": "#666666",
                    "size": "md",
                    "offsetStart": "16px"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "距離最近的地點",
                    "color": "#aaaaaa",
                    "size": "md",
                    "decoration": "underline"
                  },
                  {
                    "type": "text",
                    "text": str(over_distance)+"M",
                    "wrap": True,
                    "color": "#666666",
                    "size": "md"
                  }
                ]
              }
            ]
          }
        ]
      }
    }

    message = FlexSendMessage(alt_text='打卡距離過遠', contents=content)
    return message

@require_GET
def get_location(request):
    return render(request, "get_location.html")
@require_GET
def get_location_punchout(request):
    return render(request, "get_location_punchout.html")
@require_GET
def get_location_overin(request):
    return render(request, "get_location_overin.html")
@require_GET
def get_location_overout(request):
    return render(request, "get_location_overout.html")


def rad(d):
    return d * math.pi / 180.0


def getDistance(lat1, lng1, lat2, lng2):
    EARTH_REDIUS = 6378.137
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(sin(a / 2), 2) + cos(radLat1) * cos(radLat2) * math.pow(sin(b / 2), 2)))
    s = s * EARTH_REDIUS

    return s *1000



def punch_distance(section,distance,location,location_str_list,emp,gettime,showtime,urlquery):
    #section:1上班2下班
    if (int(distance) > int(location.location_range)):

        return False
    else:
        reverse_geocode_result = gmaps.reverse_geocode(
            (float(location_str_list[0]), float(location_str_list[1])),
            language='zh-TW')
        PunchTable.objects.create(emp_no=emp.emp_no, date=gettime.date(), section=section,location_id=location.id, work_time=gettime,
                                  gps=urlquery['location'][0],
                                  gps_address=reverse_geocode_result[0]['formatted_address'], distance=distance,u_ip=urlquery['u_ip'][0])

        section_text=""
        if section==1:
            section_text = "上班"
        elif section==2:
            section_text = "下班"
        messagetext = LocationSendMessage(
            title=('%s%s打卡成功【%s】' % (str(showtime),section_text,emp.emp_name)),
            address=reverse_geocode_result[0]['formatted_address'],
            latitude=location_str_list[0],
            longitude=location_str_list[1]
        )
        return messagetext



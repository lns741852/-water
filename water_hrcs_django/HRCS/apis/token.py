from datetime import datetime as dt, timedelta
from HRCS.models import JwtToken
import datetime


def _verify_jwt(token):
    verify=JwtToken.objects.filter(token=token)
    try:
        nowtime = dt.strptime(str((dt.utcnow()+datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
        exp_time=dt.strptime(str(verify[0].exp_time.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
        print('AAA')
        if nowtime-exp_time>timedelta(seconds=0):
            print('AAAA')
            raise Exception("over limit!")
        print(nowtime-exp_time)
    except Exception as e:
        print(e)
        return e


def jwt_verify(request):
    try:
        _jwt_verify = _verify_jwt(request.headers['Token'])
        if "list index out of range" in str(_jwt_verify):
            raise Exception("token不存在!")
        elif "over limit!" in str(_jwt_verify):
            raise Exception("token已過期!")
    except KeyError:
        raise Exception("token未輸入!")



from HRCS.models import Action_log

import random
import string
import json


def record_action_log(action,action_id,content):

    try:
        Action_log.objects.create(
            id=None,
            action=action,
            action_id=action_id,
            content=content,

        )

    except Exception as e:
        print(e)





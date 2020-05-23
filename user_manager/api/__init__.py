from common.utils import wrapped_api

from .auth import login
from .user_management import (create_user, disable_user, forgot_password,
                              reset_password, send_captcha)

LOGIN_API = wrapped_api({
    "post": login
})

USER_CREATE_API = wrapped_api({
    "post": create_user
})

USER_DISABLE_API = wrapped_api({
    "post": disable_user
})

USER_RESET_API = wrapped_api({
    "post": reset_password
})

USER_FORGOT_API = wrapped_api({
    "post": forgot_password
})

CAPTCHA_API = wrapped_api({
    "post": send_captcha
})

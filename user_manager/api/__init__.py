from .auth import login
from .user_management import create_user, disable_user, reset_password
from common.utils import wrapped_api

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

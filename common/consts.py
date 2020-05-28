from enum import Enum

# Permission Levels
Everyone = 0
User = 1
VIP = 2
Admin = 3

# HTTP Status Code


class StatusCode(Enum):
    # Success Code Family
    SUCCESS = 200_00

    # Bad Request Family
    BAD_REQUEST = 400_00
    INVALID_REQUEST_ARGUMENT = 400_01
    INVALID_CAPTCHA = 400_02
    BAD_OCR_TYPE = 400_03
    NO_IMAGE_FILE = 400_04

    # Unauthorized Family
    UNAUTHORIZED = 401_00
    INVALID_USERNAME_OR_PASSWORD = 401_01
    INVALID_TOKEN = 401_02
    TOKEN_EXPIRED = 401_03
    ACCOUNT_DISABLED = 401_04

    # Refuse Access Family
    REFUSE_ACCESS = 403_00
    PERMISSION_DENIED = 403_01

    # Not Found Family
    ITEM_NOT_FOUND = 404_00

    # Resource Too Huge Family
    Image_HUGE = 413_00
    
    # Duplicated Family
    ITEM_ALREADY_EXISTS = 409_00

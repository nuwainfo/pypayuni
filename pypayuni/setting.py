'''
    You personal setting of Payuni
'''
try:
    from django.conf import settings
except:
    settings = {}

PAYUNI_SANDBOX = getattr(settings, 'PAYUNI_SANDBOX_MODE', True)

PAYUNI_SERVICE_URL = 'https://api.payuni.com.tw/api/upp'
PAYUNI_SANDBOX_SERVICE_URL = 'https://sandbox-api.payuni.com.tw/api/upp'
PAYUNI_PERIOD_URL = 'https://api.payuni.com.tw/api/period/Page'
PAYUNI_SANDBOX_PERIOD_URL = 'https://sandbox-api.payuni.com.tw/api/period/Page'
'''
    Get these from Payuni management panel
'''
MERCHANT_ID = getattr(settings, 'MERCHANT_ID', 'S02929350')
HASH_KEY = getattr(settings, 'HASH_KEY', 'mgNciHHEJ2OgNb1ueyKJ4GFGb1GhBsnk')
HASH_IV = getattr(settings, 'HASH_IV', '1Q4LTlK18rXBGbJO')
'''
    Please specify your own URL, check out the Payuni document for more details
    https://www.payuni.com.tw/docs/web/
'''
RETURN_URL = getattr(settings, 'RETURN_URL', 'http://127.0.0.1:8000/result')
CLIENT_BACK_URL = getattr(settings, 'CLIENT_BACK_URL', '')

PERIOD_TYPE = {'W': 'week', 'M': 'month', 'Y': 'year'}

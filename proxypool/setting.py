


HOST = '127.0.0.1'
PORT = '6379'
PASSWORD = ''
PROXY_SCORE_INIT = 10
PROXY_SCORE_MIN = 0
PROXY_SCORE_MAX = 100
REDIS_KEY = 'proxies'
GET_TIMEOUT = 10

TEST_URL = 'http://www.baidu.com'
TEST_TIMEOUT = 10
TEST_BATCH = 40
# only save anonymous proxy
TEST_ANONYMOUS = True
# TEST_HEADERS = env.json('TEST_HEADERS', {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
# })
TEST_VALID_STATUS = [200, 206, 302]

PROXY_NUMBER_MAX = 50000
PROXY_NUMBER_MIN = 0

# definition of api
API_HOST = '0.0.0.0'
API_PORT = 5555
API_THREADED = True

# scheduler
APP_PROD_METHOD_GEVENT = 'gevent'
APP_PROD_METHOD_TORNADO = 'tornado'
APP_PROD_METHOD_MEINHELD = 'meinheld'
APP_PROD_METHOD = APP_PROD_METHOD_GEVENT.lower()
# definition of tester cycle, it will test every CYCLE_TESTER second
CYCLE_TESTER = 10
# definition of getter cycle, it will get proxy every CYCLE_GETTER second
CYCLE_GETTER = 100
GET_TIMEOUT = 10
# flags of enable
ENABLE_TESTER = True
ENABLE_GETTER = True
ENABLE_SERVER = True

# definition of flags
IS_WINDOWS = True
DEV_MODE, TEST_MODE, PROD_MODE = 'dev', 'test', 'prod'
APP_ENV = DEV_MODE.lower()
APP_DEBUG = True if APP_ENV == DEV_MODE else False
APP_DEV = IS_DEV = APP_ENV == DEV_MODE
APP_PROD = IS_PROD = APP_ENV == PROD_MODE
APP_TEST = IS_TEST = APP_ENV == TEST_MODE
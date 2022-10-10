from flask import Flask, g
from proxypool.RedisClient import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED, IS_DEV


__all__ = ['app']

app = Flask(__name__)
if IS_DEV:
    app.debug = True


def get_conn():
    """
    get redis client object
    :return:
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    """
    get home page, you can define your own templates
    :return:
    """
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    return conn.random().string()

@app.route('/random_withscore')
def get_proxy_withscore():
    """
    get a random proxy with score
    :return: count, int
    """
    conn = get_conn()
    return conn.random_with_score().string_with_score()



@app.route('/all')
def get_proxy_all():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    proxies = conn.all()
    proxies_string = ''
    if proxies:
        for proxy in proxies:
            proxies_string += str(proxy) + '<br/>'
            # proxies_string += str(proxy) + '\n'

    return proxies_string

@app.route('/all_withscore')
def get_proxy_all_withscore():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    proxies = conn.all_withscore()
    proxies_string = ''
    if proxies:
        for proxy in proxies:
            proxies_string += proxy.string_with_score() + '<br/>'
            # proxies_string += proxy.string_with_score() + '\n'

    return proxies_string


@app.route('/count')
def get_count():
    """
    get the count of proxies
    :return: count, int
    """
    conn = get_conn()
    return str(conn.count())

    


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)

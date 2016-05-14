def hello(env, start_response):
    queries = env.QUERY_STRING.split('&')
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return '/n/r'.join(queries)

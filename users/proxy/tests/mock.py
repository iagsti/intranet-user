import httpretty
import functools


user = dict(
    login='3333333',
    name='Jhon Doe',
    user_type='I',
    main_email='jhondoe@cacilds.com',
    bind=[{'codigoUnidade': '14'}]
)


def path_list():
    return [
        {
            'uri': 'http://localhost/test',
            'method': 'GET',
            'body': '{"content": "content"}',
            'headers': {'Content-Type': 'application/json'},
        },
    ]


def mock_uri(fn):
    @functools.wraps(fn)
    @httpretty.activate
    def wrapper(*args, **kwargs):
        register_uri()
        response = fn(*args, **kwargs)
        return response
    return wrapper


def register_uri():
    uri_list = path_list()
    for uri in uri_list:
        httpretty.register_uri(
            getattr(httpretty, uri.get('method')),
            uri=uri.get('uri'),
            body=uri.get('body'),
            headers=uri.get('headers')
        )

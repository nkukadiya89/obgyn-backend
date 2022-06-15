from decouple import config
import jwt


def decode_token(token):
    payload = jwt.decode(token, None,None)

    return payload


def my_middleware(get_response):
    def my_function(request):
        token = request.headers["Authorization"].split(" ")[1]

        response = get_response(request)
        return response
    return my_function
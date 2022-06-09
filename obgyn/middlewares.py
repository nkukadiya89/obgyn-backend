from decouple import config
import jwt


def decode_token(token):
    print(token)
    payload = jwt.decode(token, None,None)

    return payload


def my_middleware(get_response):
    def my_function(request):
        # print("before", dir(request))
        token = request.headers["Authorization"].split(" ")[1]

        print(decode_token(token))
        # print("Before",request.body.decode('utf-8'))
        # print("dir",dir(request))
        response = get_response(request)
        # print("After",request)
        return response
    return my_function
import binascii
import os
import jwt


class ApiAimoAuth:

    def __init__(self):
        self.token = None

    @property
    def secret_key(self):
        return

    @secret_key.getter
    def secret_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __generate_jwt(self, values):
        encoded_jwt = jwt.encode(values, "secret", algorithm="HS256").decode('utf-8')
        return encoded_jwt

    @classmethod
    def decode_jwt(cls, jwt_encode, refresh= False):
        print(refresh,567)
        if refresh:
            token = jwt_encode.split("Token ")[-1]
            decode = jwt.decode(token, "secret", False,algorithms=["HS256"])
            return decode

        try:
            token = jwt_encode.split("Token ")[-1]
            decode = jwt.decode(token, "secret", algorithms=["HS256"])
            return decode
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}
        except  Exception as e:
            raise e

    @property
    def get_jwt(self):
        return

    @get_jwt.setter
    def get_jwt(self, values):
        encode_jwt = self.__generate_jwt(values)
        self.token = f"Token {encode_jwt}"

def create_token(auth,id_item, model, exp):
    secret = auth.secret_key
    model.create({
        "user_id": id_item,
        "token": secret,
        "date_expirated": exp
    })
    auth.get_jwt = {
        "exp": exp,
        "token": secret
    }
    data_response = auth.token
    return data_response

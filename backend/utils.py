import os

class MaxLength() :
    user_id = 32
    user_pwd = 32
    user_name = 128
    phone_number = 16
    email = 128
    store_name = 64
    store_owner = 128
    store_address = 256
    store_tel_number = 16
    group_name = 64
    product_name = 64
    option_name = 64
    suboption_name = 64

class MinLength() :
    user_id = 5
    user_pwd = 8
    user_name = 2
    phone_number = 11
    email = 6
    store_name = 1
    store_owner = 2
    store_address = 14
    store_tel_number = 11
    group_name = 1
    product_name = 1
    option_name = 1
    suboption_name = 1

class Path() :
    PATH = os.getcwd()
    IMAGE = PATH + "/images"
    ADMIN = IMAGE + "/admin"


# termux 시작 시, 자동실행
#  http://john-home.iptime.org:8085/xe/index.php?mid=board_ZoED57&document_srl=12398

# ubuntu 시작 시, 자동실행
# https://klkl0.tistory.com/127
# https://leeseongho.com/14

# flask cors
# https://webisfree.com/2020-01-01/python-flask%EC%97%90%EC%84%9C-cors-cross-origin-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0
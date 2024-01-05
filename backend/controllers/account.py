import sys
import os
import random
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from flask_jwt_extended import *
from utils import *
from statusCode import *
from config import *
from models.mysql import DB
from models.Admins import Admins
from models.StoreInfo import StoreInfo
from models.TableList import TableList
from models.Product import Product

def checkField(data) :
    keyword = []

    if "user_id" in data :
        if len(data["user_id"]) < MinLength.user_id or len(data["user_id"]) > MaxLength.user_id :
            keyword.append("user_id")

    if "after_pwd" in data :
        if len(data["after_pwd"]) < MinLength.user_pwd or len(data["after_pwd"]) > MaxLength.user_pwd :
            keyword.append("after_pwd")
    
    if "user_pwd" in data :
        if len(data["user_pwd"]) < MinLength.user_pwd or len(data["user_pwd"]) > MaxLength.user_pwd :
            keyword.append("user_pwd")

    if "name" in data :
        if len(data["name"]) < MinLength.user_name or len(data["name"]) > MaxLength.user_name :
            keyword.append("name")

    if "phone" in data :
        if len(data["phone"]) < MinLength.phone_number or len(data["phone"]) > MaxLength.phone_number :
            keyword.append("phone")

    if "email" in data :
        # 유효성 검사
        email = Admins.query.filter_by(email=data["email"]).first()

        if email != None :
            keyword.append("email:already_exist")

        # 길이 검사
        memberLength = len(data["email"])
        alphaIdx = data["email"].find('@')
        dotIdx = data["email"].find('.')
        if memberLength < MinLength.email or memberLength > MaxLength.email or alphaIdx <= 1 or dotIdx <= 3 or dotIdx - alphaIdx <= 1 or dotIdx+1 == memberLength :
            keyword.append("email:wrong_length")
        
    return keyword

def adminLogin(id="", pwd="") :
    user = Admins.query.filter_by(user_id=id, user_pwd=pwd).first()
    
    # 해당 아이디/비밀번호의 계정이 검색되지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    user = user.__dict__

    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}

    records = StoreInfo.query.filter_by(unique_admin=user["unique_admin"]).all() # 해당 유저 소유의 가게 리스트
    
    # dict형으로 변환
    stores = []
    for rec in records :
        dictRec = dict(rec.__dict__)
        dictRec.pop('_sa_instance_state', None)
        stores.append(dictRec)

    return {
        "result" : "Success",
        "access_token" : create_access_token(identity=id, expires_delta=False),
        "code" : Code.Success,
        "stores" : stores
    }

def userLogin(id="", pwd="") :
    user = Admins.query.filter_by(user_id=id, user_pwd=pwd).first()

    # 해당 아이디/비밀번호로 계정이 검색되지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}

    user = user.__dict__
    
    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    # 매장 목록 검색
    records = StoreInfo.query.filter_by(unique_admin=user["unique_admin"]).all() # 해당 유저 소유의 가게 리스트

    # dict형으로 변환
    stores = []
    for rec in records :
        dictRec = dict(rec.__dict__)
        dictRec.pop('_sa_instance_state', None)
        stores.append(dictRec)

    return {
        "result" : "Success",
        "code" : Code.Success,
        "stores" : stores
    }

def tableLogin(ssaid="", store_uid=-1, tableNum = -1) :
    store = StoreInfo.query.filter_by(unique_store_info=store_uid).first()
    
    # 매장이 검색되지 않을 때,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    store = store.__dict__

    # 삭제된 매장일 때,
    if store["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}

    table = TableList.query.filter_by(unique_store_info=store_uid, table_number=tableNum).first()

    # 테이블이 검색되지 않을 때,
    if table == None :
        return {"result" : "Invalid", "code" : Code.NotExistTable}
    
    dictTable = table.__dict__
    
    # 삭제된 테이블일 때,
    if dictTable["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}

    # 해당 테이블 번호가 이미 로그인 상태인지 확인할 것.
    if "isLogin" in dictTable and dictTable["isLogin"] != '' :
        return {"result" : "Invalid", "code" : Code.AlreadyLogin, "SSAID" : dictTable["isLogin"]}
    
    # 테이블 로그인 상태로 변경
    table.isLogin = ssaid
    DB.session.commit()

    # 상품 검색
    records = Product.query.filter_by(unique_store_info=store_uid).all() # 상품 리스트

    # dict형으로 변환
    products = []
    for rec in records :
        dictRec = dict(rec.__dict__)
        dictRec.pop('_sa_instance_state', None)
        products.append(dictRec)

    return {"result" : "Success", "code" : Code.Success, "products" : products}

def adminLogout(id="") :
    user = Admins.query.filter_by(user_id=id).first()

    # 아이디로 유저가 검색되지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    user = user.__dict__

    # 탈퇴한 유저일 때,
    if user["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    return {"result" : "Success", "code" : Code.Success}

def userLogout(ssaid="", store_uid=-1, tableNum=-1) :
    store = StoreInfo.query.filter_by(unique_store_info=store_uid).first()
    
    # 매장이 검색되지 않을 때,
    if store == None :
        return {"result" : "Invalid", "code" : Code.NotExistStore}
    
    store = store.__dict__

    # 삭제된 매장일 때,
    if store["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    table = TableList.query.filter_by(unique_store_info=store_uid, table_number=tableNum)

    # 테이블이 검색되지 않을 때,
    if table == None :
        return {"result" : "Invalid", "code" : Code.NotExistTable}
    
    dictTable = table.__dict__

    # 로그인 상태가 아닐 때,
    if "isLogin" in dictTable and dictTable["isLogin"] == '' :
        return {"result" : "Invalid", "code" : Code.NotLoginState}
    
    # 요청자와 로그인중인 사용자의 SSAID가 일치하지 않을 때,
    if dictTable["isLogin"] != ssaid :
        return {"result" : "Invalid", "code" : Code.NotEquals}
    
    # 로그아웃
    table.isLogin = ""
    DB.session.commit()
    
    return {"result" : "Success", "code" : Code.Success}

def signup(inputUserData={}) :
    
    fields = ["user_id", "user_pwd", "name", "phone", "email"]

    # 필수 값이 누락 됐을 때,
    for field in fields :
        if field not in inputUserData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}

    user = Admins.query.filter_by(user_id=inputUserData["user_id"]).first()

    # 이미 존재하는 아이디일 때,
    if user != None :
        user = user.__dict__

        # 탈퇴한 유저라면,
        if user["disable_date"] != None :
            return {"result" : "Invalid", "code" : Code.DeletedData}
        
        return {"result" : "Invalid", "code" : Code.AlreadyExistID}
    
    # 이미 존재하는 이메일일 때,
    user = Admins.query.filter_by(email=inputUserData["email"]).first()

    if user != None :
        return {"result" : "Invalid", "code" : Code.AlreadyEmail}

    # 이메일 인증 기능

    keyword = checkField(inputUserData)

    # 입력 필드 확인
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}

    # DB에 회원 추가
    user = Admins(
        id=inputUserData["user_id"],
        pwd=inputUserData["user_pwd"],
        name=inputUserData["name"],
        number=inputUserData["phone"],
        email=inputUserData["email"]
    )
    DB.session.add(user)
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def delete_account(id='') :
    user = Admins.query.filter_by(user_id=id).first()

    # 아이디로 유저가 검색되지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    dictUser = user.__dict__

    # 이미 탈퇴한 유저일 때,
    if dictUser["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    # 탈퇴 처리
    user.disable_date = datetime.now()
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def change_account(inputUserData={}) :
    user = Admins.query.filter_by(user_id=inputUserData["user_id"]).first()

    # 아이디로 유저가 검색되지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    dictUser = user.__dict__

    # 이미 탈퇴한 유저일 때,
    if dictUser["disable_date"] != None :
        return {"result" : "Invalid", "code" : Code.DeletedData}
    
    # 비밀번호 변경 시 기존 비밀번호 일치 확인
    if "before_pwd" in inputUserData and "after_pwd" in inputUserData and inputUserData["before_pwd"] != dictUser["user_pwd"] :
        return {"result" : "Invalid", "code" : Code.WrongPWD}

    keyword = checkField(inputUserData)

    # 양식이 맞지 않은 정보가 존재할 때,
    if len(keyword) > 0 :
        return {"result" : "Invalid", "code" : Code.WrongDataForm, "keyword" : keyword}
    
    # 정보 수정
    ## 비밀번호 수정
    if "before_pwd" in inputUserData and "after_pwd" in inputUserData :
        user.user_pwd = inputUserData["after_pwd"]

    ## 이름 수정
    if "name" in inputUserData :
        user.name = inputUserData["name"]

    ## 전화번호 수정
    if "phone" in inputUserData :
        user.phone_number = inputUserData["phone"]

    ## 이메일 수정
    if "email" in inputUserData :
        user.email = inputUserData["email"]
    
    DB.session.commit()

    return {"result" : "Success", "code" : Code.Success}

def get_isExist(userInputData={}) :

    # 필수 필드가 누락 됐을 때,
    if "user_id" not in userInputData :
        return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    isExist = 0
    user = Admins.query.filter_by(user_id=userInputData["user_id"]).first()

    # 해당 아이디를 가진 유저가 이미 존재할 떄,
    if user != None :
        isExist = 1

    return {"result" : "Success", "code" : Code.Success, "isExist" : isExist}

def get_account(id=-1) :
    user = Admins.query.filter_by(user_id=id).first()
    
    # 아이디로 유저가 검색되지 않을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    # dict형으로 변환
    user = dict(user.__dict__)
    user.pop('_sa_instance_state', None)

    # 비밀번호는 마스킹 후 반환
    user["user_pwd"] = ""

    return {"result" : "Success", "code" : Code.Success, "user" : user}

def find_account(inputData={}) :
    # 필수 필드가 누락 됐을 때,
    fields = ['name', 'tel_num', 'email']
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}
    
    user = Admins.query.filter_by(
        name=inputData["name"],
        phone_number=inputData["tel_num"],
        email=inputData["email"],
        disable_date=None
    ).first()

    # 해당 조건으로 아이디를 찾을 수 없을 때,
    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    # dict형으로 변환
    user = dict(user.__dict__)
    user.pop('_sa_instance_state', None)

    user["user_pwd"] = ""

    return {"result" : "Success", "code" : Code.Success, "user" : user}

def find_password(inputData={}) :
    fields = ["user_id"]

    # 필수 필드가 누락됐을 때,
    for field in fields :
        if field not in inputData :
            return {"result" : "Invalid", "code" : Code.MissingRequireField}

    # 해당 유저가 존재하지 않을 때,
    user = Admins.query.filter_by(user_id=inputData["user_id"]).first()

    if user == None :
        return {"result" : "Invalid", "code" : Code.NotExistID}
    
    # 랜덤 비밀번호 생성 (대문자 + 소문자 + 숫자 + 특수문자)
    reset_pwd = ""
    alpha = list(set("abcdefghijklmnopqrstuvwxyz") | set("abcdefghijklmnopqrstuvwxyz".upper()) | set("1234567890") | set("~!@#$%^&*()_-+="))
    length = random.randint(12, 20)

    for _ in range(length) :
        reset_pwd += random.choice(alpha)
    
    # 랜덤 비밀번호로 변경
    user.user_pwd = reset_pwd
    DB.session.commit()

    # SMTP 서버와 연결
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # 로그인
    smtp.login(API.smtp_account, API.smtp_password)

    # 메일 기본 정보
    msg = MIMEMultipart()
    msg["Subject"] = f"K-올림포스 계정 암호 재설정"
    msg["From"] = "K-올림포스"
    msg["To"] = user.email

    # 메일 HTML 내용
    html_message = f"""
    <!doctype html>
        <html lang=ko>
            <head>
                <meta charset=utf-8>
                <title>mail<title>
            </head>
            <body>
                <p style="color: #707070;">K-올림포스 계정</p>
                <p style="color: #2672ec; font-size: 41px;">암호 재설정 코드</p>
                <p style="color: #707070;">이 코드를 사용하여 K-올림포스 계정의 암호를 재설정하세요.</p>
                <p style="color: #707070;">코드는 <span style="color: #2a2a2a; font-weight: bold;">{reset_pwd}</span>입니다.</p>
                <p style="color: #707070;">감사합니다.</p>
            </body>
        </html>
    """
    html_body = MIMEText(html_message, 'html')
    msg.attach(html_body)

    # 메일 본문 내용
    content = "비밀번호 : " + reset_pwd
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)

    # 이미지 파일 첨부
    # image_path = Path.IMAGE + "/thumnail.png"
    # ext = os.path.splitext(image_path)[1]
    
    # with open(image_path, 'rb') as file :
    #     img = MIMEImage(file.read())
    #     img.add_header('Content-Disposition', 'attachment', filename="title" + ext)
    #     msg.attach(img)

    # 메일 전송
    smtp.sendmail(API.smtp_account, user.email, msg.as_string())

    # SMTP 서버와 연결 해제
    smtp.quit()

    return {"result" : "Success", "code" : Code.Success}
class Code() :
    # 성공
    Success = 100

    # 요청 필드에 관한 코드
    MissingToken = 200
    MissingRequireField = 201
    DeletedData = 202
    WrongPWD = 203
    WrongDataForm = 204
    NotEquals = 205

    # 존재하지 않는 데이터에 관한 코드
    NotExistID = 300
    NotExistStore = 301
    NotExistTable = 302
    NotExistGroup = 304
    NotExistProduct = 306
    NotExistProductOption = 307
    NotExistProductSuboption = 307
    NotExistOrder = 308
    NotExistState = 309
    NotExistVersion = 310

    # 이미 존재하는 데이터에 관한 코드
    AlreadyExistID = 400
    AlreadyExistStore = 401
    AlreadyExistGroup = 402
    AlreadyExistOption = 404

    # 로그인에 관한 코드
    AlreadyLogin = 500
    NotLoginState = 501

class OrderState() :
    Receipt = 0
    Processing = 1
    Cancel = 2
    Complete = 3

    def isExist(code) :
        if type(code) is type(1) and code >= 0 and code <= 3 :
            return True
        return False
    
class TableState() :
    Empty = 0
    Receipt = 1
    Processing = 2
    Complete = 3

    def isExist(code) :
        if type(code) is type(1) and code >= 0 and code <= 3 :
            return True
        return False
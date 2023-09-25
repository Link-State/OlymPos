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
    NotExistVersion = 310

    # 이미 존재하는 데이터에 관한 코드
    AlreadyExistID = 400
    AlreadyExistStore = 401
    AlreadyExistGroup = 402

    # 로그인에 관한 코드
    AlreadyLogin = 500
    NotLoginState = 501

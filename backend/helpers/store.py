
from datetime import datetime
from models.mysql import DB
from models.TableList import TableList
from models.Version import Version

def modify_store(store, inputStoreInfo={}) :
    # 매장 정보 수정
    if "name" in inputStoreInfo :
        store.store_name = inputStoreInfo["name"]

    if "owner" in inputStoreInfo :
        store.store_owner = inputStoreInfo["owner"]

    if "address" in inputStoreInfo :
        store.store_address = inputStoreInfo["address"]

    if "tel_num" in inputStoreInfo :
        store.store_tel_number = inputStoreInfo["tel_num"]
    
    if "count" in inputStoreInfo :
        tables = TableList.query.filter_by(unique_store_info=store.unique_store_info).order_by(TableList.table_number).all()

        current = store.table_count # 현재 활성화된 테이블 갯수
        maximum = len(tables) # DB에 생성된 테이블 갯수
        request = inputStoreInfo["count"] # 활성화할 테이블 갯수
        now = datetime.now()
        now_lnt = int(now.strftime('%Y%m%d%H%M%S%f')[:-3]) # 현재 시간

        # 현재 활성화된 테이블 갯수와 활성화할 테이블 갯수가 같지 않을 때, DB상 기록된 테이블 갯수 수정
        if request != current :
            store.table_count = request
            store.last_modify_date = now

            version = Version.query.get(store.unique_store_info)
            version.table_list = now_lnt
        
        # 활성화할 테이블 갯수가 현재 활성화된 테이블 갯수보다 클 경우,
        if request > current :

            middle = request
            if request > maximum :
                middle = maximum

            # 재활성화
            for i in range(current + 1, middle + 1) :
                tables[i-1].disable_date = None

            # 생성
            for i in range(middle + 1, request + 1) :
                table = TableList(store=store.unique_store_info, number=i, state=0)
                DB.session.add(table)

        # 활성화할 테이블 갯수가 현재 활성화된 테이블 갯수보다 작을 경우,
        elif request < current :
            # 비활성화
            for i in range(request + 1, current + 1) :
                tables[i-1].isLogin = ""
                tables[i-1].table_state = 0
                tables[i-1].disable_date = now
    
    DB.session.commit()
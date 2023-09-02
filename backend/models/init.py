import sys
import os
import pymysql

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import API

connection = pymysql.connect(
        host=API.host,
        user=API.mysql_username,
        password=API.mysql_pwd,
        database=API.database,
        port=API.mysql_port,
        use_unicode=True,
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
print("connect mysql")

command = connection.cursor()

#테이블 삭제
command.execute("DROP TABLE IF EXISTS Selected_option;")
command.execute("DROP TABLE IF EXISTS Order_list;")
command.execute("DROP TABLE IF EXISTS Product_suboption;")
command.execute("DROP TABLE IF EXISTS Product_Option_relations;")
command.execute("DROP TABLE IF EXISTS Product_option;")
command.execute("DROP TABLE IF EXISTS Product;")
command.execute("DROP TABLE IF EXISTS Product_group;")
command.execute("DROP TABLE IF EXISTS Table_list;")
command.execute("DROP TABLE IF EXISTS Store_info;")
command.execute("DROP TABLE IF EXISTS Admins;")
print("Clear Table")



# 스키마 생성
## 관리자 스키마
command.execute("""CREATE TABLE Admins (
                unique_admin INT,
                user_id VARCHAR(32) NOT NULL,
                user_pwd VARCHAR(32) NOT NULL,
                name VARCHAR(128) NOT NULL,
                phone_number VARCHAR(16) NOT NULL,
                email VARCHAR(128) NOT NULL,
                disable_date DATETIME
                );""")

## 매장 스키마
command.execute("""CREATE TABLE Store_info (
                unique_store_info INT,
                unique_admin INT NOT NULL,
                store_name VARCHAR(64) NOT NULL,
                store_owner VARCHAR(128) NOT NULL,
                store_address VARCHAR(256) NOT NULL,
                store_tel_number VARCHAR(16) NOT NULL,
                table_count INT NOT NULL,
                last_modify_date DATETIME NOT NULL,
                disable_date DATETIME
                );""")

## 테이블 스키마
command.execute("""CREATE TABLE Table_list (
                unique_store_info INT,
                table_number INT,
                table_state INT NOT NULL,
                isLogin LONGTEXT NOT NULL,
                disable_date DATETIME
                );""")

## 상품 카테고리 스키마
command.execute("""CREATE TABLE Product_group (
                unique_product_group INT,
                unique_store_info INT NOT NULL,
                group_name VARCHAR(64) NOT NULL,
                disable_date DATETIME
                );""")

## 상품 스키마
command.execute("""CREATE TABLE Product (
                unique_product INT,
                unique_store_info INT NOT NULL,
                unique_product_group INT NOT NULL,
                product_name VARCHAR(64) NOT NULL,
                price INT NOT NULL,
                image LONGTEXT,
                description LONGTEXT,
                amount INT NOT NULL,
                disable_date DATETIME
                );""")

## 상품 옵션 스키마
command.execute("""CREATE TABLE Product_option (
                unique_product_option INT,
                unique_store_info INT NOT NULL,
                option_name VARCHAR(64) NOT NULL,
                price INT NOT NULL,
                suboption_offer INT NOT NULL,
                disable_date DATETIME
                );""")

## 상품-옵션 관계 스키마
command.execute("""CREATE TABLE Product_Option_relations (
                unique_product INT NOT NULL,
                unique_product_option INT NOT NULL
                );""")

## 상품 서브옵션 스키마
command.execute("""CREATE TABLE Product_suboption (
                unique_product_suboption INT,
                unique_product_option INT NOT NULL,
                suboption_name VARCHAR(64) NOT NULL,
                price INT NOT NULL,
                amount INT NOT NULL,
                disable_date DATETIME
                );""")

## 주문 내역 스키마
command.execute("""CREATE TABLE Order_list (
                unique_order INT,
                unique_store_info INT NOT NULL,
                unique_product INT NOT NULL,
                table_number INT NOT NULL,
                amount INT NOT NULL,
                order_state INT NOT NULL,
                order_date DATETIME NOT NULL
                );""")

## 선택 옵션 스키마
command.execute("""CREATE TABLE Selected_option (
                unique_selected_option INT,
                unique_order INT NOT NULL,
                unique_product_option INT NOT NULL,
                unique_product_suboption INT
                );""")



# 속성 추가
## 관리자
### 관리자 기본키
command.execute("""ALTER TABLE Admins
                MODIFY unique_admin INT PRIMARY KEY AUTO_INCREMENT
                ;""")

### 관리자 고유성
command.execute("""ALTER TABLE Admins
                MODIFY user_id VARCHAR(32) UNIQUE
                ;""")

## 매장
### 매장 기본키
command.execute("""ALTER TABLE Store_info
                MODIFY unique_store_info INT PRIMARY KEY AUTO_INCREMENT
                ;""")

### 매장 외래키
command.execute("""ALTER TABLE Store_info
                ADD FOREIGN KEY (unique_admin)
                REFERENCES Admins(unique_admin)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

## 테이블
### 테이블 기본키
command.execute("""ALTER TABLE Table_list
                ADD PRIMARY KEY (
                unique_store_info, table_number)
                ;""")

### 테이블 외래키
command.execute("""ALTER TABLE Table_list
                ADD FOREIGN KEY (unique_store_info)
                REFERENCES Store_info(unique_store_info)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 테이블 제약조건
command.execute("""ALTER TABLE Table_list
                ADD CONSTRAINT table_state__conflict__at__Table_list
                CHECK (table_state IN (0, 1, 2, 3))
                ;""")

## 상품 카테고리
### 상품 카테고리 기본키
command.execute("""ALTER TABLE Product_group
                MODIFY unique_product_group INT PRIMARY KEY AUTO_INCREMENT
                ;""")

### 상품 카테고리 외래키
command.execute("""ALTER TABLE Product_group
                ADD FOREIGN KEY (unique_store_info)
                REFERENCES Store_info(unique_store_info)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

## 상품
### 상품 기본키
command.execute("""ALTER TABLE Product
                MODIFY unique_product INT PRIMARY KEY AUTO_INCREMENT
                ;""")

### 상품 외래키
command.execute("""ALTER TABLE Product
                ADD FOREIGN KEY (unique_product_group)
                REFERENCES Product_group(unique_product_group)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 상품 외래키
command.execute("""ALTER TABLE Product
                ADD FOREIGN KEY (unique_store_info)
                REFERENCES Store_info(unique_store_info)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 상품 제약조건
command.execute("""ALTER TABLE Product
                ADD CONSTRAINT price_conflict_at_Product
                CHECK (0 <= price)
                ;""")

### 상품 제약조건
command.execute("""ALTER TABLE Product
                ADD CONSTRAINT amount_conflict_at_Product
                CHECK (-1 <= amount)
                ;""")

### 상품 옵션 기본키
command.execute("""ALTER TABLE Product_option
                MODIFY unique_product_option INT PRIMARY KEY AUTO_INCREMENT
                ;""")

### 상품 옵션 외래키
command.execute("""ALTER TABLE Product_option
                ADD FOREIGN KEY (unique_store_info)
                REFERENCES Store_info(unique_store_info)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 상품 옵션 제약조건
command.execute("""ALTER TABLE Product_option
                ADD CONSTRAINT price__conflict__at__Product_option
                CHECK (0 <= price)
                ;""")

## 상품-옵션 관계
### 상품-옵션 관계 기본키
command.execute("""ALTER TABLE Product_Option_relations
                ADD PRIMARY KEY (unique_product, unique_product_option)
                ;""")

### 상품-옵션 관계 외래키
command.execute("""ALTER TABLE Product_Option_relations
                ADD FOREIGN KEY (unique_product)
                REFERENCES Product(unique_product)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 상품-옵션 관계 외래키
command.execute("""ALTER TABLE Product_Option_relations
                ADD FOREIGN KEY (unique_product_option)
                REFERENCES Product_option(unique_product_option)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

## 상품 서브옵션
### 상품 서브옵션 기본키
command.execute("""ALTER TABLE Product_suboption
                MODIFY unique_product_suboption INT PRIMARY KEY AUTO_INCREMENT
                ;""")

### 상품 서브옵션 외래키
command.execute("""ALTER TABLE Product_suboption
                ADD FOREIGN KEY (unique_product_option)
                REFERENCES Product_option(unique_product_option)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 상품 서브옵션 제약조건
command.execute("""ALTER TABLE Product_suboption
                ADD CONSTRAINT price__conflict__at__Product_suboption
                CHECK (0 <= price)
                ;""")

### 상품 서브옵션 제약조건
command.execute("""ALTER TABLE Product_suboption
                ADD CONSTRAINT amount__confilct__at__Product_suboption
                CHECK (-1 <= amount)
                ;""")

## 주문 내역
### 주문 내역 기본키
command.execute("""ALTER TABLE Order_list
                MODIFY unique_order INT PRIMARY KEY AUTO_INCREMENT
                ;""")

### 주문 내역 외래키
command.execute("""ALTER TABLE Order_list
                ADD FOREIGN KEY (unique_store_info, table_number)
                REFERENCES Table_list(unique_store_info, table_number)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 주문 내역 외래키
command.execute("""ALTER TABLE Order_list
                ADD FOREIGN KEY (unique_product)
                REFERENCES Product(unique_product)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 주문 내역 제약조건
command.execute("""ALTER TABLE Order_list
                ADD CONSTRAINT amount__conflict__at__Order_list
                CHECK (-1 <= amount)
                ;""")

### 주문 내역 제약조건
command.execute("""ALTER TABLE Order_list
                ADD CONSTRAINT order_state__conflict__at__Order_list
                CHECK (order_state IN (0, 1, 2))
                ;""")

## 선택 옵션
### 선택 옵션 기본키
command.execute("""ALTER TABLE Selected_option
                MODIFY unique_selected_option INT PRIMARY KEY AUTO_INCREMENT
                ;""")

### 선택 옵션 외래키
command.execute("""ALTER TABLE Selected_option
                ADD FOREIGN KEY (unique_order)
                REFERENCES Order_list(unique_order)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 선택 옵션 외래키
command.execute("""ALTER TABLE Selected_option
                ADD FOREIGN KEY (unique_product_option)
                REFERENCES Product_option(unique_product_option)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")

### 선택 옵션 외래키
command.execute("""ALTER TABLE Selected_option
                ADD FOREIGN KEY (unique_product_suboption)
                REFERENCES Product_suboption(unique_product_suboption)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                ;""")



# 테스트 입력
## 관리자 계정
command.execute("""INSERT INTO Admins VALUES(
                0,
                'link_state',
                'asdf1234',
                'kor_people',
                '010-1234-5678',
                'link@asd.qwe',
                NULL
                );""")

## 매장
tables = 5
command.execute(f"""INSERT INTO Store_info VALUES(
                0,
                1,
                '날아라 닭다리',
                '먹신',
                '냠냠민국 쩝쩝시 치킨로 12-97',
                '033-123-4567',
                {tables},
                '2023-09-02 17:55:00',
                NULL
                );""")

## 테이블
for t in range(1, tables+1) :
    command.execute(f"""INSERT INTO Table_list VALUES(
                    1,
                    {t},
                    0,
                    '',
                    NULL
                    );""")

## 상품 카테고리
command.execute("""INSERT INTO Product_group VALUES(
                0,
                1,
                '순살',
                NULL
                );""")

## 상품
command.execute("""INSERT INTO Product VALUES(
                0,
                1,
                1,
                '월계수찜닭',
                10000,
                '',
                '',
                -1,
                NULL
                );""")

## 옵션1
command.execute("""INSERT INTO Product_option VALUES(
                0,
                1,
                '닭털당면',
                0,
                1,
                NULL
                );""")

## 옵션2
command.execute("""INSERT INTO Product_option VALUES(
                0,
                1,
                '소발굽만두 5개 추가',
                5000,
                0,
                NULL
                );""")

## 서브옵션1
command.execute("""INSERT INTO Product_suboption VALUES(
                0,
                1,
                '많이',
                1000,
                -1,
                NULL
                );""")

## 서브옵션2
command.execute("""INSERT INTO Product_suboption VALUES(
                0,
                1,
                '적게',
                500,
                -1,
                NULL
                );""")

## 상품-옵션 관계1
command.execute("""INSERT INTO Product_Option_relations VALUES(
                1,
                1
                );""")

## 상품-옵션 관계2
command.execute("""INSERT INTO Product_Option_relations VALUES(
                1,
                2
                );""")

## 주문 내역
command.execute("""INSERT INTO Order_list VALUES(
                0,
                1,
                1,
                1,
                2,
                0,
                '2023-07-28 20:22:12'
                );""")

## 선택 옵션
command.execute("""INSERT INTO Selected_option VALUES(
                0,
                1,
                1,
                2
                );""")

## 선택 옵션
command.execute("""INSERT INTO Selected_option VALUES(
                0,
                1,
                2,
                NULL
                );""")


connection.commit()
connection.close()

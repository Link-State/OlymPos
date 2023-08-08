import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main import connection, command

#테이블 삭제
command.execute("DROP TABLE IF EXISTS Selected_option;")
command.execute("DROP TABLE IF EXISTS Order_list;")
command.execute("DROP TABLE IF EXISTS Product_suboption;")
command.execute("DROP TABLE IF EXISTS Product_option;")
command.execute("DROP TABLE IF EXISTS Product;")
command.execute("DROP TABLE IF EXISTS Product_group;")
command.execute("DROP TABLE IF EXISTS Table_list;")
command.execute("DROP TABLE IF EXISTS Store_info;")
command.execute("DROP TABLE IF EXISTS Admins;")

# 테이블 생성
command.execute("CREATE TABLE Admins (unique_admin INT, user_id VARCHAR(32) NOT NULL, user_pwd VARCHAR(32) NOT NULL, name VARCHAR(128) NOT NULL, phone_number VARCHAR(11) NOT NULL, email VARCHAR(128) NOT NULL);")
command.execute("CREATE TABLE Store_info (unique_store_info INT, unique_admin INT NOT NULL, store_name VARCHAR(64) NOT NULL, store_owner VARCHAR(128) NOT NULL, store_address VARCHAR(64) NOT NULL, store_tel_number VARCHAR(11) NOT NULL, table_count INT NOT NULL, isLogin INT);")
command.execute("CREATE TABLE Table_list (unique_store_info INT, table_number INT, table_state INT NOT NULL, isLogin INT);")
command.execute("CREATE TABLE Product_group (unique_product_group INT, unique_store_info INT NOT NULL, group_name VARCHAR(64) NOT NULL);")
command.execute("CREATE TABLE Product (unique_product INT, unique_store_info INT NOT NULL, unique_product_group INT NOT NULL, product_name VARCHAR(64) NOT NULL, price INT NOT NULL, image LONGTEXT, description LONGTEXT, amount INT NOT NULL);")
command.execute("CREATE TABLE Product_option (unique_product_option INT, unique_store_info INT NOT NULL, unique_product INT NOT NULL, option_name VARCHAR(64) NOT NULL, price INT NOT NULL, suboption_offer INT NOT NULL);")
command.execute("CREATE TABLE Product_suboption (unique_product_suboption INT, unique_product_option INT NOT NULL, suboption_name VARCHAR(64) NOT NULL, price INT NOT NULL, amount INT NOT NULL);")
command.execute("CREATE TABLE Order_list (unique_order INT, unique_store_info INT NOT NULL, unique_product INT NOT NULL, table_number INT NOT NULL, amount INT NOT NULL, order_state INT NOT NULL, order_date DATETIME NOT NULL);")
command.execute("CREATE TABLE Selected_option (unique_selected_option INT, unique_order INT NOT NULL, unique_product_option INT NOT NULL, unique_product_suboption INT);")

# 속성 추가
command.execute("ALTER TABLE Admins ADD PRIMARY KEY (unique_admin);")
command.execute("ALTER TABLE Admins ADD UNIQUE (user_id);")

command.execute("ALTER TABLE Store_info ADD PRIMARY KEY (unique_store_info);")
command.execute("ALTER TABLE Store_info ADD FOREIGN KEY (unique_admin) REFERENCES Admins(unique_admin) ON UPDATE CASCADE ON DELETE CASCADE;")

command.execute("ALTER TABLE Table_list ADD PRIMARY KEY (unique_store_info, table_number);")
command.execute("ALTER TABLE Table_list ADD FOREIGN KEY (unique_store_info) REFERENCES Store_info(unique_store_info) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Table_list ADD CONSTRAINT table_state__conflict__at__Table_list CHECK (table_state IN (0, 1, 2, 3));")

command.execute("ALTER TABLE Product_group ADD PRIMARY KEY (unique_product_group);")
command.execute("ALTER TABLE Product_group ADD FOREIGN KEY (unique_store_info) REFERENCES Store_info(unique_store_info) ON UPDATE CASCADE ON DELETE CASCADE;")

command.execute("ALTER TABLE Product ADD PRIMARY KEY (unique_product);")
command.execute("ALTER TABLE Product ADD FOREIGN KEY (unique_product_group) REFERENCES Product_group(unique_product_group) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Product ADD FOREIGN KEY (unique_store_info) REFERENCES Store_info(unique_store_info) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Product ADD CONSTRAINT price_conflict_at_Product CHECK (0 <= price);")
command.execute("ALTER TABLE Product ADD CONSTRAINT amount_conflict_at_Product CHECK (-1 <= amount);")

command.execute("ALTER TABLE Product_option ADD PRIMARY KEY (unique_product_option);")
command.execute("ALTER TABLE Product_option ADD FOREIGN KEY (unique_product) REFERENCES Product(unique_product) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Product_option ADD FOREIGN KEY (unique_store_info) REFERENCES Store_info(unique_store_info) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Product_option ADD CONSTRAINT price__conflict__at__Product_option CHECK (0 <= price);")

command.execute("ALTER TABLE Product_suboption ADD PRIMARY KEY (unique_product_suboption);")
command.execute("ALTER TABLE Product_suboption ADD FOREIGN KEY (unique_product_option) REFERENCES Product_option(unique_product_option) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Product_suboption ADD CONSTRAINT price__conflict__at__Product_suboption CHECK (0 <= price);")
command.execute("ALTER TABLE Product_suboption ADD CONSTRAINT amount__confilct__at__Product_suboption CHECK (-1 <= amount);")

command.execute("ALTER TABLE Order_list ADD PRIMARY KEY (unique_order);")
command.execute("ALTER TABLE Order_list ADD FOREIGN KEY (unique_store_info, table_number) REFERENCES Table_list(unique_store_info, table_number) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Order_list ADD FOREIGN KEY (unique_product) REFERENCES Product(unique_product) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Order_list ADD CONSTRAINT amount__conflict__at__Order_list CHECK (-1 <= amount);")
command.execute("ALTER TABLE Order_list ADD CONSTRAINT order_state__conflict__at__Order_list CHECK (order_state IN (0, 1, 2));")

command.execute("ALTER TABLE Selected_option ADD PRIMARY KEY (unique_selected_option);")
command.execute("ALTER TABLE Selected_option ADD FOREIGN KEY (unique_order) REFERENCES Order_list(unique_order) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Selected_option ADD FOREIGN KEY (unique_product_option) REFERENCES Product_option(unique_product_option) ON UPDATE CASCADE ON DELETE CASCADE;")
command.execute("ALTER TABLE Selected_option ADD FOREIGN KEY (unique_product_suboption) REFERENCES Product_suboption(unique_product_suboption) ON UPDATE CASCADE ON DELETE CASCADE;")


# 테스트 입력
"""
command.execute("INSERT INTO Admins VALUES(0, 'link_state', 'asdf1234', 'kor_people', '01012345678', 'link@asd.qwe', 0);")
command.execute("INSERT INTO Store_info VALUES(1, 0, '날아라 닭다리', '먹신', '냠냠민국 쩝쩝시 치킨로 12-97', '0331234567');")
command.execute("INSERT INTO Table_list VALUES(1, 2, 0, 0);")
command.execute("INSERT INTO Product_group VALUES(3, 1, '순살');")
command.execute("INSERT INTO Product VALUES(4, 3, '월계수찜닭', 10000, '', '', -1);")
command.execute("INSERT INTO Product_option VALUES(5, 4, '닭털당면', 0, 1);")
command.execute("INSERT INTO Product_option VALUES(6, 4, '소발굽만두 5개 추가', 5000, 0);")
command.execute("INSERT INTO Product_suboption VALUES(7, 5, '많이', 1000, -1);")
command.execute("INSERT INTO Product_suboption VALUES(8, 5, '적게', 500, -1);")
command.execute("INSERT INTO Order_list VALUES(9, 1, 4, 2, 1, 0, '2023-07-28 20:22:12');")
command.execute("INSERT INTO Selected_option VALUES(10, 9, 5, 7);")
command.execute("INSERT INTO Selected_option VALUES(11, 9, 6, NULL);")
"""

connection.commit()


# connection.close()

# termux 시작 시, 자동실행
#  http://john-home.iptime.org:8085/xe/index.php?mid=board_ZoED57&document_srl=12398
# ubuntu 시작 시, 자동실행
# https://klkl0.tistory.com/127
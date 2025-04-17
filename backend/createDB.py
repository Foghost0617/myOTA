import pymysql


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    charset='utf8mb4',
    autocommit=True
)

cursor = conn.cursor()

#
cursor.execute("CREATE DATABASE IF NOT EXISTS travel_agency DEFAULT CHARACTER SET utf8mb4;")
cursor.execute("USE travel_agency;")

# #基表
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     account VARCHAR(50) NOT NULL UNIQUE,
#     password VARCHAR(255) NOT NULL,
#     role TINYINT NOT NULL,  -- 1游客 2导游 3旅社 4文旅局
# );
# """)
#
# #游客
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS tourists (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     tourist_name VARCHAR(50),
#     phone VARCHAR(20),
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
# );
# """)
#
# #导游
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS guides (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     guide_name VARCHAR(50),
#     phone VARCHAR(20),
#     agency_id INT,
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
# );
# """)
#
# #旅社
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS travel_agencies (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     agency_name VARCHAR(100),
#     address VARCHAR(255),
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
# );
# """)
#
# #建文旅局
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS gov_admins (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     admin_name VARCHAR(100),
#     region VARCHAR(100),
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
# );
# """)
#
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS tourist_guide_relation (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     tourist_id INT NOT NULL,
#     guide_id INT NOT NULL,
#     interaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
#     comment TEXT,
#     FOREIGN KEY (tourist_id) REFERENCES tourists(id),
#     FOREIGN KEY (guide_id) REFERENCES guides(id)
# );
# """)



print("数据库和表创建成功")

cursor.close()
conn.close()

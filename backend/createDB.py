import pymysql


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='118211yao',
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

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS tourist_route (
# id INT AUTO_INCREMENT PRIMARY KEY,
#     tourist_id INT NOT NULL,
#     route_id INT NOT NULL,
#     signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     status ENUM('待确认', '已确认', '已取消') DEFAULT '待确认',
#     FOREIGN KEY (tourist_id) REFERENCES tourists(id) ON DELETE CASCADE,
#     FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE
# );
# """)
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS route_guides (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     route_id INT,
#     guide_id INT,
#     FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE,
#     FOREIGN KEY (guide_id) REFERENCES guides(id) ON DELETE CASCADE
# );
# """)
#
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS chat_rooms (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     route_id INT,
#     is_private BOOLEAN DEFAULT FALSE,
#     FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE
# );
# """)
#
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS messages (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     room_id INT,
#     sender_id INT,
#     content TEXT,
#     latitude FLOAT,
#     longitude FLOAT,
#     FOREIGN KEY (room_id) REFERENCES chat_rooms(id) ON DELETE CASCADE,
#     FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
# );
# """)

# 群组表：记录群名、创建者等信息
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_by_id INT NOT NULL,
    created_by_role TINYINT NOT NULL,  -- 1游客 2导游 3旅社 4文旅局
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

# 群成员表：记录群组和用户的对应关系
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_group_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    user_role TINYINT NOT NULL,  -- 同样是 1游客 2导游 等
    FOREIGN KEY (group_id) REFERENCES chat_groups(id) ON DELETE CASCADE
);
""")


print("数据库和表创建成功")

cursor.close()
conn.close()

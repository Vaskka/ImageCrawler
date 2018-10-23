set mysql_username = root
set mysql_password = password

pip3 install -i https://pypi.douban.com/simple scrapy
pip3 install -i https://pypi.douban.com/simple pillow

mysql -u%mysql_username% -p%mysql_password% -e 'CREATE DATABASE IF NOT EXISTS table_image DEFAULT CHARSET UTF8MB4 COLLATE utf8mb4_general_ci;'

mysql -u%mysql_username% -p%mysql_password% -e 'create table table_image (    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,    img_url VARCHAR(255) NOT NULL,    img_title VARCHAR(255) NOT NULL,    img_size VARCHAR(255) NOT NULL,    img_upload_time VARCHAR(255) NOT NULL,    img_file_path VARCHAR(255) NOT NULL,    img_base64 LONGTEXT NOT NULL );'

python main.py
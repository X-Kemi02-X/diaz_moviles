CREATE USER diaz_moviles_user WITH PASSWORD 'diaz_moviles_pass';
CREATE DATABASE diaz_moviles_db OWNER diaz_moviles_user;
GRANT ALL PRIVILEGES ON DATABASE diaz_moviles_db TO diaz_moviles_user;
\q
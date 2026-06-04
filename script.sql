CREATE DATABASE diaz_moviles;
CREATE USER diaz_user WITH PASSWORD 'diaz_pass';
ALTER ROLE diaz_user SET client_encoding TO 'utf8';
ALTER ROLE diaz_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE diaz_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE diaz_moviles TO diaz_user;

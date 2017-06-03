BEGIN;

CREATE TABLE autodelivery_user(
  mlid INT PRIMARY KEY NOT NULL,
  access_token VARCHAR NOT NULL,
  refresh_token VARCHAR NOT NULL
);

CREATE TABLE item(
  name VARCHAR NOT NULL,
  mluser INT NOT NULL,
  FOREIGN KEY (mluser) REFERENCES autodelivery_user (mlid),
  id SERIAL PRIMARY KEY
);

CREATE TABLE publication(
  mlid VARCHAR PRIMARY KEY NOT NULL,
  item INT NOT NULL,
  FOREIGN KEY (item) REFERENCES item (id)
);

CREATE TABLE stock(
  id SERIAL PRIMARY KEY,
  resource VARCHAR NOT NULL,
  item INT NOT NULL,
  FOREIGN KEY (item) REFERENCES item (id)
);

COMMIT;
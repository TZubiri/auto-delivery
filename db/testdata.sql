BEGIN;

INSERT INTO autodelivery_user VALUES
  (153845410,'APP_USR123244554545-343434','RFR_USR239829328938232-sds'),
  (1002,'APP_dfdsf3r34343','RFR_dfsfsf4fs4f4f4sf4s'),
  (1003,'APP_USR12354545-343434','RFR_U328938232-sds'),
  (1004,'APP_dfdsf3rfdsfsdf34343','RFR_dfsfs4f4f4sf4s');

INSERT INTO item (name,mluser) VALUES
  ('STEAM CARD 50$',153845410),
  ('STEAM CARD 25$',153845410),
  ('STEAM CARD 10$',153845410),
  ('APPLE GIFT CARD 100$',1002),
  ('APPLE GIFT CARD 50$',1002);

INSERT INTO publication(mlid,item) VALUES
  ('MLA123247997',1),
  ('MLA123247998',2),
  ('MLA123247999',3),
  ('MLA244888843',4);

INSERT INTO stock(resource,item) VALUES
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('67ac6e7bc6eecf',1),
  ('b32c42353f',1),
  ('67ac6e7bc6eecf',2),
  ('67ac6e7bc6eecf',2),
  ('67ac6e7bc6eecf',2),
  ('67ac6e7bc6eecf',2),
  ('67ac6e7bc6eecf',3),
  ('67ac6e7bc6eecf',3),
  ('67ac6e7bc6eecf',3),
  ('67ac6e7bc6eecf',2),
  ('67ac6e7bc6eecf',2),
  ('67ac6e7bc6eecf',4);

COMMIT;
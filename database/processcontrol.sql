INSERT INTO device 
VALUES 
('172.20.10.2:8080','Solar Panel Driver','4b8f1ddd0540ebd49a6b0ca7927e3534',1),
('192.168.0.228:8080','Solar Panel Driver','4b8f1ddd0540ebd49a6b0ca7927e3534',1),
('192.168.178.122:8080','Wind Turbine Driver','4b8f1ddd0540ebd49a6b0ca7927e3534',2),
('192.168.178.117:8080','Solar Panel Driver','4b8f1ddd0540ebd49a6b0ca7927e3534',2),
('192.168.178.62:8080','Solar Panel Driver','4b8f1ddd0540ebd49a6b0ca7927e3534',1);
INSERT INTO recipe 
VALUES
(1,'Adjust Solar Panel'), 
(2,'Adjust Wind Turbine');

INSERT INTO recipe_step (fk_recipe, fk_step)
VALUES
(1,0120),
(1,1120),
(1,2110),
(1,2220),
(2,0120),
(2,1120);

INSERT INTO step 
VALUES
(0120,'POST','/api/post/requestrecipe/'),
(1110,'GET' ,'/api/get/weatherinformation/all'), 
(1120,'POST','/api/post/weatherinformation/refresh'), 
(2110,'GET' ,'/api/get/sun/position'), 
(2220,'POST','/api/post/solarpanel/position');

INSERT INTO step_requestkey
VALUES
(1120,1), 
(2220,2),
(2220,3);

INSERT INTO requestkey
VALUES
(1,'Location'), 
(2,'Value1'),
(3,'Value2');

INSERT INTO step_responsekey
VALUES 
(1120,1),  
(2220,1);

INSERT INTO responsekey
VALUES
(1,'Status');

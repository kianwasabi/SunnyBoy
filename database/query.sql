INSERT INTO device VALUES 
(1,'Solar Panel Driver','4b8f1ddd0540ebd49a6b0ca7927e3534',1),
(2,'Wind Turbine Driver','4b8f1ddd0540ebd49a6b0ca7927e3534',2)
;
INSERT INTO recipe VALUES
(1,'Adjust Solar Panel'), 
(2,'Adjust Wind Turbine')
;
INSERT INTO step VALUES
(0120,'POST','/api/requestrecipe/'),
(1110,'GET','/api/get/weatherinformation/all'), 
(1120,'GET','/api/get/weatherinformation/refresh'), 
(2110,'GET','/api/get/sun/position'), 
(2220,'POST','/api/post/solarpanel/position')
;
INSERT INTO recipe_step (fk_recipe, fk_step)
VALUES
(1,0120),
(1,1120),
(1,2110),
(1,2220),
(2,0120),
(2,1120)
;

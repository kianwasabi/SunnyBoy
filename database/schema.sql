--DROP TABLE IF EXISTS user;
CREATE TABLE user(
  uid integer PRIMARY KEY, 
  username VARCHAR(15),
  apikey VARCHAR(32)
);

--DROP TABLE IF EXISTS weatherinformation;
CREATE TABLE weatherinformation(
  wid interger PRIMARY KEY, 
  locationname VARCHAR(32), 
  longitude VARCHAR(32),
  latitude VARCHAR(32), 
  location_time VARCHAR(32), 
  timezone VARCHAR(32), 
  azimuth VARCHAR(32),
  elevation VARCHAR(32),
  sunrise VARCHAR(32),
  sunset VARCHAR(32), 
  wind_speed VARCHAR(32),
  wind_direction VARCHAR(32),
  temperatur VARCHAR(32),
  cloudiness VARCHAR(32),
  weather_description VARCHAR(32), 
  visibility VARCHAR(32)
);

--DROP TABLE IF EXISTS panel;
CREATE TABLE panel(
  pid integer PRIMARY KEY, 
  val1 VARCHAR(32),
  val2 VARCHAR(32)
);

--DROP TABLE IF EXISTS requests;
CREATE TABLE requests (
  rid integer PRIMARY KEY,
  time_req TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
  uid integer, 
  pid integer,
  FOREIGN KEY (uid) REFERENCES user (uid),
  FOREIGN KEY (pid) REFERENCES weatherinformation (pid)
); 
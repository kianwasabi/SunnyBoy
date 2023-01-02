CREATE TABLE IF NOT EXISTS device(
  device_id           TEXT PRIMARY KEY,
  devicename          TEXT NOT NULL, 
  apikey              TEXT NOT NULL,
  fk_recipe_to_device INTEGER,
  FOREIGN KEY(fk_recipe_to_device) REFERENCES recipe(recipe_id)
);

CREATE TABLE IF NOT EXISTS recipe(
  recipe_id   INTEGER PRIMARY KEY,  
  description TEXT NOT NULL         
);

CREATE TABLE IF NOT EXISTS recipe_step(
  fk_recipe   INTEGER, 
  fk_step     INTEGER, 
  FOREIGN KEY (fk_recipe) REFERENCES recipe(recipe_id),
  FOREIGN KEY (fk_step)   REFERENCES step(step_id)--,
  --PRIMARY KEY (fk_recipe, fk_step)
);

CREATE TABLE IF NOT EXISTS step(
  step_id INTEGER PRIMARY KEY,       --Key in Header
  --domain  TEXT NOT NULL,             --URL:Domain   --currently in response header
  method  TEXT NOT NULL,             --URL:Method
  route   TEXT NOT NULL              --URL:Resource Path
);

CREATE TABLE IF NOT EXISTS step_requestkey(
  fk_step        INTEGER, 
  fk_requestkey  INTEGER, 
  FOREIGN KEY (fk_step)       REFERENCES step(step_id), 
  FOREIGN KEY (fk_requestkey) REFERENCES requestkey(requestkey_id)
);

CREATE TABLE IF NOT EXISTS step_responsekey(
  fk_step         INTEGER, 
  fk_responsekey  INTEGER, 
  FOREIGN KEY (fk_step)        REFERENCES step(step_id), 
  FOREIGN KEY (fk_responsekey) REFERENCES responsekey(responsekey_id)
);

CREATE TABLE IF NOT EXISTS requestkey(
  requestkey_id  INTEGER PRIMARY KEY,
  keytitle       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS responsekey(
  responsekey_id  INTEGER PRIMARY KEY,
  keytitle        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS weatherinformation(
  weather_id          INTEGER PRIMARY KEY, 
  locationname        TEXT NOT NULL,
  longitude           TEXT NOT NULL,
  latitude            TEXT NOT NULL, 
  location_time       TEXT NOT NULL, 
  timezone            TEXT NOT NULL, 
  azimuth             TEXT NOT NULL,
  elevation           TEXT NOT NULL,
  sunrise             TEXT NOT NULL,
  sunset              TEXT NOT NULL, 
  wind_speed          TEXT NOT NULL,
  wind_direction      TEXT NOT NULL,
  temperatur          TEXT NOT NULL,
  cloudiness          TEXT NOT NULL,
  weather_description TEXT NOT NULL, 
  visibility          TEXT NOT NULL, 
  created             TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task(
  task_id           INTEGER PRIMARY KEY, 
  discription       TEXT NOT NULL,
  fk_task_to_device INTEGER, 
  FOREIGN KEY (fk_task_to_device) REFERENCES device (device_id)
);

CREATE TABLE IF NOT EXISTS solarpanel(
  solarpanel_id   INTEGER PRIMARY KEY, 
  value1          INTEGER,
  value2          INTEGER, 
  adjusted        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS areacodes_zipcodes;
DROP TABLE IF EXISTS areacodes;
DROP TABLE IF EXISTS merchants;
DROP TABLE IF EXISTS receipts;
DROP TABLE IF EXISTS cities_zipcodes;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS zipcodes;


-- Broke out area codes to make search easier, if I decide to use it.
CREATE TABLE IF NOT EXISTS areacodes (
  id SERIAL PRIMARY KEY, -- Shouldn't need this, but forced to by  
                         -- save() in db.py.
  name VARCHAR(3) UNIQUE -- Forced to use VARCHAR by find_by_name() in db.py
  -- more to go here later, maybe
);

CREATE TABLE IF NOT EXISTS cities (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS zipcodes (
  id SERIAL PRIMARY KEY, -- Shouldn't need this, but forced to by  
                         -- save() in db.py.
  name VARCHAR(5) UNIQUE -- Forced to use VARCHAR by find_by_name() in db.py
  -- more to go here later, maybe
);

CREATE TABLE IF NOT EXISTS cities_zipcodes (
  id SERIAL PRIMARY KEY,
  city_id INT,
  zip_id INT,
  UNIQUE (city_id, zip_id),
  CONSTRAINT fk_city
      FOREIGN KEY (city_id) 
      REFERENCES cities(id)
      ON DELETE CASCADE,
  CONSTRAINT fk_zip
      FOREIGN KEY (zip_id) 
      REFERENCES zipcodes(id)
      ON DELETE CASCADE
);
-- Should name actually be unique? Made it unique to agree with cities
-- and zipcodes, and so find_by_name() will work in a consistent manner.
CREATE TABLE IF NOT EXISTS merchants (
  name VARCHAR(255) NOT NULL,
  cz_id INT,
  taxpayer_number INT,
  location_number INT,
  permit_number VARCHAR(16),
  address VARCHAR(256),
  latitudue FLOAT,
  longitude FLOAT,
  CONSTRAINT fk_city_zip
      FOREIGN KEY (cz_id) 
      REFERENCES cities_zipcodes(id)
      ON DELETE CASCADE
  CONSTRAINT pk_location_id
      PRIMARY KEY (taxpayer_number, location_number)
);

CREATE TABLE IF NOT EXISTS receipts (
  id SERIAL PRIMARY KEY,
  merchant_id INT,
  reporting_end_date datetime,
  liquor_sales INT,
  beer_sales INT,
  wine_sales INT,
  cover_sales INT,
  total_sales INT, 
  CONSTRAINT fk_merchant
      FOREIGN KEY (merchant_id) 
      REFERENCES merchants(pk_location_id)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS areacodes_zipcodes (
  id SERIAL PRIMARY KEY,
  area_id INT,
  zip_id INT,
  UNIQUE (area_id, zip_id),
  CONSTRAINT fk_areacode
      FOREIGN KEY (area_id) 
      REFERENCES areacodes(id)
      ON DELETE CASCADE,
  CONSTRAINT fk_zip
      FOREIGN KEY (zip_id) 
      REFERENCES zipcodes(id)
      ON DELETE CASCADE
);


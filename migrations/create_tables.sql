DROP TABLE IF EXISTS merchants;
DROP TABLE IF EXISTS receipts;
DROP TABLE IF EXISTS cities_zipcodes;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS zipcodes;


CREATE TABLE IF NOT EXISTS cities (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS zipcodes (
  id SERIAL PRIMARY KEY, -- Shouldn't need this, but forced to by
                         -- save() in db.py.
  name VARCHAR(5) UNIQUE, -- Forced to use VARCHAR by find_by_name() in db.py
  -- More to go here later, maybe, like population by male/female.
  population INT
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
  id SERIAL PRIMARY KEY,
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
      UNIQUE (taxpayer_number, location_number)
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

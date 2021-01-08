DROP TABLE IF EXISTS merchants;
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
  name VARCHAR(5) UNIQUE -- Forced to use VARCHAR by find_by_name() in db.py
  -- more to go here later, maybe
);

CREATE TABLE IF NOT EXISTS cities_zipcodes (
  id SERIAL PRIMARY KEY,
  city_id INT,
  zip_id INT,
  UNIQUE (city_id, zip_id),
  CONSTRAINT fk_city
      FOREIGN KEY(city_id) 
      REFERENCES cities(id)
      ON DELETE CASCADE,
  CONSTRAINT fk_zip
      FOREIGN KEY(zip_id) 
      REFERENCES zipcodes(id)
      ON DELETE CASCADE
);

-- Should name actually be unique? Made it unique to agree with cities
-- and zipcodes, and so find_by_name() will work in a consistent manner.
CREATE TABLE IF NOT EXISTS merchants (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  cz_id INT,
  liquor_sales INT,
  beer_sales INT,
  wine_sales INT,
  cover_sales INT,
  CONSTRAINT fk_city_zip
      FOREIGN KEY(cz_id) 
      REFERENCES cities_zipcodes(id)
      ON DELETE CASCADE
);

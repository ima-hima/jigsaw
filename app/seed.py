import psycopg2
from api.src.models import Areacode, City, Merchant, Zipcode, CityZipcode
import api.src.orm as orm


db.drop_all_tables(db.conn, db.cursor)

def build_city_zipcode(city_name='', zip_name=''):
    """Create data for testing of city and zipcode tables."""
    if city_name and zip_name:
        zipcode = db.find_or_create(Zipcode(name=zip_name), db.conn, db.cursor)[0]
        city = db.find_or_create(City(name=city_name), db.conn, db.cursor)[0]
        cross = db.find_or_create(CityZipcode(city_id=city.id, zip_id=zipcode.id), db.conn, db.cursor)
    return city, zipcode, cross

def build_merchant(merchant_name='', zipcode_name='', city_name=''):
    """Create data for testing of merchant table."""
    if city_name and zipcode_name and merchant_name:
        zipcode = db.find_or_create(Zipcode(name=zipcode_name), db.conn, db.cursor)[0]
        city = db.find_or_create(City(name=city_name), db.conn, db.cursor)[0]
        zipcode_city_cross = db.find_or_create(CityZipcode(city_id=city.id, zip_id=zipcode.id), db.conn, db.cursor)[0]
        merchant = db.find_or_create(Merchant(name=merchant_name, cz_id=zipcode_city_cross.id), db.conn, db.cursor)[0]
    return merchant

mn, mn_zip, mn_x_10001 = build_city_zipcode('Manhattan', '10001')
ps, ps_zip, ps_x_11220 = build_city_zipcode('Park_Slope', '11220')
bh, bh_zip, bh_x_11201 = build_city_zipcode('Brooklyn_Heights', '11201')
ch, ch_zip, ch_x_11201 = build_city_zipcode('Cobble_Hill', '11201')
cg, cg_zip, cg_x_11213 = build_city_zipcode('Carroll_Gardens', '11213')

brooklyn_ps, _, bk_x_ps = build_city_zipcode('Brooklyn', ps_zip.name)
brooklyn_bh, _, bk_x_bh = build_city_zipcode('Brooklyn', bh_zip.name)
brooklyn_cg, _, bk_x_cg = build_city_zipcode('Brooklyn', cg_zip.name)
brooklyn_ch, _, bk_x_ch = build_city_zipcode('Brooklyn', ch_zip.name)

frannies = build_merchant('frannies', mn_zip.name, mn.name)
chucks = build_merchant('chucks', bh_zip.name, bh.name)
charlies = build_merchant('charlies', ch_zip.name, ch.name)
fonzis = build_merchant('fonzis', cg_zip.name, cg.name)


# find_or_create(CityZipcode(city_id=brooklyn.id, zip_id=brooklyn.zipcode), db.conn, db.cursor)
# find_or_create(CityZipcode(city_id=brooklyn2.id, zip_id=brooklyn2.zipcode), db.conn, db.cursor)
# find_or_create(CityZipcode(city_id=brooklyn3.id, zip_id=brooklyn3.zipcode), db.conn, db.cursor)
# find_or_create(CityZipcode(city_id=brooklyn4.id, zip_id=brooklyn4.zipcode), db.conn, db.cursor)
# find_or_create(CityZipcode(city_id=manhattan.id, zip_id=manhattan.zipcode), db.conn, db.cursor)
# find_or_create(CityZipcode(city_id=park_slope.id, zip_id=park_slope.zipcode), db.conn, db.cursor)
# find_or_create(CityZipcode(city_id=brooklyn_heights.id, zip_id=brooklyn_heights.zipcode), db.conn, db.cursor)
# find_or_create(CityZipcode(city_id=cobble_hill.id, zip_id=cobble_hill.zipcode), db.conn, db.cursor)
# find_or_create(CityZipcode(city_id=carroll_gardens.id, zip_id=carroll_gardens.zipcode), db.conn, db.cursor)



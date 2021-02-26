import backend.src.db as db
import backend.src.models as models
import backend.src.orm as orm
import backend.src.adapters as adapters
import psycopg2



class Builder:
    def run(self, merchant_details, conn, cursor):
        cityzip = CityzipBuilder().run(merchant_details, conn, cursor)
        return MerchantBuilder().run(merchant_details, cityzip, conn, cursor)

class MerchantBuilder:
    attributes = ['name', 'liquor_sales', 'beer_sales', 'wine_sales', 'cover_sales', 'total_sales', 'cz_id']

    def select_attributes(self, merchant_details, cityzip):
        return dict(zip(self.attributes,
                        [merchant_details['location_name'],
                         merchant_details['liquor_receipts'],
                         merchant_details['beer_receipts'],
                         merchant_details['wine_receipts'],
                         merchant_details['cover_charge_receipts'],
                         merchant_details['total_receipts'],
                         cityzip.id,
                        ]
                       )
                    )

    def run(self, merchant_details, cityzip, conn, cursor):
        selected = self.select_attributes(merchant_details, cityzip)
        return orm.find_or_create(models.Merchant(**selected), conn, cursor)[0]

class CityzipBuilder:
    def run(self, merchant_details, conn, cursor):
        zipcode_name = merchant_details['location_zip']
        city_name = merchant_details['location_city']

        zipcode = orm.find_or_create(models.Zipcode(name=zipcode_name), conn, cursor)[0]
        city = orm.find_or_create(models.City(name=city_name), conn, cursor)[0]
        cityzip = orm.find_or_create(models.CityZipcode(city_id=city.id, zip_id=zipcode.id),
                                    conn,
                                    cursor)[0]
        return cityzip

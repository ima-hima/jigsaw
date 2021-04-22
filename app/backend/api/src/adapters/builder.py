# import backend.src.db as db
import backend.src.models as models
import backend.src.orm as orm
import backend.src.adapters as adapters
import psycopg2


class Builder:
    def run(self, merchant_details):
        cityzip = CityzipBuilder().run(merchant_details)
        merchant = MerchantBuilder().run(merchant_details, cityzip)
        return ReceiptBuilder().run(merchant_details, merchant)


class MerchantBuilder:
    attributes = ['name',
                  'address',
                  'permit_number',
                  'cz_id',
                  'latitude',
                  'longitude',
                  'taxpayer_id',
                  'location',
                  ]

    def select_attributes(self, merchant_details, cityzip):
        # get lat, long here.
        return dict(zip(self.attributes,
                        [merchant_details['location_name'],
                         merchant_details['location_address'],
                         merchant_details['tabc_permit_number'],
                         merchant_details['taxpayer_id'],
                         merchant_details['location'],
                         cityzip.id,
                         latitude,
                         longitude,
                         ]))

    def run(self, merchant_details, cityzip):
        selected = self.select_attributes(merchant_details, cityzip)
        return orm.find_or_create(models.Merchant(**selected))[0]


class ReceiptBuilder:
    attributes = ['reporting_end_date',
                  'liquor_sales',
                  'beer_sales',
                  'wine_sales',
                  'cover_sales',
                  'total_sales',
                  ]

    def select_attributes(self, merchant_details, merchant):
        return dict(zip(self.attributes,
                        [merchant_details['obligation_end_date_yyyymmdd'],
                         merchant_details['liquor_receipts'],
                         merchant_details['beer_receipts'],
                         merchant_details['wine_receipts'],
                         merchant_details['cover_charge_receipts'],
                         merchant_details['total_receipts'],
                         merchant.id,
                         ]))

    def run(self, receipt_details, merchant):
        selected = self.select_attributes(receipt_details, cityzip)
        return orm.find_or_create(models.Receipt(**selected))[0]


class CityzipBuilder:
    def run(self, merchant_details):
        zipcode_name = merchant_details['location_zip']
        city_name = merchant_details['location_city']

        zipcode = orm.find_or_create(models.Zipcode(name=zipcode_name))[0]
        city = orm.find_or_create(models.City(name=city_name))[0]
        cityzip = orm.find_or_create(models.CityZipcode(city_id=city.id,
                                                        zip_id=zipcode.id))[0]
        return cityzip


class LatLongBuilder:
    def run(self, merchant_details):
        pass

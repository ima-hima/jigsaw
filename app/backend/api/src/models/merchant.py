import api.src.orm as orm
import api.src.models as models

class Merchant(models.Table):
    __table__ = 'merchants'
    columns = ['id',
               'name',
               'cz_id',
               'liquor_sales',
               'beer_sales',
               'wine_sales',
               'cover_sales',
               'total_sales'
              ]

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}'
            setattr(self, key, kwargs[key])

    def city(self, cursor):
        """Return the city where this merchant is located."""
        query_str = ('SELECT c.* '
                       'FROM cities c '
                       'JOIN cities_zipcodes cz ON cz.city_id = c.id '
                      'WHERE cz.id = %s;'
                    )
        cursor.execute(query_str, (self.cz_id,))
        record = cursor.fetchone()
        return orm.build_from_record(models.City, record)


    def zipcode(self, cursor):
        """Return the city where this merchant is located."""
        query_str = ('SELECT z.* '
                       'FROM zipcodes z '
                       'JOIN cities_zipcodes cz ON cz.zip_id = z.id '
                      'WHERE cz.id = %s;'
                    )
        cursor.execute(query_str, (self.cz_id,))
        record = cursor.fetchone()
        return orm.build_from_record(models.Zipcode, record)

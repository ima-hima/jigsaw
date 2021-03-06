import api.src.orm as orm
import api.src.models as models

class Zipcode(models.Table):
    __table__ = 'zipcodes'
    columns = ['id', 'name']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
            setattr(self, key, kwargs[key])

    def cities(self, cursor):
        """Return all cities in this zip code."""
        query_str = ('SELECT c.* '
                       'FROM cities c '
                       'JOIN cities_zipcodes cz ON cz.city_id = c.id '
                      'WHERE cz.zip_id = %s;'
                    )
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return orm.build_from_records(models.City, records)

    def merchants(self, cursor):
        """Return all merchants in this zip code."""
        query_str = ('SELECT m.* '
                       'FROM merchants m '
                       'JOIN cities_zipcodes cz ON m.cz_id = cz.id '
                      'WHERE cz.zip_id = %s;'
                    )
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return orm.build_from_records(models.Merchant, records)

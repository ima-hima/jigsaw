import api.src.orm
import api.src.models as models

class Areacode(models.Table):
    __table__ = 'areacodes'
    columns = ['id', 'name']

    def __init__(self, **kwargs):
        Areacode.initialize_table(kwargs)

    def zipcodes(self, cursor):
        """Return all zip codes in this area code."""
        query_str = ('SELECT z.* '
                       'FROM zipcodes z '
                       'JOIN areacodes_zipcodes az ON az.zip_id = z.id '
                      'WHERE az.areacode_id = %s;'
                    )
        cursor.execute(query_str, (self.id,))
        records = cursor.fetchall()
        return orm.build_from_records(models.Zipcode, records)

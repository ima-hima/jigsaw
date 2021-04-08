import models


class AreacodeZipcode(models.Table):
    __table__ = 'areacodes_zipcodes'
    columns = ['id', 'area_id', 'zip_id']

    def __init__(self, **kwargs):
        AreacodeZipcode.initialize_table(kwargs)

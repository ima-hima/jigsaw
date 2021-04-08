class Table:

    def initialize_table(cls, **kwargs):
        """
        Set up one of some class in models. Called in __init__s in all
        model class definitions.
        """
        print('initialize', cls, type(cls), kwargs)
        for key in kwargs.keys():
            if key not in cls.columns:
                raise f'{key} not in {cls.columns}'
            setattr(cls, key, kwargs[key])

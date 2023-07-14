import pyhocon

__all__ = [
    'Country',
]


class Country:
    def __init__(
            self,
            iso_country: str,
    ):
        self.iso_country = iso_country
        self.conf = pyhocon.ConfigFactory.parse_file(f'./Lib/countries/{iso_country}.conf')

    def __repr__(self):
        return f"Country({self.iso_country})"



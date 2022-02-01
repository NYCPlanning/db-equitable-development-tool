from geosupport import Geosupport, GeosupportError
import pandas as pd
import usaddress

g = Geosupport()


class Geocoder:
    @classmethod
    def from_eviction_address(self, record) -> str:
        """Return latitude, longitude in degrees"""
        if pd.notnull(record.latitude) and pd.notnull(record.longitude):
            return record.latitude, record.longitude
        address = self.eviction_record_to_address(record)
        return self.geocode_address(address)

    def eviction_record_to_address(self, record) -> dict:
        """Using these docs as guide https://usaddress.readthedocs.io/en/latest/"""
        parsed = usaddress.parse(record.eviction_address)
        parsed = {k: v for v, k in parsed}
        rv = {}
        rv["address_num"] = parsed.get("AddressNumber", "")
        street_name_components = [
            parsed.get("StreetNamePreModifier"),
            parsed.get("StreetNamePreDirectional"),
            parsed.get("StreetNamePreType"),
            parsed.get("StreetName"),
            parsed.get("StreetNamePostModifier"),
            parsed.get("StreetNamePostDirectional"),
            parsed.get("StreetNamePostType"),
        ]
        rv["street_name"] = " ".join([s for s in street_name_components if s])
        rv["borough"] = record.borough
        rv["zip"] = record.eviction_postcode
        return rv

    def geocode_address(self, address: dict) -> str:
        """Requires docker"""
        try:
            geocoded = g["1"](
                street_name=address["street_name"],
                house_number=address["address_num"],
                borough=address["borough"],
                mode="extended",
            )
            return geocoded["PUMA Code"]
        except GeosupportError as e:
            geo = e.result
            return None

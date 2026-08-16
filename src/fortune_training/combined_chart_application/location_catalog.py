from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib.metadata import PackageNotFoundError, version

import geonamescache


LOCATION_CATALOG_SCHEMA = "ZIWEI-BAZI-LOCAL-LOCATION-CATALOG-R1"
LOCATION_CATALOG_ALGORITHM_ID = "OFFLINE-GEONAMES-PLUS-CALIBRATION-PRESETS-R1"
LOCATION_CATALOG_ALGORITHM_VERSION = "1.0.0"
GEONAMES_MIN_CITY_POPULATION = 5000


@dataclass(frozen=True)
class LocationRecord:
    selection_id: str
    birth_place: str
    display_name: str
    latitude: float
    longitude: float
    timezone_id: str
    source_kind: str
    source_version: str
    country_code: str = ""
    admin1_code: str = ""
    population: int = 0
    aliases: tuple[str, ...] = ()

    def json_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["aliases"] = list(self.aliases)
        return payload


# These are explicit local-app conveniences, not Time/Calendar truth.  They keep
# high-value calibration locations stable where a generic city centroid would
# otherwise change a true-solar-time test vector.
CALIBRATION_PRESETS: tuple[LocationRecord, ...] = (
    LocationRecord(
        selection_id="PRESET:BEIJING",
        birth_place="Beijing",
        display_name="Beijing / 北京 · calibration preset",
        latitude=39.9042,
        longitude=116.4074,
        timezone_id="Asia/Shanghai",
        source_kind="CALIBRATION_PRESET_R1",
        source_version="1.0.0",
        country_code="CN",
        aliases=("Beijing", "北京", "Peking"),
    ),
    LocationRecord(
        selection_id="PRESET:SHANGHAI",
        birth_place="Shanghai",
        display_name="Shanghai / 上海 · calibration preset",
        latitude=31.2304,
        longitude=121.4737,
        timezone_id="Asia/Shanghai",
        source_kind="CALIBRATION_PRESET_R1",
        source_version="1.0.0",
        country_code="CN",
        aliases=("Shanghai", "上海"),
    ),
    LocationRecord(
        selection_id="PRESET:GREENWICH_OBSERVATORY",
        birth_place="Greenwich",
        display_name="Greenwich Observatory / 格林尼治天文台 · calibration preset",
        latitude=51.4769,
        longitude=0.0,
        timezone_id="Europe/London",
        source_kind="CALIBRATION_PRESET_R1",
        source_version="1.0.0",
        country_code="GB",
        aliases=("Greenwich", "Greenwich Observatory", "格林尼治", "格林尼治天文台"),
    ),
    LocationRecord(
        selection_id="PRESET:NEW_YORK",
        birth_place="New York",
        display_name="New York / 纽约 · calibration preset",
        latitude=40.7128,
        longitude=-74.006,
        timezone_id="America/New_York",
        source_kind="CALIBRATION_PRESET_R1",
        source_version="1.0.0",
        country_code="US",
        aliases=("New York", "New York City", "NYC", "纽约", "紐約"),
    ),
    LocationRecord(
        selection_id="PRESET:APIA",
        birth_place="Apia",
        display_name="Apia / 阿皮亚 · calibration preset",
        latitude=-13.833333,
        longitude=-171.76666,
        timezone_id="Pacific/Apia",
        source_kind="CALIBRATION_PRESET_R1",
        source_version="1.0.0",
        country_code="WS",
        aliases=("Apia", "阿皮亚", "阿皮亞"),
    ),
    LocationRecord(
        selection_id="PRESET:LORD_HOWE_ISLAND",
        birth_place="Lord Howe Island",
        display_name="Lord Howe Island / 豪勋爵岛 · calibration preset",
        latitude=-31.5531,
        longitude=159.0839,
        timezone_id="Australia/Lord_Howe",
        source_kind="CALIBRATION_PRESET_R1",
        source_version="1.0.0",
        country_code="AU",
        aliases=("Lord Howe Island", "Lord Howe", "豪勋爵岛", "豪勳爵島"),
    ),
)


class OfflineLocationCatalog:
    """Offline city/preset lookup for local-app input assistance only.

    Returned coordinates and timezone IDs become explicit BirthInput fields.
    The catalog does not alter, infer, or collapse downstream civil-time versus
    physical-longitude semantics.
    """

    def __init__(self) -> None:
        self._geo = geonamescache.GeonamesCache(
            min_city_population=GEONAMES_MIN_CITY_POPULATION
        )
        self._presets = {row.selection_id: row for row in CALIBRATION_PRESETS}
        try:
            self._geonamescache_version = version("geonamescache")
        except PackageNotFoundError:
            self._geonamescache_version = getattr(geonamescache, "__version__", "UNKNOWN")

    @staticmethod
    def _normalized(value: str) -> str:
        return " ".join(value.casefold().split())

    @classmethod
    def _preset_matches(cls, row: LocationRecord, query: str) -> bool:
        needle = cls._normalized(query)
        haystacks = (row.birth_place, row.display_name, *row.aliases)
        return any(needle in cls._normalized(value) for value in haystacks)

    def _city_record(self, city: dict[str, object]) -> LocationRecord:
        geoname_id = str(city["geonameid"])
        name = str(city["name"])
        country = str(city.get("countrycode", ""))
        admin1 = str(city.get("admin1code", ""))
        timezone_id = str(city["timezone"])
        qualifiers = ", ".join(value for value in (admin1, country) if value)
        display = f"{name} · {qualifiers} · {timezone_id}" if qualifiers else f"{name} · {timezone_id}"
        aliases = tuple(str(value) for value in city.get("alternatenames", []) if value)
        return LocationRecord(
            selection_id=f"GEONAMES:{geoname_id}",
            birth_place=name,
            display_name=display,
            latitude=float(city["latitude"]),
            longitude=float(city["longitude"]),
            timezone_id=timezone_id,
            source_kind="GEONAMESCACHE_OFFLINE_R1",
            source_version=self._geonamescache_version,
            country_code=country,
            admin1_code=admin1,
            population=int(city.get("population", 0) or 0),
            aliases=aliases,
        )

    @classmethod
    def _rank(cls, row: LocationRecord, query: str) -> tuple[int, int, str, str]:
        needle = cls._normalized(query)
        canonical = cls._normalized(row.birth_place)
        aliases = tuple(cls._normalized(value) for value in row.aliases)
        if canonical == needle:
            quality = 0
        elif canonical.startswith(needle):
            quality = 1
        elif needle in aliases:
            quality = 2
        elif any(value.startswith(needle) for value in aliases):
            quality = 3
        else:
            quality = 4
        source_priority = 0 if row.source_kind == "CALIBRATION_PRESET_R1" else 1
        return (quality, source_priority, -row.population, row.display_name.casefold())

    def search(self, query: str, *, limit: int = 12) -> tuple[LocationRecord, ...]:
        query = query.strip()
        if not 1 <= limit <= 20:
            raise ValueError("location search limit must be in [1, 20]")
        if len(query) > 80:
            raise ValueError("location search query is too long")

        candidates: dict[str, LocationRecord] = {}
        if not query:
            for row in CALIBRATION_PRESETS:
                candidates[row.selection_id] = row
        else:
            for row in CALIBRATION_PRESETS:
                if self._preset_matches(row, query):
                    candidates[row.selection_id] = row

            # A one-character global scan is noisy and unnecessarily expensive;
            # one-character aliases can still match the explicit presets above.
            if len(query) >= 2:
                city_rows: dict[str, dict[str, object]] = {}
                for attribute in ("name", "alternatenames"):
                    for city in self._geo.search_cities(
                        query,
                        attribute=attribute,
                        case_sensitive=False,
                        contains_search=True,
                    ):
                        city_rows[str(city["geonameid"])] = city
                for city in city_rows.values():
                    row = self._city_record(city)
                    candidates.setdefault(row.selection_id, row)

        ordered = sorted(candidates.values(), key=lambda row: self._rank(row, query))
        return tuple(ordered[:limit])

    def get(self, selection_id: str) -> LocationRecord | None:
        selection_id = selection_id.strip()
        preset = self._presets.get(selection_id)
        if preset is not None:
            return preset
        if not selection_id.startswith("GEONAMES:"):
            return None
        geoname_id = selection_id.split(":", 1)[1]
        city = self._geo.get_cities().get(geoname_id)
        return None if city is None else self._city_record(city)

    def metadata(self) -> dict[str, object]:
        return {
            "schema": LOCATION_CATALOG_SCHEMA,
            "algorithm_id": LOCATION_CATALOG_ALGORITHM_ID,
            "algorithm_version": LOCATION_CATALOG_ALGORITHM_VERSION,
            "geonamescache_version": self._geonamescache_version,
            "minimum_city_population": GEONAMES_MIN_CITY_POPULATION,
            "network_access": False,
            "coordinate_semantics": "CITY_OR_PRESET_DEFAULT_ONLY_MANUAL_REFINEMENT_ALLOWED",
        }

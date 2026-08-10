import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from data.sheets import load_data
from data.cleaning import clean_data


# ------------------------------------
# Load EMS data
# ------------------------------------

df = clean_data(load_data())


# ------------------------------------
# Load existing cache
# ------------------------------------

CACHE_FILE = "cache/location_coordinates.csv"

try:
    cache_df = pd.read_csv(CACHE_FILE)

except FileNotFoundError:

    cache_df = pd.DataFrame(
        columns=[
            "Location",
            "Latitude",
            "Longitude"
        ]
    )


# ------------------------------------
# Find locations not yet geocoded
# ------------------------------------

existing_locations = set(
    cache_df["Location"]
)

new_locations = sorted(
    set(
        df["Call location"]
        .dropna()
        .astype(str)
        .str.strip()
    )
    - existing_locations
)

print(
    f"{len(new_locations)} new locations found."
)


# ------------------------------------
# Initialise geocoder
# ------------------------------------

geolocator = Nominatim(
    user_agent="ems_heatmap"
)

geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds=1
)


# ------------------------------------
# Geocode locations
# ------------------------------------

new_rows = []

for location in new_locations:

    print(f"Searching: {location}")

    result = geocode(
        location + ", Singapore"
    )

    if result:

        print(
            f"✓ {location} -> {result.address}"
        )

        new_rows.append({
            "Location": location,
            "Latitude": result.latitude,
            "Longitude": result.longitude
        })

    else:

        print(
            f"✗ Could not find: {location}"
        )


# ------------------------------------
# Save updated cache
# ------------------------------------

if new_rows:

    new_df = pd.DataFrame(
        new_rows
    )

    cache_df = pd.concat(
        [
            cache_df,
            new_df
        ],
        ignore_index=True
    )

    cache_df.to_csv(
        CACHE_FILE,
        index=False
    )

    print(
        f"Saved {len(new_rows)} new locations."
    )

else:

    print(
        "No new locations."
    )

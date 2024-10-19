from typing import List
from shapely.geometry import Point, shape
import geojson
from main_app.models import ServiceArea  # Import ServiceArea model
import json


# Function to check if a point is within any main_app area
def get_service_areas_by_location(
    lat: float, lng: float, service_areas: List[ServiceArea]
) -> List[dict]:
    """
    Given a latitude and longitude, return a list of main_app areas that include the point.
    """
    point = Point(lat, lng)  # Create a Point object

    result = []  # List to hold results
    for area in service_areas:

        area_shape = shape(geojson.loads(json.dumps(area.geojson)))
        if area_shape.contains(point):  # Check if point is within area
            result.append(
                {
                    "name": area.name,
                    "provider_name": area.provider.name,
                    "price": area.price,
                }
            )

    return result

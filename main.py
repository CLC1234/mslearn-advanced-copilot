import json
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


current_dir = dirname(abspath(__file__)) 
wellknown_path = join(current_dir, ".well-known")
historical_data = join(current_dir, "weather.json")

app = FastAPI()
app.mount("/.well-known", StaticFiles(directory=wellknown_path), name="static")


# load historical json data and serialize it:
with open(historical_data, "r") as f:
    data = json.load(f)

@app.get('/')
def root():
    """
    Allows to open the API documentation in the browser directly instead of
    requiring to open the /docs path.
    """
    return RedirectResponse(url='/docs', status_code=301)


@app.get('/countries')
def countries():
    return list(data.keys())


@app.get('/countries/{country}/{city}/{month}')
def monthly_average(country: str, city: str, month: str):
    return data[country][city][month]

@app.get('/countries/{country}/cities')
def get_cities(country: str) -> list[str]:
    """
    Retrieve the list of cities for a given country/region.

    Parameters:
    country (str): The name of the country or region.

    Returns:
    list[str]: A list of city names within the specified country.

    Raises:
    KeyError: If the country is not found in the dataset.

    Edge Cases:
    - If the country does not exist, a 404 error is returned.
    - If the country exists but has no cities, an empty list is returned.
    """
    try:
        return list(data[country].keys())
    except KeyError:
        # Return a 404 error if the country is not found
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Country '{country}' not found.")

# Generate the OpenAPI schema:
openapi_schema = app.openapi()
with open(join(wellknown_path, "openapi.json"), "w") as f:
    json.dump(openapi_schema, f)
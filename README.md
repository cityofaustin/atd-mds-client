# atd-mds-client
A Python utility to interact data endpoints compliant with the [Mobility Data Specification](https://github.com/openmobilityfoundation/mobility-data-specification/tree/master/provider), as designed by the Open Mobility Foundation.

This client was inspired by the [City of Santa Monica MDS Provider Client](https://github.com/CityofSantaMonica/mds-provider).

## Installation

Install the library:

```python
pip install atd-mds-client
```

Or the development branch:
```python
pip install atd-mds-client-dev
```

## Getting started

```python
# Import standard libraies:
import json
from datetime import datetime

# Import the MDS Library:
from mds import *

# Provider Configuration
provider_configuration = {
    # Authentication type: "OAuth", "Bearer", "Basic" or "Custom"
    "auth_type": "Bearer",
    # If you have a Bearer authentication, provide the token:
    "token": "secret_token_here",
    # Provide the URL endpoint of the provider:
    "mds_api_url": "https://mds.your-scooter-company.com/api/endpoint/v1",
    # (Optional) The Provider ID
    "provider_id": "mds_provider_id",
    # Any additional HTTP Headers:
    "headers": {
        "App-Version": "3.0.0"
    },
    # Any additional settings:
    "time_format": "unix",
    "delay": 1, # Delay in seconds per http request
    "max_attempts": 3, # Max attempts if the http request fails
    "paging": True, # Enable/Disable pagination
    "timeout": 10, # Maximum time allowed for an HTTP request in seconds
    "version": "0.3.0", # MDS Version: "0.2.0", "0.3.0" or "0.4.0" or remove for custom driver
}

# Builds a time-zone aware date time range
my_time = MDSTimeZone(
    date_time_now=datetime(2020, 1, 1, 20), # Either Now or any date as specified by datetime, becomes end_time
    offset=3600,             # Subtract 1 hour from date_time_now and becomes start_time
    time_zone="US/Central",  # US/Central
)

 # Initialize the MDS Client
mds_client = MDSClient(config=provider_configuration, provider="amazing scooters")

# Get trips
trips = mds_client.get_trips(
    # First the start time for the query
    start_time=my_time.get_time_start(
        utc=True, # Transforms local time into UTC
        unix=True # Transforms format from ISO into Unix Epoch time
    ),
    # Now the end time:
    end_time=my_time.get_time_end(
        utc=True, # Transforms local time into UTC
        unix=True # Transforms format from ISO into Unix Epoch time
    )
)

print(json.dumps(trips))
```

# CD/CI

We make use of CircleCI for our deployments, you can see the build script in the `.circleci` folder in this repo. The basic process consists of a couple steps:

1. Generate basic variables based on the current branch
2. Change the package name based on the current branch
3. Builds the package
4. Deploys with twine 

**In short, the only way to deploy a package is to change it's version number manually in `setup.py`.** If the changes were made in the master branch, the deployment will go into production, for the dev branch, a postfix will be added to the name of the package before it is deployed to pypi. 

# Development

We currently have two branches: master and dev. The master branch is used in production, our dev is meant for development and testing. 

### Dev & Master Postfix

For the dev branch, the build script will attach a post fix `"-dev"` to the package name specified in `setup.py`. For example, in the dev branch file `setup.py` we see the package name is `name="atd-mds-client"` and the current version was `0.0.X`, if you were to change the version number and commit to the dev branch, the deployment script will deploy to pypi as `atd-mds-client-dev` with the new version.

### Pull Requests & Local Development

Pull requests are ignored by the CD/CI pipeline, meaning they do not get built. If you need a package built for dev testing:

- Test your script locally
- Create a PR against the dev branch, make sure you change the version number in setup.py
- Merge your PR branch to the dev branch

How about local development?

At the moment, local development is open-ended. You may use any python mechanism or style when including source python packages in your development and local tests.

# Tests

Some minimal unit testing has been done for the mds library; however, the testing is not thorough and it was only implemented as a way to test basic functionality. 

For more instructions and documentation, please follow this link:
https://github.com/cityofaustin/atd-mds-client/blob/master/tests

# License

The package is distributed under the GPL 3.0 license.

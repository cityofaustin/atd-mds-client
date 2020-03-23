# Tests

The following unit tests have been implemented as a quick way to test functionality. The current platform of choice is `pytest` but you are welcome to use any other.

### Important

You will need a configuration file in your `tests/` directory, the file must be named `config.json` so the final path is `tests/config.json`. Feel free to look at the provided template below and adjust as necessary.

Once you have the file in the correct folder, you may proceed to running tests.

### Virtual Env
Also, you will want to check you have your venv loaded and running:

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install requests pytz pytest
```


# Running Tests

Once you have your configuration file set up, the only thing you need is to type:

To run all tests:
```
$ pytest -v
```

For specific tests:
```
$ pytest -v tests/test_mds_client_base.py
```

For more verbose tests:
```
$ pytest -vs tests/test_mds_client_base.py
```

# Sample `tests/config`

You may follow this pattern when configuring your mds endpoints:

```json
{
  "sample_co": {
    "auth_type": "Custom",
    "token": "NotARealToken_7b6b4af962a5c58facbe37860ab46bcf",
    "mds_api_url": "https://sample.com/trips",
    "headers": {
      "App-Version": "3.0.0"
    },
    "mds_param_override": {
      "start_time": "custom_start_time"
    },
    "time_format": "unix",
    "provider_id": "7b7243fc-ea90-465f-81a0-13cc66066ab7",
    "delay": 1,
    "max_attempts": 3,
    "paging": true,
    "timeout": 10,
    "version": "0.3.0"
  },
  "provider_a": {
    "auth_type": "Bearer",
    "token": "your_token_here",
    "mds_api_url": "https://mds.yourprovider.com/",
    "headers": {
      "App-Version": "3.0.0"
    },
    "time_format": "unix",
    "provider_id": "provider_uuid_here",
    "delay": 1,
    "max_attempts": 3,
    "paging": true,
    "timeout": 10,
    "version": "0.3.0"
  },
  "provider_b": {
    "auth_type": "OAuth",
    "token_url": "https://login.provider.com/oauth/v2/token",
    "auth_data": {
      "client_id": "client_id_here",
      "client_secret": "client_secret",
      "grant_type": "client_credentials",
      "scope": "emobility.mds"
    },
    "auth_token_res_key": "access_token",
    "paging": true,
    "provider_id": "provider_uuid_here",
    "time_format": "unix",
    "token": null,
    "mds_api_url": "https://api.provider.com/mds",
    "version": "0.3.0"
  },
  "provider_c": {
    "auth_type": "Basic",
    "auth_data": {
      "username": "provider_username",
      "password": "provider_password"
    },
    "mds_api_url": "https://api.provider.com/v1/mds",
    "time_format": "unix",
    "provider_id": "provider_uuid_here",
    "delay": 1,
    "max_attempts": 3,
    "paging": true,
    "version": "0.4.0"
  }
}
```
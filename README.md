# Admesh Python API library

[![PyPI version](https://img.shields.io/pypi/v/admesh-python.svg)](https://pypi.org/project/admesh-python/)

The Admesh Python library provides convenient access to the Admesh REST API from any Python 3.8+
application. The library includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Documentation

- **Complete Documentation**: [https://docs.useadmesh.com/](https://docs.useadmesh.com/) - Full SDK documentation and guides
- **API Reference**: The full API of this library can be found in [api.md](api.md)

## Installation

```sh
# install from PyPI
pip install admesh-python
```

## Getting an API Key

To use the AdMesh API, you'll need an API key:

1. Create an account at [https://useadmesh.com/agents](https://useadmesh.com/agents) if you don't have one
2. Once registered, you can obtain your API key from the dashboard
3. Use this API key in your application as shown in the examples below

## Usage

```python
import os
from admesh import Admesh

client = Admesh(
    api_key=os.environ.get("ADMESH_API_KEY"),  # This is the default and can be omitted
)

response = client.recommend.get_recommendations(
    query="Best CRM for remote teams",
    format="auto",
)
print(response.recommendation_id)
# Access recommendations
for rec in response.response.recommendations:
    print(f"Title: {rec.title}")
    print(f"Reason: {rec.reason}")
    print(f"Link: {rec.admesh_link}")
```

There are several ways to provide your API key:

1. **Direct parameter**: Pass it directly as shown above with the `api_key` parameter
2. **Environment variable**: Set the `ADMESH_API_KEY` environment variable
3. **Using dotenv (recommended)**: Use [python-dotenv](https://pypi.org/project/python-dotenv/) to load from a `.env` file:

```python
# Install python-dotenv: pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()  # Load API key from .env file

# Create a .env file with: ADMESH_API_KEY=your_api_key_here
client = Admesh()  # No need to specify api_key, it's loaded from environment
```

Using environment variables or dotenv is recommended to keep your API key secure and out of source control.

## Async usage

Simply import `AsyncAdmesh` instead of `Admesh` and use `await` with each API call:

```python
import os
import asyncio
from admesh import AsyncAdmesh

client = AsyncAdmesh(
    api_key=os.environ.get("ADMESH_API_KEY"),  # This is the default and can be omitted
)


async def main() -> None:
    response = await client.recommend.get_recommendations(
        query="Best CRM for remote teams",
        format="auto",
    )
    print(response.recommendation_id)
    # Access recommendations
    for rec in response.response.recommendations:
        print(f"Title: {rec.title}")
        print(f"Reason: {rec.reason}")
        print(f"Link: {rec.admesh_link}")


asyncio.run(main())
```

## Handling errors

When the library is unable to connect to the API (for example, due to network connection problems or a timeout), a subclass of `admesh.APIConnectionError` is raised.

When the API returns a non-success status code (that is, 4xx or 5xx
response), a subclass of `admesh.APIStatusError` is raised, containing `status_code` and `response` properties.

All errors inherit from `admesh.APIError`.

```python
import admesh
from admesh import Admesh

client = Admesh()

try:
    client.recommend.get_recommendations(
        query="Best CRM for remote teams",
        format="auto",
        # Set to False if you want to handle empty recommendations yourself
        raise_on_empty_recommendations=True,
    )
except admesh.NoRecommendationsError as e:
    print("No recommendations were found for your query")
    print(e.message)
    # Handle the case where no recommendations are available
    # For example, you might want to suggest alternative queries
except admesh.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except admesh.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except admesh.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as follows:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |
| N/A         | `NoRecommendationsError`   |

## Requirements

Python 3.8 or higher.

## Support

We are keen for your feedback; please open an [issue](https://www.github.com/GouniManikumar12/admesh-python/issues) with questions, bugs, or suggestions.

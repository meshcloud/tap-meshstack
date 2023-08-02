# tap-meshstack

`tap-meshstack` is a Singer tap for the [meshStack Cloud Foundation Platform](https://www.meshcloud.io/).

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

At this moment, the tap is only available via GitHub.
To install via `meltano.yml`, specify this repository via pip_url

```yaml
plugins:
  extractors:
  - name: tap-meshstack
    namespace: tap_meshstack
    pip_url: git+https://github.com/meshcloud/tap-meshstack
    executable: tap-meshstack
```

## Configuration

### Accepted Config Options

- `federation`: meshStack federation config
  - `api_url`: meshStack federation API URL
  - `auth`: authentication options, see [Authorization](#source-authentication-and-authorization)
    - `username`: basic auth username
    - `password`: basic auth password (plaintext)
- `kraken`: meshStack kraken config
  - `api_url`: meshStack kraken API URL
  - `auth`: authentication options, see [Authorization](#source-authentication-and-authorization)
    - `username`: basic auth username
    - `password`: basic auth password (plaintext)
- `cert_path`: path to a public SSL certificate used to verify connection to meshStack. Useful if you are running meshStack Enterprise with certificates signed by a non-public Certificate Authority

A full list of supported settings and capabilities for this tap is available by running:

```bash
tap-meshstack --about
```

### Source Authentication and Authorization

The tap supports meshStack API authentication with HTTP Basic auth. Please review the official meshStack API documentation
section on [API Authentication](https://docs.meshcloud.io/api#authentication) how you can configure the required access.

### meshObject Representation in Records

The tap transforms your [meshObject tags](https://docs.meshcloud.io/docs/meshstack.metadata-tags.html) to a generic
key-values representation that's suitable for ETL. This is required so that ETL pipelines that expect static record
schemas can more handle easily handle the dynamic schema nature of tags. 

> Note that meshObject tag schemas can also be different from object to object in the same collection.

Consider the following example to understand how the transformation works. The `meshWorkspace` has the following
JSON representation in the meshObject API:

```json
{
  "apiVersion": "v1",
  "kind": "meshWorkspace",
  "metadata": {
      "name": "customer",
      "createdOn": "2021-01-25T10:28:38Z"
  },
  "spec": {
      "displayName": "admin-customer",
      "tags": {
          "environment": ["dev", "prod"]
      }
  }
}
```

The tap transforms this object into the following record representation

```json
{
  "apiVersion": "v1",
  "kind": "meshWorkspace",
  "metadata": {
      "name": "customer",
      "createdOn": "2021-01-25T10:28:38Z"
  },
  "spec": {
      "displayName": "admin-customer",
      "tags": [{
        "key": "environment", "values": ["dev", "prod"]
      }]
  }
}
```

The tap also removes the meshObject `_links` property as this is seldomly useful in ETL usecases and takes up a lot of 
unnecessary data, requiring explicit configuration to remove from records.

## Usage

You can easily run `tap-meshstack` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-meshstack --version
tap-meshstack --help
tap-meshstack --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_meshstack/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-meshstack` CLI interface directly using `poetry run`:

```bash
poetry run tap-meshstack --help
```

### Testing with [Meltano](https://www.meltano.com)

For local development on the tap, specify an executable directly in `meltano.yml`

```yaml
executable: /path/to/tap-meshstack/.venv/bin/tap-meshstack
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.

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

- `api_url`: meshStack API URL
- `auth`: authentication options, see [Authorization](#source-authentication-and-authorization)
  - `username`: basic auth username
  - `password`: basic auth password (plaintext)
- `tag_schemas`: see [meshObject Tag Schemas](#meshobject-tag-schemas)

A full list of supported settings and capabilities for this tap is available by running:

```bash
tap-meshstack --about
```

### Source Authentication and Authorization

The tap supports meshStack API authentication with HTTP Basic auth. Please review the official meshStack API documentation
section on [API Authentication](https://docs.meshcloud.io/api#authentication) how you can configure the required access.

### meshObject Tag Schemas

The tap needs to understand your [meshObject tag](https://docs.meshcloud.io/docs/meshstack.metadata-tags.html) configuration
in order to emit correct the schemas and records into singer streams. You therefore have to supply a JSON schema
of supported tags for each meshObject type you wish to read a stream for. Here's an example:

```yaml
tag_schemas:
  meshProject:
    properties:
      environment:
        items:
          oneOf:
          - description: prod
            enum:
            - prod
          - description: dev
            enum:
            - dev
          type: string
        type: array
  meshPaymentMethod:
    properties:
      costCenterNumber:
        type: string
      department:
        type: string
```

> There's a helper script `tags.py` that can help you build a tag configuration from meshStack's _private_ API.
> Please contact us for help about this. We are considering options to improve this process in the future.

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

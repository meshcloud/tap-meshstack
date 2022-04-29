"""Stream type classes for tap-meshstack."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_meshstack.client import meshStackStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class ChargebackStatementsStream(meshStackStream):
    """ChagebackStatements meshObject stream"""
    name = "chargebackStatements"
    path = "/api/meshobjects/chargebackstatements"
    # primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "chargebackstatement.json"
    


"""Tests standard tap features using the built-in SDK tests library."""

import os
from multiprocessing import Process
from time import sleep

from flask import Flask
from flask import send_from_directory

from singer_sdk.testing import get_standard_tap_tests

from tap_meshstack.tap import TapMeshStack

SAMPLE_CONFIG = {
    "federation": {
        "auth": {
            "username" : "user",
            "password": "password"
        },
        "api_url": "http://localhost:8000"
    },
    "kraken": {
        "auth": {
            "username" : "user",
            "password": "password"
        },
        "api_url": "http://localhost:8091"
    },
    "tag_schemas": {}
}


def run_stub():
    stub = Flask(__name__)

    this_dir = os.path.dirname(os.path.realpath(__file__))
    stub_dir = this_dir + "/../../stub"
    
    @stub.route('/api/meshobjects/<path:path>')
    def send_report(path):
        return send_from_directory(f"{stub_dir}/meshobjects", f"{path}.json")

    stub.run(host='localhost', port=8000)

# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(
        TapMeshStack,
        config=SAMPLE_CONFIG
    )

    server = Process(target=run_stub)
    server.start()
    sleep(1) # this is absolutley unreliable, yet gets the job done
    
    for test in tests:
        test()

    server.terminate()
    server.join()
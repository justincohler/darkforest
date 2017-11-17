"""
A simple utility to read sensitive data from a local config file.

(NOT FOR PRODUCTION)

Author: Justin Cohler
Created: 11/17/2017
"""
import json

class Config:
    """Contains basic utility for retrieving sensitive data."""

    @staticmethod
    def get(key):
        """Return the configuration value for the given lookup key."""
        with open("config.json") as f:
            config = json.load(f)
        return config[key]

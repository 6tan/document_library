#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import json
from inspect import getframeinfo, currentframe
from pathlib import Path

from fastjsonschema import compile

filename = getframeinfo(currentframe()).filename
ROOT_PATH = Path(filename).resolve().parents[1].resolve()

SCHEMA_ROOT = f"file:{ROOT_PATH}/utils/"

CREATE_SCHEMA_DICT = {
    "title": "create Schema",
    "type": "object",
    "id": f"{SCHEMA_ROOT}",
    "additionalProperties": False,
    "properties": {
        "audioFileType": {
            "$ref": "utils_json_schema_definitions.json#/definitions/audioFileType",
        },
        "audioFileMetadata": {
        }
    },
    "allOf": [
        {
            "if": {
                "properties": {"audioFileType": {"const": "song"}}
            },
            "then": {
                "properties": {
                    "audioFileMetadata": {
                        "$ref": "utils_json_schema_definitions.json#/definitions/song"
                    }
                }
            }
        },
        {
            "if": {
                "properties": {"audioFileType": {"const": "podcast"}}
            },
            "then": {
                "properties": {
                    "audioFileMetadata": {
                        "$ref": "utils_json_schema_definitions.json#/definitions/podcast"
                    }
                }
            }
        },
        {
            "if": {
                "properties": {"audioFileType": {"const": "audiobook"}}
            },
            "then": {
                "properties": {
                    "audioFileMetadata": {
                        "$ref": "utils_json_schema_definitions.json#/definitions/audiobook"
                    }
                }
            }
        }
    ],
    "required": ["audioFileType", "audioFileMetadata"]
}
CREATE_SCHEMA_DICT_VALIDATOR = compile(CREATE_SCHEMA_DICT)

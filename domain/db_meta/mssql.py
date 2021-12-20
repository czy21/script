#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: ${{{file_path}}}' AS [file];",
    "footer": "SELECT 'executed: ${{{file_path}}}' AS [file];",
    "substitution": {
        "TrackedColumns": "id not null"
    }
}

#!/usr/bin/env python3

self = {
    "header": "SELECT 'executing: ${{{file_path}}}' AS [file];\ngo",
    "footer": "SELECT 'executed: ${{{file_path}}}' AS [file];\ngo",
    "substitution": {
        "TrackedColumns": "id not null"
    }
}

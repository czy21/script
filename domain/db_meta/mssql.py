#!/usr/bin/env python3

self = {
    "header": "SELECT 'Executing: ${{{file_path}}}' AS file;",
    "footer": "SELECT 'Executed: ${{{file_path}}}' AS file;",
    "substitution": {
        "TrackedColumns": "id not null"
    }
}

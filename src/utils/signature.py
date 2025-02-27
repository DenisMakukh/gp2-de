"""
Module Description:
This module performs XYZ functionality.

Author: Denis Makukh
Date: 27.02.2025
"""
import hashlib
import json
from typing import Dict, Any


def get_signature(params: Dict[str, Any], secret: str) -> str:
    stringified_params = {k: str(v) for k, v in params.items()}

    sorted_params = dict(sorted(stringified_params.items()))

    json_params = json.dumps(sorted_params, separators=(",", ":"), ensure_ascii=False)

    signature_data = json_params + secret
    return hashlib.sha256(signature_data.encode("utf-8")).hexdigest()

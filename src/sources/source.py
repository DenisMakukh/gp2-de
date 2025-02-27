"""
Module Description:
This module performs XYZ functionality.

Author: Denis Makukh
Date: 27.02.2025
"""
import logging
from typing import Optional, Dict, Any, Union

import httpx
import pandas as pd

log = logging.getLogger(__name__)


class Source:
    async def search(
            self
    ) -> pd.DataFrame:
        raise NotImplementedError

    async def make_request(
            self,
            method: str,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None,
            body: Optional[Dict[str, Any]] = None,
            timeout: float = 60.0
    ) -> Union[Dict[str, Any], str, bytes]:
        import httpx

        async with httpx.AsyncClient(http2=True, timeout=timeout) as client:
            log.info(f"Requesting {method} {url}")

            content_type = headers.get("content-type", "").lower() if headers else ""

            if "application/x-www-form-urlencoded" in content_type:
                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    data=body,
                    timeout=timeout
                )
            else:
                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=body,
                    timeout=timeout
                )

            response.raise_for_status()

            response_content_type = response.headers.get("Content-Type", "").lower()

            if "application/json" in response_content_type:
                return response.json()
            else:
                return response.text

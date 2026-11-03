"""
Matrix COSEC Biometric Device Communication Client
Interacts with Matrix COSEC Door / VEGA Terminals via CGI API endpoints.
"""

import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MatrixClient")


class MatrixCOSECClient:
    def __init__(self, ip: Optional[str] = None, port: Optional[int] = None, timeout: Optional[int] = None):
        self.ip = ip or Config.DEVICE_IP
        self.port = port or Config.DEVICE_PORT
        self.timeout = timeout or Config.TIMEOUT
        self.base_url = f"http://{self.ip}:{self.port}"
        self.submit_url = f"{self.base_url}/cgi-bin/submit"
        self.session_id = None

    def execute_query(self, query: str) -> Dict[str, Any]:
        """
        Sends raw text command to /cgi-bin/submit endpoint and parses JSON-like response.
        """
        if not query.endswith("?"):
            query += "?"

        req = urllib.request.Request(
            self.submit_url,
            data=query.encode("utf-8"),
            headers={"Content-Type": "text/plain", "User-Agent": "MatrixCOSECManager/1.0"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw_text = resp.read().decode("utf-8", errors="ignore").strip()
                return self._parse_matrix_response(raw_text)
        except urllib.error.URLError as e:
            logger.error(f"Connection failed to {self.submit_url}: {e}")
            return {"status": "error", "message": str(e)}

    def _parse_matrix_response(self, text: str) -> Dict[str, Any]:
        """
        Parses Matrix COSEC response formatted as:
        response-code=0 { "field":"value", ... }
        """
        result = {"raw": text, "response_code": None, "data": {}}
        if not text:
            return result

        # Extract response code
        if "response-code=" in text:
            parts = text.split("{", 1)
            code_part = parts[0].replace("response-code=", "").strip()
            result["response_code"] = code_part

            if len(parts) > 1:
                json_str = "{" + parts[1]
                # Matrix responses sometimes have trailing comma or empty key "":""
                try:
                    parsed = json.loads(json_str)
                    # clean up empty keys
                    parsed.pop("", None)
                    result["data"] = parsed
                except json.JSONDecodeError:
                    # fallback to basic key-value extraction
                    lines = json_str.replace("{", "").replace("}", "").split(",")
                    for line in lines:
                        if ":" in line:
                            k, v = line.split(":", 1)
                            clean_k = k.strip().strip('"').strip("'")
                            clean_v = v.strip().strip('"').strip("'")
                            if clean_k:
                                result["data"][clean_k] = clean_v
        return result

    def get_banner_info(self) -> Dict[str, Any]:
        """Fetches device banner info (Device Model, Name, Door ID)."""
        res = self.execute_query("GetBannerInfo?")
        return res.get("data", {})

    def get_login_params(self) -> Dict[str, Any]:
        """Fetches login requirements, password status, and device variant."""
        res = self.execute_query("getLoginPara?")
        return res.get("data", {})

    def get_encryption_keys(self) -> Dict[str, str]:
        """Fetches temporary AES Key and IV for secure authentication."""
        res = self.execute_query("GetKeyAndIV?")
        data = res.get("data", {})
        return {
            "key": data.get("KeyValue", ""),
            "iv": data.get("IvValue", "")
        }

    def check_connection(self) -> bool:
        """Verifies if the device HTTP server is accessible."""
        try:
            with urllib.request.urlopen(f"{self.base_url}/", timeout=self.timeout) as resp:
                return resp.status == 200
        except Exception:
            return False

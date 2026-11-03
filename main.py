"""
Matrix COSEC Manager CLI Entry Point
"""

import sys
import json
from config import Config
from matrix_client import MatrixCOSECClient


def main():
    print("=" * 60)
    print("   Matrix COSEC Biometric Device Manager")
    print("=" * 60)
    print(f"Target Device: {Config.DEVICE_IP}:{Config.DEVICE_PORT}")
    print()

    client = MatrixCOSECClient()

    print("[*] Testing HTTP connectivity...")
    if not client.check_connection():
        print(f"[!] Unable to connect to {Config.DEVICE_IP}. Please ensure:")
        print("    1. Ethernet cable is securely connected.")
        print("    2. Local interface IP is set on the matching subnet.")
        sys.exit(1)

    print("[+] Device responded successfully (HTTP 200 OK)!")
    print()

    print("[*] Fetching Device Banner Information...")
    banner = client.get_banner_info()
    if banner:
        print("    Device Model :", banner.get("bannerInfoField1", "Unknown"))
        print("    Device Name  :", banner.get("bannerInfoField2", "Unknown"))
        print("    Door Number  :", banner.get("bannerInfoField3", "Unknown"))
    else:
        print("    No banner data received.")

    print()
    print("[*] Fetching Login Parameters...")
    params = client.get_login_params()
    if params:
        print("    Device Code       :", params.get("cosecDeviceCode", "Unknown"))
        print("    Hardware Version  :", params.get("vegaHwVersion", "Unknown"))
        print("    Admin Pass Present:", bool(int(params.get("adminPswdSts", 0))))
    print()

    print("[*] Fetching Temporary Encryption Keys...")
    keys = client.get_encryption_keys()
    if keys.get("key"):
        print("    AES Key & IV negotiation verified.")
    print()

    print("=" * 60)
    print("   Device is fully online and ready for operations!")
    print("=" * 60)


if __name__ == "__main__":
    main()

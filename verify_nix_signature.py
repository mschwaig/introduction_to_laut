#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pynacl
"""
Nix binary cache signature verification.

This script verifies signatures from Nix binary cache .narinfo files.
"""

import base64
import nacl.signing
import nacl.exceptions


def main():
    # Values from the .narinfo file
    store_path = "/nix/store/wvfhs8k86740b7j3h1iss94z7cb0ggj1-hello-2.12.2"
    nar_hash = "sha256:1q27ixp15f8ggr11gjfgqql5s10iwv9gnh3hqgwdwrrxwk0kc0ii"
    nar_size = "274392"
    references = [
        "/nix/store/lmn7lwydprqibdkghw7wgcn21yhllz13-glibc-2.40-66",
        "/nix/store/wvfhs8k86740b7j3h1iss94z7cb0ggj1-hello-2.12.2"
    ]

    # Signature and public key
    signature_b64 = "qzsDAeq7dRyXpCyBtj4t+yZjaBFQcNf+Tp0XMVEm8/p1XS8GtA1cSYngx6fI07ib61ZNd0A8tWypIC0KxHs4AA=="
    public_key_b64 = "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=".split(":")[1]

    # Construct the fingerprint (format: "1;{store_path};{nar_hash};{nar_size};{references}")
    ref_string = ','.join(references)
    fingerprint = f"1;{store_path};{nar_hash};{nar_size};{ref_string}"
    print(f"Fingerprint: {fingerprint}")

    # Decode base64 values
    signature = base64.b64decode(signature_b64)
    public_key = base64.b64decode(public_key_b64)

    # Verify the signature
    try:
        verify_key = nacl.signing.VerifyKey(public_key)
        verify_key.verify(fingerprint.encode('utf-8'), signature)
        print("✓ Signature is valid!")
        return True
    except nacl.exceptions.BadSignatureError:
        print("✗ Signature verification failed!")
        return False


if __name__ == "__main__":
    main()

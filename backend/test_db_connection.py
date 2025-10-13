import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import dns.resolver

print("--- Starting Database Connection Test ---")

# Load environment variables from .env file
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    print("\n❌ FATAL: MONGO_URI not found in your .env file. Please check the file.")
else:
    print(f"\n1. Found MONGO_URI: {mongo_uri}\n")

    # --- Test 1: Basic DNS Lookup ---
    try:
        print("2. Testing DNS resolution for the cluster hostname...")
        # Extract hostname from URI, e.g., 'minuteme.lns8q3l.mongodb.net'
        hostname = mongo_uri.split('@')[1].split('/')[0]
        result = dns.resolver.resolve(hostname, 'A')
        print(f"   ✅ DNS lookup successful. Found IP addresses: {[ip.to_text() for ip in result]}")
    except Exception as e:
        print(f"   ❌ DNS lookup FAILED. This is the root cause of the problem.")
        print(f"      Error: {e}")
        print("      This suggests a firewall, antivirus, VPN, or network restriction is blocking the request.")
        print("--- Test Finished ---")
        exit() # Stop the test if DNS fails

    # --- Test 2: Attempting the actual connection ---
    try:
        print("\n3. Attempting to connect to MongoDB Atlas...")
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000 # Give it 5 seconds to connect
        )
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ping')
        print("\n✅✅✅ SUCCESS! Connection to MongoDB was successful. ✅✅✅")
        print("If this test succeeds but the app fails, the problem is environmental within the app's process.")

    except ConnectionFailure as e:
        print(f"\n❌❌❌ FAILURE! Could not connect to MongoDB.")
        print(f"   Error Details: {e}")
        print("\n   This confirms a network-level issue. Please check the following:")
        print("    - Is your IP address whitelisted in MongoDB Atlas? (Go to Network Access -> Add IP Address -> Allow Access From Anywhere)")
        print("    - Is a Firewall, Antivirus, or VPN blocking the connection?")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

print("\n--- Test Finished ---")
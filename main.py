import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

print("--- DEBUG INFORMATION ---")
print(f"URL exists: {bool(SUPABASE_URL)}")

if SUPABASE_URL:
    print(f"URL Value length: {len(SUPABASE_URL)}")
    print(f"URL Starts with: {SUPABASE_URL[:10]}")
    print(f"URL Rawrepr: {repr(SUPABASE_URL)}")
else:
    print("Error: SUPABASE_URL is completely None or empty!")

print(f"KEY exists: {bool(SUPABASE_KEY)}")
print("-------------------------")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL variable was not passed to Python script.")

from supabase import create_client, Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("Successfully connected to Supabase!")

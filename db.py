import os
import httpx
from postgrest import SyncPostgrestClient
from storage3 import SyncStorageClient
from gotrue import SyncGoTrueClient

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase environment variables")

# Manually create components
postgrest = SyncPostgrestClient(
    base_url=SUPABASE_URL + "/rest/v1",
    headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
)

storage = SyncStorageClient(
    base_url=SUPABASE_URL + "/storage/v1",
    headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
)

auth = SyncGoTrueClient({
    "url": SUPABASE_URL + "/auth/v1",
    "headers": {
        "apiKey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    },
    "auto_refresh_token": False,
    "persist_session": False
})

# Create a simple wrapper class
class SimpleSupabaseClient:
    def __init__(self):
        self.postgrest = postgrest
        self.storage = storage
        self.auth = auth
    
    def table(self, table_name):
        return self.postgrest.from_(table_name)
    
    def from_(self, table_name):
        return self.table(table_name)

supabase = SimpleSupabaseClient()

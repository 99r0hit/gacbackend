import os
from supabase import create_client
from dotenv import load_dotenv

# Load .env locally (Render ignores .env anyway)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not set")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY is not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


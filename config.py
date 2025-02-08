import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
ADMIN_SECRET = os.getenv("ADMIN_SECRET")  # Change this before production
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Your Supabase project URL
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Your RLS key
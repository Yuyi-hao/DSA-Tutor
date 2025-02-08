import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load environment variables from .env file
ADMIN_SECRET = os.getenv("ADMIN_SECRET")  # Change this before production
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Your Supabase project URL
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Your RLS key
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


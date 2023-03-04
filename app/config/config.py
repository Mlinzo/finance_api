from dotenv import load_dotenv
import os
import asyncio

def configure():
    load_dotenv()    
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

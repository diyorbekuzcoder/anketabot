import hashlib
import hmac
from urllib.parse import parse_qsl
import logging

def validate_telegram_data(init_data: str, bot_token: str) -> bool:
    if not init_data:
        return False
        
    try:
        parsed_data = dict(parse_qsl(init_data))
        if "hash" not in parsed_data:
            return False
            
        hash_val = parsed_data.pop("hash")
        
        # Sort keys alphabetically
        sorted_data = sorted(parsed_data.items(), key=lambda x: x[0])
        data_check_string = "\n".join([f"{k}={v}" for k, v in sorted_data])
        
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        return calculated_hash == hash_val
    except Exception as e:
        logging.error(f"Telegram data validation error: {e}")
        return False

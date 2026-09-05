import hashlib
import hmac
from urllib.parse import parse_qsl, urlencode

def validate_telegram_data(init_data: str, bot_token: str) -> bool:
    parsed_data = dict(parse_qsl(init_data))
    hash_val = parsed_data.pop('hash')
    sorted_data = sorted(parsed_data.items(), key=lambda x: x[0])
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted_data])
    secret_key = hmac.new(b'WebAppData', bot_token.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return calculated_hash == hash_val

bot_token = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
init_data_dict = {
    'query_id': 'AAH4j_8LAAAAAPiP_wsO1WkP',
    'user': '{"id":201192952,"first_name":"Dew","last_name":"","username":"dew","language_code":"en"}',
    'auth_date': '1700000000'
}
sorted_items = sorted(init_data_dict.items(), key=lambda x: x[0])
data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted_items])
secret_key = hmac.new(b'WebAppData', bot_token.encode(), hashlib.sha256).digest()
valid_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

mock_init_data = urlencode(init_data_dict) + f'&hash={valid_hash}'
print('Validation result:', validate_telegram_data(mock_init_data, bot_token))

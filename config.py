import os
import dotenv

dot_env_path = dotenv.find_dotenv()
dotenv.load_dotenv(dot_env_path)

guestoo = {
    'LOGIN_USER_NAME': os.getenv('LOGIN_USER_NAME'),
    'LOGIN_SECRET': os.getenv('LOGIN_SECRET'),
    'REFRESH_URI': os.getenv('REFRESH_URI'),
    'EVENT_ID': os.getenv('EVENT_ID'),
    'RELOGIN_HOURS': 10,
    'TOKEN_URL': "https://app.guestoo.de/auth/oauth/token",
    'GUESTS_URL': "https://app.guestoo.de/rest/guests",
    'DETAILED_GUESTS_URL': 'https://app.guestoo.de/rest/guests/search/withDetails'
}

import os
import dotenv

dot_env_path = dotenv.find_dotenv()
dotenv.load_dotenv(dot_env_path)

REFRESH_URI = os.getenv('REFRESH_URI')
guestoo = {
    'LOGIN_USER_NAME': os.getenv('LOGIN_USER_NAME'),
    'LOGIN_SECRET': os.getenv('LOGIN_SECRET'),
    'TOKEN_URL': "https://app.guestoo.de/auth/oauth/token",
    'GUESTS_URL': "https://app.guestoo.de/rest/guests",
    'DETAILED_GUESTS_URL': 'https://app.guestoo.de/rest/guests/search/withDetails',
    'EVENT_ID': os.getenv('EVENT_ID'),
}

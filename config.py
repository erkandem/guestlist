import os
import dotenv

dot_env_path = dotenv.find_dotenv(raise_error_if_not_found=True)
dotenv.load_dotenv(dot_env_path)
REFRESH_URI = '0023b4611f183619016bad427adfc667'
guestoo = {
    'LOGIN_USER_NAME': os.getenv('LOGIN_USER_NAME'),
    'LOGIN_SECRET': os.getenv('LOGIN_SECRET'),
    'TOKEN_URL': "https://app.guestoo.de/auth/oauth/token",
    'GUESTS_URL': "https://app.guestoo.de/rest/guests",
    'TOKEN': ''
}

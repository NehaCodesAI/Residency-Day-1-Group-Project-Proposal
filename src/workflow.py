import requests
import configparser

# Get token saved in .env
config = configparser.ConfigParser()
config.read("../.env")
TOKEN = config.get('CREATE_AI', 'API_KEY')

api_url = "https://api-main-beta.aiml.asu.edu/queryV2"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
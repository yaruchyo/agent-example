from dotenv import load_dotenv
from rotagent import DevTools

load_dotenv()
QUERY = "Find me 3 action movies"
ISSUER_ID = "dev_postman"
if __name__ == "__main__":
    DevTools.generate_bearer_token(QUERY, issuer_id=ISSUER_ID)

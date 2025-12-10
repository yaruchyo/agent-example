from rotagent import DevTools
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    DevTools.setup_persistent_keys(
        keys_dir="../../authorized_keys", issuer_id="dev_postman"
    )

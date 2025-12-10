from dotenv import load_dotenv
from rotagent import DevTools

load_dotenv()
if __name__ == "__main__":
    DevTools.setup_persistent_keys(
        keys_dir="../../authorized_keys", issuer_id="dev_postman"
    )

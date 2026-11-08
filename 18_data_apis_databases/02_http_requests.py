"""Module 18 · Calling web APIs with requests

  pip install requests

A web API is a URL that answers with data (usually JSON) instead of a web page.
The essentials of calling one safely:
  - always set a TIMEOUT (otherwise a dead server can hang your program forever)
  - check the STATUS code (raise_for_status)
  - pass query parameters with params=..., never by gluing strings together
  - catch requests.RequestException for network problems

TEACHING NOTES
  Why it matters  Your service will call other services; without timeouts and checks one slow
                  partner takes you down.
  Picture it      An API call is a letter with a form; the reply has a status code you must read
                  before the body.
  Watch out       Always set a timeout and call raise_for_status(); retry only idempotent calls.
  In real jobs    Payment, shipping, CRM and weather APIs; reuse a requests.Session.
  Interview       Q: How do you call an external API robustly?
                  A: Timeout, status check, retries with backoff on 429/5xx, a session for
                     pooling, logging.

Run it:  python 18_data_apis_databases/02_http_requests.py   (needs internet)
"""
import requests

API = "https://api.github.com"

# --- 1. A GET request with params, headers and a timeout -----------------------------------
try:
    resp = requests.get(
        f"{API}/search/repositories",
        params={"q": "language:python", "sort": "stars", "per_page": 3},   # -> ?q=...&sort=...
        headers={"Accept": "application/vnd.github+json"},
        timeout=10,
    )
    resp.raise_for_status()                       # 4xx/5xx -> raises HTTPError
    data = resp.json()                            # JSON text -> dict
    print(f"status {resp.status_code}, {data['total_count']:,} Python repos")
    for repo in data["items"]:
        print(f"  {repo['full_name']:<35} {repo['stargazers_count']:>8,} stars")

    # --- 2. Handle "not found" without crashing ---------------------------------------------
    missing = requests.get(f"{API}/repos/CodeMitVishal/does-not-exist", timeout=10)
    print("missing repo ->", missing.status_code)  # 404
    if missing.status_code == 404:
        print("  handled: show 'not found' to the user instead of crashing")

except requests.Timeout:
    print("The API took too long. Try again later.")
except requests.RequestException as e:            # no internet, DNS errors, HTTP errors...
    print(f"Network problem: {type(e).__name__}. Are you online?")

# --- 3. Sending data: POST with a JSON body (shown, not run) ----------------------------------
# resp = requests.post("https://api.example.com/orders",
#                      json={"item": "book", "qty": 2},       # serialised for you
#                      headers={"Authorization": f"Bearer {token}"},
#                      timeout=10)
# Keep tokens in environment variables (os.environ["API_TOKEN"]), never in code.

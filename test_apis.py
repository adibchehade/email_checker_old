import re
import time
import json
import random
import urllib
import urllib.request

from logger import log
from random_requests import get_random_session_request

APIS_FILE = 'data/api.txt'
APIS_FILE_OUTPUT = 'data/api_response_200.txt'

# Read URLs to check
urls_to_check = []
with open(APIS_FILE, 'r') as fp:
    urls_to_check = fp.read().splitlines()

# Get a random email
with open('data/emails.txt', 'r') as fp:
    emails = fp.read().splitlines()
email = emails[random.randint(0, len(emails))]

# # Read the headers file
# with open('data/parameters.txt', 'r') as fp:
#     params = fp.readlines()

# # Parse headers data
# param_sets = []
# param_set = []
# for param in params:
#     if param.strip() != '':
#         param_set.append(param)
#     else:
#         param_sets.append(param_set)
#         param_set = []

# # Get the first set only
# param_set = param_sets[0]

# # Get session id
# req = urllib.request.Request("https://www.westernunion.com/wuconnect/rest/api/v1.0/CreateSession?timestamp={}".format(str(int(time.time()*1000))))
# for param in param_set:
#     matches = re.match(r'.+\"(.+)\", \"(.+)\".+',param)
#     req.add_header(matches.group(1), matches.group(2))

#     try:
#         body = b"{\"device\":{\"id\":\"\",\"type\":\"WEB\"},\"channel\":{\"name\":\"Western Union\",\"type\":\"WEB\",\"version\":\"9Z00\",\"device_identifier\":\"RESPONSIVE_WEB\",\"is_responsive\":\"true\"},\"external_reference_no\":\"1\",\"locale\":{\"country_code\":\"us\",\"language_code\":\"en\"},\"security\":{\"black_box_data\":{\"data\":\"0400CIfeAe15Cx8Nf94lis1ztjXGwoPOvePAXyx2B+S3GHv4zk88XIRRraRLunIct8bff+0OYje9QG3QyfTeh05zWmOBOa6UBu99tJnG7aBZufFTM+276GxRfLnYpgrFwByeqHV8lCsVIFbWfvi2lw6riEVfH5Uu1Pa6eRLHB1R9v2d8MjlSDtQj+Jtpu4sEMnf8VWodMUtjVJMS2ITlncEvFXsdUywEcm1K+F9+VNHlcz2VwAGEd3H4L952RAUPKwCzLQAfZaA7jSiwHHrDW3HSYxnPse2ZJCsq4e3f1u/ETzp5VpgkQXTQzZ2bCkUkx/iDf2bn3Sw5z10y0BqqmpPWK5eIIfzGRmuyVIAW7uDQjXP1CYi+TBqr3g2vHHGOZYr7JaKI7U4dmdRZBrj3LMq6iXlL9ZZMAKELmgn6CSbaXfRSaQNEG0FLiAWeQwVS3/hrPOYe85lXFCRN2krK3MiK1aItlVfahFwAQkjj/Bf3sgBpWZmpMPu3J+3HIgrXK7aMtUplBKI7zAe5LqBNk4kdSgpA2sdPp297uf8vNtTCr7/8HBzsKudZ5X1CE/Fgu0JWx7yacWI+PSKq5dbmqXWqTFN9ILpoIeXbhWKXcVtbrPCixPMqjFULp9I8UWAJoym9T+HoQVdeZcQIrULZXTBjG6UIdAMpjc1v/zE8byqzj+BO44oNAQPdfLI+vS3zO1UWOjx45x9ZlwMJdmNWP4mnL4jqdQ4rX1XOyAfUMZ5LKFqFl81CC76WZKXakoCa7XCW4IhJrOz08Pzf+x4pw6W9esbGEpq7CoRYvFQ3SxgXyvTx/y4JwLTE4Nxv4KowoTq90t/25gxtwQokB0ojkm20iUzI+mPNi65X5WFPYlDG9N0Lbh5nOj3u3DXqRCiKCUrsEkMt8z9fxO9pLLGVQUKIYR2wTw53CiWK96FOpPevDWtH2XR0QkfOd02D73n81x6hEMCy0s3hRLn08Th9FlNHDMJBqLj+Tz8r0O/E9ABp/9e7Ass1MT2qnLUp3jXsoo0BtaQs3aTWzAj/ypZq/h+ZaTb+e2ERnQvcpeWgW0V2eQpdgS6+ebIBT9vO/g2GqbAcLd4t9XvVSBPuppttgqi/0yfOq1vG2COf7bsfFYzAaFLxVajijX/olA2vHHGOZYr7JaKI7U4dmdRZBrj3LMq6iXlL9ZZMAKELmgn6CSbaXfRSaQNEG0FLiAihm4Lf/K7HlU99UoH2xklR3N/aeGt5EB/svVUJi7EGUSnZsY8TL9w0j8/lZ9+74sNpkoqaTrmhoW0aLFYgm2YxWGZYhQabfSN8veAtIY6ioVg6fdSBnYKijDqHtCq29GqemMBz8q5Len0BJTgLAg0K0EGZNc9EzZa3c3jVldoE\",\"length\":1380},\"client_ip\":\"103082043065\"},\"bashPath\":\"/us/en\"}"
#         response = urllib.request.urlopen(req, body)
#         data = response.read()
#         if not data:
#             exit('Session id could not be created. Empty response from server. Exiting...')
#         session_id = json.loads(data.decode('utf-8'))['security']['session']['id']
#     except Exception as e:
#         log.info(e)
#         exit(1)

req, session_id = get_random_session_request()
log.info('session id created: {}'.format(session_id))

# Test the urls from APIS_FILE
urls_200 = []
for url in urls_to_check:
    req.full_url = '{}?timestamp={}'.format(url, str(int(time.time()*1000)))
    log.info(req.full_url)

    body = json.dumps({
        'email': email,
        'security': {'session': {'id': session_id},
        'version': '2'},
        'bashPath': '/us/en'
    }).encode()

    try:
        response = urllib.request.urlopen(req, body)
        # Save 200 response url to file
        with open(APIS_FILE_OUTPUT, 'a') as fp:
            fp.write(url)
    
    except urllib.error.HTTPError as e:
        log.info('{} {}'.format(e.code, e.reason))
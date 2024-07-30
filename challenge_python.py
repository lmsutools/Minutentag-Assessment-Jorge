"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
import boto3

def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}
    next_token = None
    if prefix:
        kwargs['Prefix'] = prefix

    while True:
        if next_token:
            kwargs['ContinuationToken'] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])
        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                yield obj
        next_token = resp.get('NextContinuationToken', None)
        if not next_token:
            break


"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""
def fn(main_plan, obj, extensions=[]):
    
    # Initialization
    # items: An empty list to store the final processed items.
    # sp: A boolean flag to check if the main plan item is found.
    # cd: A boolean flag to check if any item is marked as deleted.
    # ext_p: A dictionary to store extension prices and their quantities.
    items = []
    sp = False
    cd = False

    ext_p = {}

    # Iterates over each extension and populates the ext_p dictionary with the price ID as the key and the quantity as the value.
    for ext in extensions:
        ext_p[ext['price'].id] = ext['qty']

    # Iterates over each item in obj['items'].data.
    for item in obj['items'].data:
        product = {
            'id': item.id
        }

        # Checks if the item's price ID does not match the main plan's ID and is not in the extensions dictionary.
        if item.price.id != main_plan.id and item.price.id not in ext_p:
            product['deleted'] = True
            cd = True
        # Checks if the item's price ID is in the extensions dictionary
        elif item.price.id in ext_p:
            qty = ext_p[item.price.id]
            if qty < 1:
                product['deleted'] = True
            else:
                product['qty'] = qty
            del ext_p[item.price.id]
        # Checks if the item's price ID matches the main plan's ID.
        elif item.price.id == main_plan.id:
            sp = True

        # Appends the processed item to the items list.
        items.append(product)
    
    # Ensure Main Plan Item
    # Checks if the main plan item was not found in the previous iteration.
    # Appends the main plan item with a quantity of 1 to the items list.
    if not sp:
        items.append({
            'id': main_plan.id,
            'qty': 1
        })
    
    # Add Remaining Extensions
    # Iterates over any remaining items in the ext_p dictionary.
    for price, qty in ext_p.items():
        # Skips items with a quantity less than 1.
        if qty < 1:
            continue
        # Appends items with their respective quantities to the items list.
        items.append({
            'id': price,
            'qty': qty
        })
    # Return Final Items
    return items


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""
class Caller:
    add = lambda a, b: a + b
    concat = lambda a, b: f'{a},{b}'
    divide = lambda a, b: a / b
    multiply = lambda a, b: a * b

def fn(fn_to_call, *args): #Passes the arguments to the retrieved method
    #  Dynamically retrieves the method from the Caller class based on the string fn_to_call.
    return getattr(Caller, fn_to_call)(*args)


"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""
# Function categorizes the video based on its aspect ratio into one of three types: portrait, landscape, or standard.
def fn(config, w, h):
# config: A dictionary containing different encoding presets categorized into three keys:
# 'p': Presets for portrait videos.
# 'l': Presets for landscape videos.
# 's': Presets for standard aspect ratio videos.
# w: The width of the video.
# h: The height of the video.
    v = None
    # Calculates the aspect ratio of the video.
    ar = w / h

    # If the aspect ratio is less than 1, it indicates a portrait video (height is greater than width).
    if ar < 1:
        v = [r for r in config['p'] if r['width'] <= w]
    # If the aspect ratio is greater than 4/3, it indicates a landscape video (width is significantly greater than height).
    elif ar > 4 / 3:
        v = [r for r in config['l'] if r['width'] <= w]
    # If the aspect ratio is between 1 and 4/3, it indicates a standard aspect ratio video.
    else:
        v = [r for r in config['s'] if r['width'] <= w]
    # Returns the list of presets that match the video's aspect ratio category and width constraint.
    return v

"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""
import requests

class Helper:
    DOMAIN = 'http://example.com'
    SEARCH_IMAGES_ENDPOINT = 'search/images'
    GET_IMAGE_ENDPOINT = 'image'
    DOWNLOAD_IMAGE_ENDPOINT = 'downloads/images'

    AUTHORIZATION_TOKEN = {
        'access_token': None,
        'token_type': None,
        'expires_in': 0,
        'refresh_token': None
    }

    def _perform_request(self, method, endpoint, image_id=None, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']
        
        headers = {
            'Authorization': f'{token_type} {access_token}',
        }
        # constructs the URL based on the endpoint and optionally an image ID
        if image_id:
            URL = f'{self.DOMAIN}/{endpoint}/{image_id}'
        else:
            URL = f'{self.DOMAIN}/{endpoint}'

        send = {
            'headers': headers
        }

        if method == 'get':
            send['params'] = kwargs
            response = requests.get(URL, **send)
        elif method == 'post':
            send['data'] = kwargs
            response = requests.post(URL, **send)
        else:
            raise ValueError("Unsupported method")

        return response

    def search_images(self, **kwargs):
        return self._perform_request('get', self.SEARCH_IMAGES_ENDPOINT, **kwargs)
        
    def get_image(self, image_id, **kwargs):
        return self._perform_request('get', self.GET_IMAGE_ENDPOINT, image_id, **kwargs)

    def download_image(self, image_id, **kwargs):
        return self._perform_request('post', self.DOWNLOAD_IMAGE_ENDPOINT, image_id, **kwargs)

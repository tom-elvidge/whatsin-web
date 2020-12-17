import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import demjson
import datetime
import pprint
import boto3
import time

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

def get_bbcgf_recipe_urls():
    # Parse the sitemap.
    response = requests.get('https://www.bbcgoodfood.com/sitemap.xml', headers={'User-Agent':USER_AGENT})
    sitemap = ElementTree.fromstring(response.content)

    # Extract all recipe URLs from the sitemap.
    urls = []
    for item in sitemap:
        url = item[0].text

        if '/recipes/' not in url or '/' in url.split('/recipes/')[1]:
            # This url isn't for a recipe so we don't care.
            print('Ignoring URL {}'.format(url))
            continue

        lastmod = item[1].text
        urls.append((url, lastmod))

    return urls

def get_details_from_page(soup):
    script_tags = soup.find_all('script')
    for tag in script_tags:
        tag_str = str(tag)
        # Use the function definition because its at the start of the script and the variable names will be unique.
        if 'function(n,e,o,r,i)' in tag_str:
            # Remove everything from the script apart from the page details in the JavaScript object.
            js_obj = tag_str.split('permutive.addon("web",')[1][0:-23]
            # Use demjson since the page details are in a JavaScript object and not JSON.
            return demjson.decode(js_obj)
    return None

def get_ingredients_from_page(soup):
    # Find ingredients in page.
    ingredient_section = soup.find(id='recipe-ingredients')
    ingredient_groups = ingredient_section.find_all(
        'ul', class_='ingredients-list__group')
    # Add all ingredients to a list.
    ingredients = []
    for ingredient_group in ingredient_groups:
        for ingredient in ingredient_group.find_all('li'):
            ingredients.append(ingredient.get('content'))
    # Return ingredients.
    return ingredients

def get_method_from_page(soup):
    # Find method in page.
    method_section = soup.find('div', class_='method')
    method_items = method_section.find_all('li', class_='method__item')
    # Add all method steps to a list.
    method = []
    for item in method_items:
        method.append(item.getText())
    # Return method.
    return method


def build_initial_recipe(page_id, sitemap_ref, page_details, raw_ingredients, method):
    # Extract attributes from passed date sources.
    parse_datetime = str(datetime.datetime.now())
    bbcgf_update_date = sitemap_ref[1]
    title = page_details['page']['title']
    ingredients = page_details['page']['recipe']['ingredients']

    # Non-required fields so set as None and wrap each in a try catch in case they are missing.
    cooking_time = None
    prep_time = None
    serves = None
    rating_count = None
    nutrition_info = None
    try:
        cooking_time = page_details['page']['recipe']['cooking_time']
    except Exception as e:
        print('cooking_time missing:\n{}'.format(str(e)))
    try:
        prep_time = page_details['page']['recipe']['prep_time']
    except Exception as e:
        print('prep_time missing:\n{}'.format(str(e)))
    try:
        serves = page_details['page']['recipe']['serves']
    except Exception as e:
        print('serves missing:\n{}'.format(str(e)))
    try:
        rating_count = page_details['page']['recipe']['ratings']
    except Exception as e:
        print('ratings missing:\n{}'.format(str(e)))
    try:
        nutrition_info = page_details['page']['recipe']['nutrition_info']
    except Exception as e:
        print('nutrition_info missing:\n{}'.format(str(e)))

    # Return the final database item for this recipe.
    return {
        'id': page_id,
        'latest_parse_datetime': parse_datetime,
        'bbcgf_update_date': bbcgf_update_date,
        'parse_results': [
            {
                'title': title,
                'parse_datetime': parse_datetime,
                'cooking_time': cooking_time,
                'prep_time': prep_time,
                'serves': serves,
                'rating_count': rating_count,
                'nutrition_info': nutrition_info,
                'ingredients': ingredients,
                'raw_ingredients': raw_ingredients,
                'method': method
            }
        ]
    }


pp = pprint.PrettyPrinter(indent=4)

# Set up BBC Good Food DynamoDB table.
db = boto3.resource('dynamodb')
bbcgf_table = db.Table('BBCGF')

# Get all recipe URLS and their update date from the sitemap.
sitemap_items = get_bbcgf_recipe_urls()
# sitemap_items = [
#     ('https://www.bbcgoodfood.com/recipes/roast-loin-pork-sage-onion-stuffing-gravy', '2017-08-26'),
#     ('https://www.bbcgoodfood.com/recipes/fruit-nut-chocolate-chequers', '2013-06-18'),
#     ('https://www.bbcgoodfood.com/recipes/double-love-chocolate-cake', '2017-09-13'),
#     ('https://www.bbcgoodfood.com/recipes/crunchy-fish-goujons-skinny-chips', '2016-01-06'),
#     ('https://www.bbcgoodfood.com/recipes/roasted-tomato-cheddar-rice-garden-salad', '2015-11-25'),
#     ('https://www.bbcgoodfood.com/recipes/courgette-broccoli-gremolata-pasta', '2015-05-13'),
#     ('https://www.bbcgoodfood.com/recipes/peach-blueberry-grunt', '2018-08-04'),
#     ('https://www.bbcgoodfood.com/recipes/prawn-tacos', '2013-06-18'),
#     ('https://www.bbcgoodfood.com/recipes/basil-strawberry-pimms', '2016-09-30'),
#     ('https://www.bbcgoodfood.com/recipes/apple-scones-blackberry-compote', '2017-09-20'),
#     ('https://www.bbcgoodfood.com/recipes/crab-leek-pasties', '2013-06-18'), 
#     ('https://www.bbcgoodfood.com/recipes/chocolate-flapjacks', '2013-10-18'),
#     ('https://www.bbcgoodfood.com/recipes/376613/indische-hachee', '2020-02-02')
# ]

print('Starting...')

total = len(sitemap_items)
progress = 0

# Parse/scrape each recipe and add it to DynamoDB.
for sitemap_item in sitemap_items:
    progress += 1
    print('Percentage progress: {}.'.format((progress / total)*100))
    # Sleep so we don't send requests too quickly for BBC Good Food.
    time.sleep(0.5)

    page_id = sitemap_item[0].split('/')[-1]

    # Check if this page has already been scraped.
    response = bbcgf_table.get_item(
        Key= {
            'id': page_id
        }
    )
    if 'Item' in response:
        # It has been scraped then skip to next item.
        print('{} already exists in database.'.format(page_id))
        continue
    print('{} does not exist in database.'.format(page_id))

    # Request recipe page.
    print('Getting recipe page at {}'.format(sitemap_item[0]))
    response = requests.get(sitemap_item[0], headers={'User-Agent':USER_AGENT})
    print(str(response))

    try:
        # Get all info from page.
        print('Processing {}.'.format(page_id))
        soup = BeautifulSoup(response.content, 'html.parser')
        page_details = get_details_from_page(soup)
        method = get_method_from_page(soup)
        raw_ingredients = get_ingredients_from_page(soup)
        print('Finished processing {}.'.format(page_id))

        recipe = build_initial_recipe(page_id, sitemap_item, page_details, raw_ingredients, method)
        pp.pprint(recipe)

        print('Putting recipe in DynamoDB.')
        bbcgf_table.put_item(
            Item = recipe
        )
        print('Done.')
    except Exception as e:
        print('Something went wrong processing the recipe. Moving onto next.')
        print(str(e))
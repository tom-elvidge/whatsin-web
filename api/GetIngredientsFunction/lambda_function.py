import json
import mysql.connector
import numpy
import csv
import os

CORS_HEADERS = {
    'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT',
    'Access-Control-Allow-Origin': '*'
}

# Load the credentials.
with open('credentials.csv') as file:
    reader = csv.reader(file, delimiter=',')
    credentials = next(reader)

# Connect to mysql instance.
print('Setting up MySQL connection...')
db = mysql.connector.connect(
  host=credentials[0],
  port=int(credentials[1]),
  user=credentials[2],
  password=credentials[3],
  database=credentials[4]
)
print('Done.')


def lambda_handler(event, context):
    try:
        print('event:\n'+str(event))
        
        recipe_name = event['pathParameters']['recipe_name']
        recipe_name = recipe_name.replace('%20', ' ')
        recipe_name = recipe_name.replace('+', ' ')
        print('recipe_name: ' + recipe_name)
        
        # The recipe_name is allowed to contain alphabetic characters or spaces.
        # If it contains anything else raise an exception in case SQL injection.
        if not recipe_name.replace(' ', '').isalpha():
            raise Exception('recipe_name contains illegal characters.')

        # Replace spaces with the any character for SQL regex to get more results.
        query = '''
            SELECT ingredient
            FROM RecipeIngredients
            WHERE recipe_id IN (
                SELECT id FROM Recipes
                WHERE title LIKE \'%{}%\'
            );
        '''
        formatted_query = query.format(recipe_name.replace(' ', '%'))
        print('query:\n' + formatted_query)

        # Execute query.
        print('Executing SQL...')
        cursor = db.cursor(dictionary=True)
        cursor.execute(formatted_query)
        print('Done.')
        
        # Extract all ingredients from SQL query response.
        ingredients = []
        for m in cursor.fetchall():
            ingredients.append(m['ingredient'])
        print('Ingredients from SQL:\n' + str(ingredients))
    
        # Get the frequency of each ingredient.
        ingredient_frequencies = get_frequencies(ingredients)
        print('ingredient_frequencies:\n' + str(ingredient_frequencies))
        
        # Filter to get all the ingredients with a high relative frequency.
        generic_ingredients = filter_ingredients(ingredient_frequencies, 1.5)
        print('generic_ingredients:\n' + str(generic_ingredients))
        
        body = {
            'ingredients': generic_ingredients
        }
        
        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps(body)
        }
    except Exception:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': 'Something went wrong...'
        }


def get_frequencies(ingredients):
    '''
    Count the number of occurences of each word or phrase in the passed list of ingredients.
    
    Parameters:
        ingredients - list - A list of ingredients. Each ingredient may occur many times.
    
    Returns:
        dict - A dictionary mapping each unique ingredient in words to the number of occurences.
    '''
    frequency = {}

    # Update frequency for each word.
    for ingredient in ingredients:
        # Dictionary keys must be immutable, so wrap in tuple.
        if ingredient in frequency:
            frequency[ingredient] = frequency[ingredient] + 1
        else:
            frequency[ingredient] = 1

    return frequency


def filter_ingredients(frequencies, std_scale):
    '''
    Filter the ingredients in ingredient_frequencies to get only the frequent ingredients.
    
    The frequency must be greater than the median + (std * std_scale).
    
    Parameters:
        frequencies - dict - A mapping of ingredients to their frequencies.
        std_scale - float - Scale the standard deviation. The greater this is the stricter the filter.
    
    Returns:
        list - A list of the ingredients that passed the filter.
    '''
    # Calculate median and standard deviation of the ingredient frequencies.
    med = numpy.median(list(frequencies.values()))
    std = numpy.std(list(frequencies.values()))
     
    # Get all the ingredients which have a frequency greater than med + (std * std_scale)
    passed = []
    for ingredient in frequencies.keys():
        if frequencies[ingredient] > med + (std * std_scale):
            passed.append(ingredient)

    return passed
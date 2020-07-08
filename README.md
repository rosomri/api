# Surprise me!
- Surprise me! is a python API that retrieve one random surprising response in JSON format, according to the parameters passed by the client.
- The surprising response will be chosen from a closed optinal list of surprising responses types, each type has its own internal logic and conditions.
- Retrieve stats (total responses, distribution) about previous successful surprising responses in JSON format.

### Installation
----------
- Surprise me! requires [Python](https://www.python.org/downloads/) to run.

    **Open with enclosed VENV environment**
    - run the 'start_api.bat' , **or -**
    ```sh
    $ 'youpath'\venv\Scripts\activate
    $ 'yourpath'\api.py
    ```
    
    **Open without environment**
    - Surprise me! requires [Flask module](https://flask.palletsprojects.com/en/1.1.x/installation/) to run.
    ```sh
    $ pip install Flask
    ```
    - Install the api and start the server by double click 'api.py', **or -**
    ```sh
    $ 'yourpath'\api.py
    ```


### Usatage
--------
Retrieve a random surprising response in JSON format, according to the parameters passed by the client.
```
GET http://localhost:3000/api/surprise?name=Ryan%20Gosling&birth_year=1980
```
- Example response:
```
{
    "type": "chuck-norris-joke",
    "result": "A Chuck Norris divided against himself can still stand."
}
```

 Retrieve a previous successful surprising responses in JSON format
```
GET http://localhost:3000/api/stats
```
- Example response:
```
{
    "requests": 27,
    "distribution": [
        {
            "type": "chuck-norris-joke",
            "count": 12
        },
        {
            "type": "kanye-quote",
            "count": 9
        },
        {
            "type": "name-sum",
            "count": 6
        }
    ]
}
```

# GET /api/surprise
---------
Retrieve one random surprising response in JSON format, according to the parameters passed by the client.
### Query parameters:
________
**name** - string, user’s full name (e.g: ‘Harry Potter’), **required**
- **if doesnt contain name -** return a 400 status code with a ‘no name field provided’ message.
- **must be alfhabetic, else** - return a 400 status code with a ‘name must contain only alphabets’ message.

**birth_year** - number, user’s birth year (e.g: 1984), **required**
- **if doesnt contain birth_year -** return a 400 status code with a ‘no birth_year field provided’ message.
- **must be numeric, else** - return a 400 status code with a ‘ birth_year must contain only digits’ message.
- **must be must be in range 1900-2020, else** - return a 400 status code with a ‘ must be in range 1900-2020’ message.

**if more than one error occur -** all the error messages retrieve with a 400 status code


### Avaliable surprises
------------
**1. 	Chuck Norris Joke (chuck-norris-joke)**
If this type was chosen, return a random Chuck Norris joke as JSON format.
-could be retrieved only if the user’s birth year is 2000 or before.

**2. 	Kanye West Quote (kanye-quote)**
If this type was chosen, return a random Kanye West quote as JSON format.
-could be retrieved only if the user’s birth year is after 2000 and the user’s first
	name doesn’t start with ‘A’ or ‘Z’.


**3. 	User Name’s Sum (name-sum)**
If this type was chosen, convert the user’s name to numbers and return the sum. 
	Each letter converted to a number (‘A’ = 1, ‘B’ = 2, ‘C’ = 3 etc.).
	-could be retrieved only if the user’s first name doesn’t start with ‘Q’.

#### How a surprise chosen
●   **If one or more surprises shuold be retrieved** - retrieve randomaly one of them

●   **If an error occurs while the api is trying to get the selected surprise** - another avalible surprise retrieve.

●	**If no surprise response was selected** - return a 404 status code with a ‘No surprise for you!’ message.

#### Optinal surprises by name and birth_year (table)
**A** = first name letter is 'Q'
**B** = first name letter is 'A' or 'Z'
**C** = year of birth is 2000 or before
| A | B | C | optinal surprises |
| ------ | ------ |--------|-------|
| v | x | v | Chuck Norris Joke
| v | x | x | Kanye West Quote
| x | v | v | Chuck Norris Joke, User Name’s Sum
| x | v | x | User Name’s Sum
| x | x | v | Chuck Norris Joke, User Name’s Sum
| x | x | x | User Name’s Sum, Kanye West Quote

# GET /api/stats
------------------
Retrieve stats (total responses, distribution) about previous successful surprising responses in JSON format
● **If there are no previous successful calls to the /surprise route -** reteieve a JSON object with 0 requests and an empty array, as example -
```
 {"requests": 0, "distributions": []}
```
● **If there are previous successful calls to the /surprise route -** reteieve a JSON object with the number of successful requests and an array of distribution, as example -
```
{
    "requests": 15,
    "distribution": [
        {
            "type": "chuck-norris-joke",
            "count": 4
        },
        {
            "type": "kanye-quote",
            "count": 4
        },
        {
            "type": "name-sum",
            "count": 7
        }
    ]
}
```


# Credits
----------------------
[free REST API for random Kanye West quotes.](https://kanye.rest/)
[a free JSON API for hand curated Chuck Norris facts.](https://api.chucknorris.io/)

-------------------
**Thank you, wish you lot of Surprises!**


# NLP-AllRecipes

#### 1. Dependencies
In order to make sure that our code runs properly you will need to install all following python packages:
 - conda install dnspython
 - conda install pymongo
 - conda install tabulate
 - conda install beautifulsoup4
 - conda install requests
 - conda install selenium
 - conda install nltk
 - conda install pandas
 
#### 2. Running the Code
In order to run the code you will need to call the pipeline python script:
```python
python pipeline.py
```
Afterwards, the program will ask you for a recipe from www.allrecipes.com. Just copy the link to the recipe and paste it on the terminal. You do not necessarily need to copy the whole link, but make sure that the link contains the number after ```/recipe/```. An example for a recipe link would be ```https://www.allrecipes.com/recipe/220643/```! The program will then read the recipe and parse it into its internal representation. We are using HTTP requests and Beautiful Soup in order to scrape the recipe webpage. After we parsed the recipe into our internal representation we store the recipe ion our database for later usage. Additionally, we built a Slenium Scraper that is able to scrape hundreds of recipes in a given section like "Vegetarian", "Persian" or "Italian" recipes. These recipes will also be stored in our database for later usage. The mentioned representation consists of the following parts:
- Facts
    - Recipe Name
    - Recipe Tags
    - Nutrition Facts
    - Cooking Times
    - Servings Count
    - Main Cooking Action
- Ingredients
    - Quantity
    - Unit
    - Name
    - Descriptor
- Directions
    - Times
    - Temperatures
    - Cooking Actions
    - Ingredients
    - Tools
    
**INGREDIENTS:** In order to parse the ingredients into quantity, unit, name and descriptor we tried many different approaches. First, we found this https://github.com/nytimes/ingredient-phrase-tagger github repository built by the New York Times. They were using a crf++ model that was trained on 180k training phrases that were labeled by humans. Originally we took that model file and used it to parse the ingredients into the internal representation. However, since the project guidelines suggested to not use an external model but build your own model we tried to train our own model using the same training data. We achieved this by applying named entity recognition to the phrases. The problem with that approach was that we got a rather bad performance on the ingredient names itself. Nevertheless, for the conversions at the end of the project we needed a good internal representation of the ingredient names in ordre to be able to make replacements. Thus, we tried to improve the training data and the model itself so that it puts a higher focus on the ingredient name itself.

**DIRECTIONS:** A direction usually consists of an action and an ingredient. Additionally, a direction can also contain information like cooking temperature or time and which tools are required to fulfil that step. To get this kind of information we are using lists of all known tools, actions and ingredients that can be used to cook something. A simple string comparison helps us to identify everything within a direction phrase. To get the time and the temperature of the direction we built a regex that finds patterns that match how people express the cooking time or temperature.

#### 3. Conversions
Furthermore, the program will offer you some conversions which you can apply to that recipe. For instance, you can convert a non-vegetarian dish to a vegetarian dish. The program will offer you the following conversions:

1:   To Vegetarian  
2:   To Non-Vegetarian  
3:   To Healthy  
4:   To Unhealthy  
5:   To Indian  
6:   To German   
7:   To Chinese 

In order to make these conversions as complex as possible but also applicable to any kind of recipe we introduced special scripts. These scripts can either _REPLACE_, _ADD_ or _SCALE_ ingredients of the recipe. During the development time we were first thinking that we don't need a _SCALING_ feature that would allow you to scale the quantity of certain ingredients by a given factor. However, since we realized that such a functionality is really helpful for making a recipe healthier or unhealthier. You can find the described scripts in the ```converts``` directory of this repository. 

**REPLACE:** If you take a look at the ```ToIndian.txt``` file you can recognize that it consists of a _REPLACE_ section. This section contains replacement steps in each line. The ingredients on the left hand side of the ```>``` symbol will be replaced with the ingredients on the right hand side. Our code will randomly pick an ingredient from the right side and replace it with the ingredient on the left side. Since we found that this is a rather stupid approach we tried to split each replacement in small replacement steps that make sense. For example, if you want to replace a sweet and sour fruit you should also pick something that is sweet and sour on the right side.  To make these scripts even more powerful we introduced the concept of ingredient variables. An example for such a variable would be the %meats% variable in the ```ToIndian.txt``` file. The line ```%meats% > lamb, chicken, goat``` will replace any kind of meet with lamb, chicken or goat. Our program will fetch all meats from our MongoDB and replace that variable with a properly formatted string that matches all meats.

**ADD:** Some cuisines, dishes or conversions require the addition of ingredients. A perfect example for this would be the Indian cuisine. While we would be able to replace spices and herbs with Indian spices and herbs the cuisine requires us to add even more spices and herbs than other cuisines would usually use. Therefore, we built an _ADD_ instruction. This _ADD_ section can be found at the end of the ```ToIndian.txt``` file. Here we can spcify which ingredients should be added to the recipe. Moreover, we can define the quantity and the unit to be added to the recipe. The hardest part in that case was finding a proper place to add these ingredients within the directions. Therefore, we also need to specify to what actions the program can add the new ingredients. All in all, the line ```
coriander powder > season, mix > 0.5 > tablespoon``` means that the program should add a half tablespoon of coriander powder to a seasoning or mixing direction per serving.

**SCALE:** We realized that we need a scaling functionality for the conversion to healthy and to unhealthy. The _SCALE_ instruction allows you to scale everything that is on the left hand side by the factor on the right hand side of the ```>``` symbol. 

#### 4. Future Outlook
To show you how all of these components could be working together we want to give you a brief outlook. Although our converter is already able to convert recipes to the Indian, the German or the Chinese cuisine we want to expand that conversion to any kind of cuisine or cooking style. Here is where our Selenium Scraper comes in. Since we can scrape hundreds of recipes we can analyze the relation between each ingredient and why they are part of the recipe. We could build and train a machine learning model based on the scraping data and apply that model to any kind of recipe. The result of the model could be a new conversion script like we were already using. All in all, we think that we can use the semantic representation our program created to introduce statistical machine learning into the project. That would help us to make the program scalable and applicable to any kind of cuisine. While we were focusing on a "depth"-approach that tries to perfectly convert a recipe into a new recipe the future would be to increase the range of cuisines. Therefore, we think that our project was a full success!
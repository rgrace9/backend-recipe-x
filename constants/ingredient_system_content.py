ingredient_system_content =  '''
Based on the ingredient from the USER return the single ingredient that includes the category ID, the diets, and allergies associated with each ingredient. The diet list is the diets that the ingredient is banned from. The allergies list is the allergies in which the ingredient is banned from. Each ingredient returned should be in this shape:
ingredient
     {"name": "All-purpose flour", "category_id": 3, "restricted_diet_ids": [3, 4, 5, 11], "allergy_ids": [7]}

As each ingredient is added to the array, include in it the appropriate allergy, category and the restricted diet IDs. An ingredient can only be associated with one category but it can be associated with many diets and allergies. 
Do not include a trailing comma after the ingredient object.
Here are the categories and their ids
 id |    name
----+------------
  1 | vegetables
  2 | fruits
  3 | grains
  4 | dairy
  5 | proteins
  6 | fats
  7 | sweets
  8 | beverages
  9 | spices
 10 | condiments
 11 | other

These are the allergy names and their IDS
 id |   name
----+-----------
  1 | peanuts
  2 | tree nuts
  3 | milk
  4 | eggs
  5 | fish
  6 | shellfish
  7 | wheat
  8 | soy
  9 | sesame
 10 | corn
 11 | mustard
 12 | celery

These are the diet names and their IDs. Associate the ingredient with the diet if the ingredient is excluded for someone following the diet
 id |           name
----+---------------------------
  1 | vegan
  2 | vegetarian
  3 | paleo
  4 | ketogenic
  5 | gluten-free
  6 | low-carb
  7 | low-fat
  8 | mediterranean
  9 | pescatarian
 10 | dairy-free
 11 | whole30
 14 | autoimmune protocol (aip)
 15 | raw food


For each ingredient it must be associated with one category. It is optional that it is associated with diets and allergies, but if it is, it can be associated with many diets and allergies.

Return only the object and no other text
 {"name": "All-purpose flour", "category_id": 3, "restricted_diet_ids": [3, 4, 5, 11], "allergy_ids": [7]}

These are descriptions of each diet
Vegan: Excludes all animal products, including meat, dairy, eggs, and honey. It also avoids animal-derived substances. Excludes dairy products like milk, cheese, yogurt, and butter.

Vegetarian: Avoids meat, fish, and poultry. allows dairy and eggs. Includes dairy products like milk, egg, cheese, yogurt, and butter.

Paleo: Bans grains, legumes, processed foods, sugar, and most dairy. Focuses on what could have been hunted or gathered in the Paleolithic era. Excludes dairy products like milk, cheese, yogurt, and butter.

Ketogenic: Severely restricts carbohydrates to force the body into a state of ketosis, where it burns fat for energy. High in fat and moderate in protein, it limits grains, sugar, fruits, and tubers. It allows dairy to be consumed. Includes dairy products like milk, cheese, yogurt, and butter.

Gluten-Free: Eliminates all foods containing gluten, which is found in wheat, barley, rye, and derivatives. Aimed at those with celiac disease or gluten sensitivity.

Low-Carb: Reduces carbohydrate intake, focusing on protein and fat as primary sources of energy. Specific allowances vary, but it generally limits grains, sugar, and sometimes fruits and legumes.

Low-Fat: Restricts intake of fat, focusing on lean meats, grains, fruits, and vegetables. It often limits or avoids high-fat dairy, nuts, oils, and fatty meats.

Mediterranean: Not highly restrictive, but emphasizes fruits, vegetables, whole grains, olive oil, fish, and moderate wine consumption. Limits red meat, sugar, and saturated fats.

Pescatarian: Avoids meat and poultry but includes fish and seafood. May also include dairy and eggs, similar to a vegetarian diet but with fish.

Dairy-Free: Excludes dairy products like milk, cheese, yogurt, and butter. Often adopted by those with lactose intolerance or dairy allergies. Excludes dairy products like milk, cheese, yogurt, and butter.

Whole30: A diet that eliminates sugar, alcohol, grains, legumes, soy, and dairy. Focuses on whole foods, meats, nuts, and vegetables. Excludes dairy products like milk, cheese, yogurt, and butter. No dairy products. 

Autoimmune Protocol (AIP): A stricter version of the paleo diet designed to reduce inflammation and symptoms of autoimmune diseases. It excludes nightshades (like tomatoes, eggplants, white, red, and russet potato varieties, all peppers, curry powder, chili powder, cayenne powder, red pepper, tomatillos, paprika, pimento, goji berries, Ashwagandha), nuts, seeds, eggs, dairy, grains, and legumes, coffee, alcohol, beans. Excludes dairy products like milk, cheese, yogurt, and butter.

NOT NIGHT SHADES:
Black pepper is NOT a nightshade. Sweet potato is not a nightshade. Mushrooms are not nightshades. Onions are nightshades. Zucchini is not a nightshade.

Raw Food: Consists of uncooked, unprocessed plant foods. Typically, food is not heated above 115 degrees Fahrenheit to preserve enzymes and nutrients. Excludes animal products, processed foods, and anything cooked above 115 degrees fahrenheit. A dehydrator can be used to cook things. Excludes dairy products like milk, cheese, yogurt, and butter.


Allergy Descriptions and Example Ingredient Bans:
1. Peanuts:

Description: A severe allergy to peanuts can trigger a life-threatening reaction called anaphylaxis. Symptoms include hives, swelling, wheezing, trouble breathing, and nausea.
Banned Ingredients: Peanuts, peanut butter, peanut oil, hydrolyzed peanut protein, lecithin (if derived from peanuts).
2. Tree Nuts:

Description: This allergy encompasses various nuts like almonds, walnuts, cashews, pecans, hazelnuts, pistachios, and Brazil nuts. Reactions can be similar to peanut allergies, ranging from mild to severe.
Banned Ingredients: All tree nuts mentioned above, any nut butters or oils derived from them, and "may contain nuts" warnings.
3. Milk:

Description: Milk allergy involves a reaction to the proteins in cow's milk. Symptoms can include hives, nausea, vomiting, diarrhea, and wheezing.
Banned Ingredients: Cow's milk, cheese, yogurt, butter, cream, ice cream, whey, casein, lactose, and any products containing these ingredients.
4. Eggs:

Description: An egg allergy triggers a reaction to egg proteins found in both yolks and whites. Symptoms can range from mild skin reactions to anaphylaxis.
Banned Ingredients: Eggs, egg whites, egg yolks, ovum, lecithin (if derived from eggs), and any products containing these ingredients.
5. Fish:

Description: Fish allergy can involve different types of fish or even shellfish. Symptoms can include hives, swelling, wheezing, and anaphylaxis.
Banned Ingredients: All types of fish mentioned in the allergy (e.g., tuna, salmon, cod), fish oil, fish sauce, isinglass, and any products containing these ingredients.
6. Shellfish:

Description: Similar to fish allergies, reactions can occur to shrimp, crab, lobster, oysters, and other shellfish. Symptoms can range from mild to severe, including anaphylaxis.
Banned Ingredients: All types of shellfish mentioned in the allergy, shellfish broth, and any products containing these ingredients.
7. Wheat:

Description: Wheat allergy involves a reaction to gluten, a protein found in wheat, barley, and rye. Symptoms can include digestive issues, skin reactions, and anaphylaxis in severe cases.
Banned Ingredients: Wheat flour, spelt, durum, semolina, kamut, einkorn, barley, rye, and any products containing these ingredients.
8. Soy:

Description: Soy allergy triggers reactions to proteins in soybeans. Symptoms can range from mild skin irritation to anaphylaxis.
Banned Ingredients: Soybeans, soy milk, tofu, tempeh, edamame, miso paste, soy sauce, lecithin (if derived from soy), and any products containing these ingredients.
9. Sesame:

Description: Sesame allergy is becoming increasingly common and can cause severe reactions similar to peanut allergies. Symptoms can include hives, swelling, wheezing, and anaphylaxis.
Banned Ingredients: Sesame seeds, tahini, sesame oil, and any products containing these ingredients.
10. Corn:

Description: Corn allergy can involve reactions to the protein in corn kernels or corn syrup. Symptoms can range from mild skin reactions to anaphylaxis.
Banned Ingredients: Corn kernels, corn flour, cornstarch, corn syrup, high-fructose corn syrup, and any products containing these ingredients.
11. Mustard:

Description: Mustard allergy can cause mild to severe reactions, including hives, swelling, and anaphylaxis.
Banned Ingredients: Mustard seeds, mustard powder, Dijon mustard, yellow mustard, and any products containing these ingredients.
12. Celery:

Description: Celery allergy can trigger reactions similar to other food allergies, including skin reactions, swelling, and anaphylaxis.
Banned Ingredients: Celery seeds, celery root (celeriac), celery stalks, and any products containing these ingredients.


Dairy refers to foods derived from the milk of mammals, most commonly cows, goats, and sheep.
Common dairy products:

Milk (whole, skim, low-fat, etc.)
Cheese (hard, soft, aged, etc.)
Yogurt (plain, flavored, Greek, etc.)
Butter
Ice cream
Cream
Sour cream

Wheat is a cereal grain commonly used in breads, pastas, pastries, and other baked goods. It contains gluten, a protein that can be problematic for people with celiac disease or gluten sensitivity.
Common wheat products:

Bread (white, wheat, sourdough, etc.)
Pasta (wheat, whole wheat, semolina)
Cereals
Cookies
Cakes
Crackers
Pizza dough
Breaded foods
Bread crumbs

Grains are the seeds of grasses, including wheat, rice, barley, oats, corn, and quinoa. They are a good source of carbohydrates, fiber, and other nutrients.

Common grain products:

Rice (white, brown, basmati, etc.)
Barley
Oats
Quinoa
Corn
Couscous
Bulgur wheat
Popcorn


If an ingredient has 'category_id': 4, then it must have at least 'restricted_diet_ids': [1, 3, 10, 11, 14, 15], 'allergy_ids': [3] at the very least.



For every ingredient, include the category, diets, and allergies associated with it. If unsure, err on the side of including any possible allergies and diets the ingredient might be banned from. We would rather be overly cautious than not cautious enough.
If there are  no diets associated with the ingredient, return an empty array restricted_diet_ids: []
If there are no allergies associated with the ingredient, return an empty array allergy_ids: []
Always associate the ingredient with a category. If the category is unknown, associate it with the category "other" with the id 11.
'''
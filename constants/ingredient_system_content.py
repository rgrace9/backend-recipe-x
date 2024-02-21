ingredient_system_content =  '''
Based on the ingredient from the USER return the single ingredient that includes the category ID, the diets, and allergies associated with each ingredient. The diet list is the diets that the ingredient is banned from. The allergies list is the allergies in which the ingredient is banned from. Each ingredient returned should be in this shape:
ingredient
     {"name": "All-purpose flour", "category_id": 3, "restricted_diet_ids": [3, 4, 5, 11], "allergy_ids": [7]},

As each ingredient is added to the array, include in it the appropriate allergy, category and the restricted diet IDs. An ingredient can only be associated with one category but it can be associated with many diets and allergies. 

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
 12 | kosher
 13 | halal
 14 | autoimmune protocol (aip)
 15 | raw food


For each ingredient it must be associated with one category. It is optional that it is associated with diets and allergies, but if it is, it can be associated with many diets and allergies.

Return only the object and no other text
 {"name": "All-purpose flour", "category_id": 3, "restricted_diet_ids": [3, 4, 5, 11], "allergy_ids": [7]},

These are descriptions of each diet
Vegan: Excludes all animal products, including meat, dairy, eggs, and often honey. It also avoids animal-derived substances.

Vegetarian: Avoids meat, fish, and poultry. Some variations (like lacto-ovo vegetarians) allow dairy and eggs.

Paleo: Bans grains, legumes, processed foods, sugar, and most dairy. Focuses on what could have been hunted or gathered in the Paleolithic era.

Ketogenic: Severely restricts carbohydrates to force the body into a state of ketosis, where it burns fat for energy. High in fat and moderate in protein, it limits grains, sugar, fruits, and tubers.

Gluten-Free: Eliminates all foods containing gluten, which is found in wheat, barley, rye, and derivatives. Aimed at those with celiac disease or gluten sensitivity.

Low-Carb: Reduces carbohydrate intake, focusing on protein and fat as primary sources of energy. Specific allowances vary, but it generally limits grains, sugar, and sometimes fruits and legumes.

Low-Fat: Restricts intake of fat, focusing on lean meats, grains, fruits, and vegetables. It often limits or avoids high-fat dairy, nuts, oils, and fatty meats.

Mediterranean: Not highly restrictive, but emphasizes fruits, vegetables, whole grains, olive oil, fish, and moderate wine consumption. Limits red meat, sugar, and saturated fats.

Pescatarian: Avoids meat and poultry but includes fish and seafood. May also include dairy and eggs, similar to a vegetarian diet but with fish.

Dairy-Free: Excludes dairy products like milk, cheese, yogurt, and butter. Often adopted by those with lactose intolerance or dairy allergies.

Whole30: A 30-day diet that eliminates sugar, alcohol, grains, legumes, soy, and dairy. Focuses on whole foods, meats, nuts, and vegetables. It's meant to reset eating habits.

Kosher: Follows Jewish dietary laws, banning pork and shellfish, and requiring meat and dairy to be consumed separately. Meat must be slaughtered and prepared according to specific rules.

Halal: Adheres to Islamic law, prohibiting alcohol, pork, and any meats not slaughtered in the name of Allah. Halal foods must also be prepared with utensils that have not been contaminated with non-halal substances.

Autoimmune Protocol (AIP): A stricter version of the paleo diet designed to reduce inflammation and symptoms of autoimmune diseases. It excludes nightshades (like tomatoes, eggplants, white, red, and russet potato varieties, all peppers, curry powder, chili powder, cayenne powder, red pepper, tomatillos, paprika, pimento, goji berries, Ashwagandha), nuts, seeds, eggs, dairy, grains, and legumes, coffee, alcohol, beans. 

NOT NIGHT SHADES:
Black pepper is NOT a nightshade. Sweet potato is not a nightshade. Mushrooms are not nightshades. Onions are nightshades. Zucchini is not a nightshade.

Raw Food: Consists of uncooked, unprocessed plant foods. Typically, food is not heated above 118 degrees Fahrenheit to preserve enzymes and nutrients. Excludes animal products, processed foods, and anything cooked above 115 degrees fahrenheit. A dehydrator can be used to cook things.




'''
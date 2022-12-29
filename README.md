# Vkinder

Vkinder is a chat bot in vk.com for searching a couple using certain criteria.

## Description

The chat bot sends to user 3 most popular photos (with the largest number of likes and comments) of suitable candidate after the user answers certain questions about criteria for searching: 
*sex (1 - female, 2 - male)
*age from (minimum age)
*age to (maximum age)
*city

## Configurations
1. You can find installation dependencies in the file 'requirements.txt'
2. Before running any code you need to edit variables in the file 'configuration.py'. You can get your access token to vk.com at https://vkhost.github.io/
3. For running chat bot use 'bot.py'
4. File 'main.py' contains all methods for the bot to work.
5. File 'database.py' is used for saving results in database PostgresSQL. Also, the database is necessary to exclude repeated results.
6. File 'keyboard.py' includes settings for buttons 'Начать' and 'Далее' to make input easier for user. 

import asyncio
from ticle_scrapper import TicleScrapper
import mysql.connector

try:
    # Crie uma conexão com o banco de dados
    cnx = mysql.connector.connect(user='admin', password='#Mpn2012nicker',
                                  host='localhost',
                                  database='property-scrapper-schema')

    cursor = cnx.cursor()

    add_data = ("INSERT INTO properties "
                   "(name, value, description, link) "
                   "VALUES (%s, %s, %s, %s)")

    ticle_scrapper = TicleScrapper()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ticle_scrapper.find_elements_to_interact())
    result = loop.run_until_complete(ticle_scrapper.execute_scrapping())

    for r in result:
        data = (r.name, r.value, r.description, r.link)
        cursor.execute(add_data, data)

    cnx.commit()

except mysql.connector.Error as err:
    print(f"Something went wrong: {err}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'cnx' in locals():
        cnx.close()
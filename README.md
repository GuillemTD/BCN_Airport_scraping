# BCN_Airport_scraping
### Descripció
Aquest web scraper ha estat desenvolupat com a part de l'assignatura de Tipologia i cicle de vida de les dades del Màster en  Data Science de la Universitat Oberta de Catalunya. 

Mitjançant un script de Python extreu les dades de la web www.barcelona-airport.com i les emmagatzema en un arxiu .csv per a un posterior anàlisi.

Per a executar l'script cal tenir instal·lades les següents llibreries:
```
pip install bs4
pip install pandas
pip install os
pip install time
pip install request
```

L'script s'executa amb la següent comanda:
```
python BCN_Airport_scraping.py
```
**Nota:** Degut al gran nombre de requests que ha de dur a terme, la creació del dataset amb totes les dades pot tardar més de 20 minuts! Si no es desitja tota la informació es recomana usar el segon script
```
python BCN_Airport_scraping_limited.py
```

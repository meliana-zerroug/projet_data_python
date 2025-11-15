# Projet Data Python

## User Guide

Une section **User Guide** qui fournit les instructions pour déployer et utiliser votre dashboard sur une autre machine ;

Afin de déployer et utiliser le dashboard il faut, dans un premier temps, cloner le projet à partir de l'adresse "https://github.com/meliana-zerroug/projet_data_python.git", puis effectuer les différentes installations nécessaires grâce au fichier "requirements.txt" à l'aide de la commande `$ python -m pip install -r requirements.txt`. Ensuite on peut lancer le fichier "main.py" et on pourra visualiser le Dashboard sur "http://127.0.0.1:8050/". 


## Data

Une section **Data** qui renseigne sur les données utilisées ;

Nous avons utilisé deux sources de données différentes. La première que nous avons utilisée provient de "https://www.fao.org/faostat/fr/#data/FS" et représente différents indicateurs en rapport avec la nutrition dans le monde comme le nombre de personnes en sous-alimentation, le nombre de personnes obèses, et tout cela en fonction de l'année et du pays. Cette base de données renseigne également sur le PIB en fonction de l'année et du pays.

La deuxième source de données provient de "https://donnees.banquemondiale.org/indicateur/SP.POP.TOTL" et permet d'obtenir la population totale en fonction du pays et de l'année.  

## Developer Guide

Une section **Developer Guide** qui renseigne sur l'architecture du code et qui permet en particulier d'ajouter simplement une page ou un graphique ;

Le code est structuré en plusieurs parties. Dans la partie utils on peut retrouver le fichier get_data qui sert à récupérer les données de nos deux sources de données différentes. Nous avons également le fichier clean_data qui permet de nettoyer les données récupérées par get_data. 

Les différents composants sont dans le dossier components. Nous avons créé un fichier python par composant. Ainsi dans ce fichier on retrouve la structure globale ainsi que le style du composant. Afin d'ajouter ces composants au Dashboard il suffit d'importer les fonctions nécessaires dans le fichier home.py, puis de les mettre dans le layout principal. Le fichier home.py comporte le style général de notre Dashboard ainsi que le code nécessaire qui permet de mettre à jour certains composants en fonction d'un filtre (par année et par indicateur). 

Plus précisément, voici comment ajouter un nouveau composant : 

1. Créer un fichier dans `src/components/`, par exemple `mon_graphique.py`
2. Définir une fonction qui retourne le composant Dash
3. Importer la fonction dans `src/pages/home.py`
4. Ajouter le composant dans le layout
5. Si besoin d'interactivité notamment avec le filtre, créer un callback avec `@app.callback`

Si l'on souhaite ajouter une autre page, il suffit de créer le fichier de la page dans le dossier pages. Ensuite, on définit le layout de la page avec une fonction qui retourne la structure HTML/Dash, un peu comme dans la page home.py. On peut ensuite enregistrer la page dans main.py avec app.layout ou le routage Dash. 

## Rapport d'analyse

Une section **Rapport d'analyse** qui met en avant les principales conclusions extraites des données ;

L’objectif de ce projet est d’analyser l’évolution de l’insécurité alimentaire dans le monde entre 2000 et 2023.

1. Évolution de l’obésité dans le monde

L’analyse montre que lorsque l’on parcourt les différentes années de 2000 à 2022, on remarque que la population obèse dans le monde est majoritairement représentée par les États-Unis, avec un chiffre qui augmente au fil du temps. La Chine suit les États-Unis, mais avec un nombre largement inférieur.

Lorsque l’on observe la courbe de tendance, cela se confirme, plus les années passent, plus le nombre de personnes obèses augmente de façon plutôt linéaire. En 2000, on compte environ 336,3 millions de personnes, tandis qu’en 2022, on dépasse les 894,9 millions de personnes obèses.

2. Sous-nutrition : évolution dans le monde

En ce qui concerne la sous-nutrition, lorsque l’on analyse la même période, on remarque que cette population est majoritairement représentée par l’Inde, avec plus de 172,1 millions de personnes en 2023. Entre 2001 et 2009, la Chine arrive en deuxième position avec plus de 39,8 millions de personnes sous-nourries. La Chine a su faire face à cette problématique, puisqu’elle ne réapparaît plus dans les années suivantes parmi les pays comptant le plus de personnes sous-nourries.

Au niveau mondial, la courbe de tendance montre que le nombre de personnes sous-nourries est très élevé en 2001 (> 915,5 millions). Il diminue progressivement jusqu’en 2012 (environ 537,1 millions), où il se stabilise. À partir de 2019, il recommence à augmenter jusqu’à atteindre 627,5 millions en 2023.

3. Relation entre PIB et sécurité alimentaire 

Nous avons voulu également étudier si le PIB avait un impact sur la nutrition dans le monde. L'histogramme ainsi que le graphique filled_area permettent de visualiser comment le niveau économique d'un pays va influencer la nutrition de sa population. 

En prenant l'année la plus récente que nous possédons (2022), on remarque qu'il y a une relation réelle entre le niveau de PIB et la nutrition des populations. Les pays ayant un PIB plus faible, notamment en dessous de 10000$ par personne, concentrent la grande majorité des personnes sous-nourries avec un pic de 221,60 millions de personnes pour la tranche avec un PIB de 7500$ à 10000$ par personne. On remarque que plus le PIB augmente et plus la sous-nutrition diminue fortement et devient presque inexistante dans les pays les plus riches. 

À l'inverse, l'obésité augmente progressivement avec le PIB. Dans les pays à PIB plus élevé, on remarque que plus le PIB augmente et plus le nombre de personnes obèses est important. 

Nous avons également étudié les années précédentes, et on remarque qu'avant 2018, le pic pour le nombre de personnes en sous-nutrition était atteint pour un PIB plus faible (5000 à 7500$) par rapport aux périodes plus récentes. 
 

## Conclusion et perspectives 

L'analyse permet donc de montrer une augmentation constante du nombre de personnes obèses dans le monde, principalement dans les pays développés comme les États-Unis. Cela peut être causé par plusieurs facteurs, comme l'urbanisation, la hausse de la sédentarité ou encore la forte disponibilité d'aliments ultra-transformés. 

En revanche, la sous-nutrition diminue progressivement jusqu'en 2012 avant de remonter à partir de 2019. Différents facteurs pourraient expliquer cela, comme la pandémie de COVID-19, les conflits géopolitiques ou encore la hausse des prix alimentaires. L'Inde reste le pays le plus touché lorsque l'on s'intéresse aux périodes récentes. 

Pour aller plus loin, on pourrait intégrer d'autres indicateurs socio-économiques comme l'éducation. Afin d'améliorer le Dashboard, on pourrait également ajouter des filtres plus avancés pour filtrer par tranches d'âge ou par continent. On pourrait aussi ajouter des indicateurs sur le taux de pauvreté dans le monde afin de mieux comprendre les liens entre nutrition et niveau économique. 

## Copyright

Une section **Copyright** qui atteste de l'originalité du code fourni.

- Nous déclarons sur l'honneur que le code fourni a été produit par nous-même.

# Bot Telegram « Photo Pro » (public)

Le bot reçoit une photo de produit. Il la rend plus lumineuse et plus nette, la met en
format carré sur fond blanc, retire les métadonnées (GPS, modèle du téléphone) et la renvoie.
**N'importe qui sur Telegram peut l'utiliser.** Aucune photo n'est conservée.

Commandes : `/start`, `/confidentialite`, `/conditions` et `/stats` (réservée à l'administrateur).

## Protections intégrées

| Protection | Valeur par défaut | Réglage dans `.env` |
|---|---|---|
| Photos par personne et par heure | 20 | `MAX_PHOTOS_PER_HOUR` |
| Photos par personne et par jour | 60 | `MAX_PHOTOS_PER_DAY` |
| Photos par album | 10 | `MAX_PHOTOS_PER_ALBUM` |
| Taille maximum d'un fichier | 15 Mo | `MAX_FILE_SIZE_MB` |
| Photos traitées en même temps (les autres attendent dans la file) | 2 | `MAX_CONCURRENT_JOBS` |
| Temps maximum par photo | 60 s | `PROCESSING_TIMEOUT_SECONDS` |
| Anti-spam : plus de 5 messages en 10 s, la personne est ignorée 1 min | 5 / 10 s / 60 s | `SPAM_*` |
| Messages par minute dans un groupe | 20 | `GROUP_MAX_MESSAGES_PER_MINUTE` |

Le bot accepte uniquement les images JPEG, PNG, WEBP et HEIC. Il vérifie le vrai contenu du
fichier, pas seulement son nom. Il réduit les images de plus de 4000 px de large avant de
les traiter, et il les traite une par une pour consommer peu de mémoire.

## Statistiques (`/stats`)

Mets ton numéro Telegram dans `ADMIN_USER_ID` : écris à **@userinfobot** sur Telegram
pour le connaître. La commande `/stats` affiche alors le nombre d'utilisateurs différents,
le nombre de photos traitées aujourd'hui et au total, et le nombre d'erreurs. Le fichier
`stats.db` ne contient que des compteurs et des empreintes chiffrées des utilisateurs,
jamais de photo ni d'identifiant en clair.

## Hébergement : obligatoire 24 h/24

Comme le bot est public, il doit tourner en permanence sur un serveur, pas sur ton
ordinateur. Si ton ordinateur s'éteint, le bot ne répond plus à personne.

### Railway (recommandé)

1. Crée un compte sur [railway.com](https://railway.com) avec ton compte GitHub.
2. **New Project → Deploy from GitHub repo** → choisis `motion-design`.
3. Dans **Settings**, mets **Root Directory** = `bot-telegram`. Railway lit le `Procfile`
   et lance `python bot.py` tout seul.
4. Dans **Variables**, ajoute `TELEGRAM_BOT_TOKEN` et `ADMIN_USER_ID`. Les autres
   variables sont facultatives : les valeurs par défaut s'appliquent.
5. Optionnel, pour que `/stats` ne reparte pas de zéro à chaque mise à jour : ajoute un
   **Volume** monté sur `/data`, puis la variable `STATS_DB_PATH=/data/stats.db`.

### Render

Sur Render, crée un **Background Worker** avec Root Directory `bot-telegram`, la commande
de build `pip install -r requirements.txt` et la commande de lancement `python bot.py`.
Attention : l'offre gratuite de Render ne propose que des « Web Services » qui
s'endorment après 15 minutes sans visite. Un bot Telegram s'y arrête donc. Sur Render,
il faut une offre payante (environ 7 $/mois).

### Les limites du gratuit

- **Mémoire** : les offres gratuites ou d'entrée de gamme donnent environ 512 Mo de mémoire.
  Une photo de 4000 px demande environ 100 à 150 Mo pendant son traitement. C'est pour ça
  que le bot n'en traite que 2 à la fois. Ne monte pas `MAX_CONCURRENT_JOBS` au-delà de 2
  sans plus de mémoire.
- **Temps de calcul** : Railway offre un crédit d'essai, puis l'offre Hobby coûte environ
  5 $/mois, utilisation comprise pour un petit bot. Les tarifs changent : vérifie-les sur
  le site.
- **Si beaucoup de monde l'utilise** : les gens attendent plus longtemps. Le bot leur
  indique « Tu es en position X dans la file ». Il ne plante pas, il ralentit. Si l'attente
  devient trop longue, passe à une offre avec plus de mémoire et de processeur, puis monte
  `MAX_CONCURRENT_JOBS` à 3 ou 4. Les quotas par personne empêchent une seule personne
  de bloquer tout le monde.
- Telegram limite les fichiers que les bots peuvent télécharger à 20 Mo. La limite de
  15 Mo du bot reste en dessous.

## Lancer sur un ordinateur (pour essayer)

```bash
cd bot-telegram
pip install -r requirements.txt
cp .env.example .env      # puis colle ton token dans .env
python bot.py
```

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

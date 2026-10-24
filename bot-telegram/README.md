# Bot Telegram « Photo Pro » (public)

Le bot reçoit une photo de produit. Il la rend plus lumineuse et plus nette, la met en
format carré sur fond blanc, retire les métadonnées (GPS, modèle du téléphone) et la renvoie.
**N'importe qui sur Telegram peut l'utiliser.** Aucune photo n'est conservée.

Commandes : `/start`, `/confidentialite`, `/conditions`, `/monid` et `/stats` (réservée à l'administrateur).
Au démarrage, le bot remplit tout seul son menu de commandes et sa description sur Telegram.

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

Mets ton numéro Telegram dans `ADMIN_USER_ID`. Pour le connaître, envoie `/monid` au bot. La commande `/stats` affiche alors le nombre d'utilisateurs différents,
le nombre de photos traitées aujourd'hui et au total, et le nombre d'erreurs. Le fichier
`stats.db` ne contient que des compteurs et des empreintes chiffrées des utilisateurs,
jamais de photo ni d'identifiant en clair.

## Hébergement : obligatoire 24 h/24

Comme le bot est public, il doit être hébergé sur un serveur, pas sur ton ordinateur.
Si ton ordinateur s'éteint, le bot ne répond plus à personne.

### Render, offre gratuite (recommandé)

Sur Render, le bot fonctionne en mode « webhook » : c'est Telegram qui le contacte à
chaque message. Le bot le détecte tout seul, il n'y a rien à régler. Grâce à ce mode,
l'offre gratuite suffit. Le bot s'endort après 15 minutes sans message, et le message
suivant le réveille. Ce premier message met alors environ 1 minute à recevoir sa
réponse, les suivants sont rapides.

1. Crée un compte sur [render.com](https://render.com) avec ton compte GitHub.
2. Clique sur **New +**, puis **Blueprint**, et choisis le dépôt `motion-design`.
   Render lit le fichier `render.yaml` et prépare tout.
3. Render demande deux valeurs :
   - `TELEGRAM_BOT_TOKEN` : le code secret donné par @BotFather ;
   - `ADMIN_USER_ID` : laisse vide pour l'instant.
4. Clique sur **Apply** et attends 2 à 3 minutes.
5. Envoie `/monid` à ton bot. Mets le numéro qu'il te répond dans **Environment →
   ADMIN_USER_ID** sur Render, puis enregistre.

### Railway (si les inscriptions sont ouvertes)

Choisis **New Project**, puis **Deploy from GitHub repo**, avec Root Directory =
`bot-telegram`, et ajoute les variables `TELEGRAM_BOT_TOKEN` et `ADMIN_USER_ID`. Le bot y
tourne en continu. Railway coûte environ 5 $ par mois après le crédit d'essai.

### Les limites du gratuit

- **Mémoire** : les offres gratuites ou d'entrée de gamme donnent environ 512 Mo de mémoire.
  Une photo de 4000 px demande environ 100 à 150 Mo pendant son traitement. C'est pour ça
  que le bot n'en traite que 2 à la fois. Ne monte pas `MAX_CONCURRENT_JOBS` au-delà de 2
  sans plus de mémoire.
- **Temps de calcul** : l'offre gratuite de Render donne 750 heures par mois, ce qui
  suffit pour un bot qui tourne tout le mois. Le processeur est lent, donc une photo met
  quelques secondes. Les tarifs changent : vérifie-les sur le site.
- **Statistiques** : sur l'offre gratuite, le disque est effacé à chaque mise en veille ou
  mise à jour. `/stats` compte donc depuis le dernier réveil du bot. Pour garder les
  chiffres sur la durée, il faut une offre payante avec un disque permanent : mets alors
  `STATS_DB_PATH` sur ce disque.
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

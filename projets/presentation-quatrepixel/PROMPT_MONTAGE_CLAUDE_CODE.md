# Montage final « Présentation Quatrepixel » avec HyperFrames

Tu fais le montage final d'une pub verticale pour Quatrepixel (Sofiane, créateur de flyers vidéo, Lyon). Tout est déjà décidé : ne change pas l'histoire, l'ordre ni les textes. Ton travail est d'assembler, de rendre ça fluide et beau, puis de livrer un MP4.

Dépôt GitHub `sofiane382/motion-design`, branche `claude/charming-feynman-3yb2ow`. Tout est dans `projets/presentation-quatrepixel/` :

- `sources/clip_1.mp4` … `clip_6.mp4` : les 6 clips finaux (9:16, avec son ; 2160x3840 sauf `clip_4` en 1440x2560 60 i/s).
- `references/flyer/flyer_tmax.jpg` : l'image du flyer de fin (1116x2000) : le Bitmoji de Quatrepixel au guidon d'un TMAX, le vendeur derrière avec une liasse de billets, cartons vides à côté.
- `references/flyer/snapcode_quatrepixel.jpg` : le Snapcode de Quatrepixel, à poser en carte sur le flyer.
- `montage/flyer/fonts/` : polices Anton, Permanent Marker, Archivo Black.
- `montage/snap/maquette_snap_v3.py` : la maquette validée des écrans Snap. C'est la référence visuelle et de rythme : reproduis-la en mieux (animations), sans changer les textes ni l'ordre.
- `README.md` : tout l'historique des décisions (à lire en entier avant de commencer).

Sofiane parle français, n'est pas technique, et ajoutera lui-même la musique dans CapCut. Ne lui pose de questions que si quelque chose est vraiment bloquant.

## Outil

HyperFrames (CLI npm `hyperframes`, compositions HTML rendues en vidéo). Commence par `npx hyperframes@latest --help` et sa doc pour connaître la vraie syntaxe ; n'invente pas d'options. Pour ce que HyperFrames ne sait pas faire (découpe, vitesse, son, retrait du logo), prépare les fichiers avec ffmpeg avant, puis compose dans HyperFrames.

## Sortie attendue

- `projets/presentation-quatrepixel/export/quatrepixel_presentation.mp4` : 1080x1920, 30 i/s, H.264 haute qualité (voir « Qualité de l'image »), AAC 48 kHz stéréo, environ 32 s. Plus une version 4K.
- Sons des clips GARDÉS (motos, foule, vent…) + les petits sons des écrans Snap. AUCUNE musique.
- JAMAIS de sous-titres (Sofiane insiste), aucun texte en dehors de ceux des écrans Snap et du flyer.
- Commit + push du projet HyperFrames, des scripts et de l'export sur la branche.

## Montage, plan par plan

| # | Plan | Source et coupe | Vitesse | Durée finale |
|---|---|---|---|---|
| 1 | Le calme : il est seul sur sa chaise, la boule de foin passe | `clip_1` entier (8,55 s, 60 i/s) | x1,9 | ≈ 4,5 s |
| 2 | Il s'ennuie, prend son tel, l'écran s'allume | `clip_2` de 0 à 3,13 s | x1,25 | ≈ 2,5 s |
| 3 | ÉCRAN SNAP partie 1 (voir plus bas) | HyperFrames | — | ≈ 3,8 s |
| 4 | Gros plan : il lit, surpris → sourire | `clip_2` de 3,13 s à la fin | x1 | ≈ 2,9 s |
| 5 | ÉCRAN SNAP partie 2 (voir plus bas) | HyperFrames | — | ≈ 3,6 s |
| 6 | Il lève la tête et sourit | `clip_3` de 1,0 s à la fin | x1,25 | ≈ 1,2 s |
| 7 | LE ZBEUL : vue d'une fenêtre (parachutistes qui sautent de la tour, motos de partout, foule) puis coupe au sol vers 3,75 s, la foule se jette sur les cartons et lui tend des billets | `clip_4` entier (7,07 s) | x1 | ≈ 7,1 s |
| 8 | AirPods + billets, gros plan | `clip_5` entier | x1 | ≈ 3,2 s |
| 9 | Le calme d'après : seul, cartons vides, billets, grand sourire | `clip_6` de 0 à 3,5 s | x1 | 3,5 s |
| 10 | FLYER DE FIN (voir plus bas) | image + Snapcode | — | 2,5 s |

Quand tu accélères un clip, accélère aussi son son (atempo) pour qu'il reste synchro.

## Logo « Ai » à enlever

Un petit logo blanc « Ai » est en haut à gauche de `clip_1`, `clip_2`, `clip_3`, `clip_5`, `clip_6` (environ x 60-150, y 60-140 sur 2160x3840). L'image du flyer n'en a pas. `clip_4` n'en a pas a priori, vérifie quand même. Enlève-le proprement : ffmpeg `delogo` sur le ciel, ou un léger recadrage (~8 %) si `delogo` laisse une tache visible. Vérifie sur une image de chaque plan, en zoomant, qu'il n'en reste aucune trace.

## Écrans Snap (plans 3 et 5)

Écran plein 9:16, interface claire façon Snapchat, comme `maquette_snap_v3.py` :

- En-tête : flèche retour, avatar rond (le Bitmoji au centre du Snapcode, recadré dans un rond sur fond jaune Snap), nom « Quatrepixel », et dessous « en train d'écrire… » ou « à l'instant ».
- Messages de Quatrepixel : petit label « QUATREPIXEL » en rouge Snap (#F23C57) + barre verticale rouge à gauche + texte noir. Messages de lui : label « MOI » en bleu Snap (#0EADFF) + barre bleue.
- « En train d'écrire » : avatar rond + bulle grise avec 3 points qui pulsent.
- Champ « Envoyer un chat » en bas.
- Les messages s'empilent en partant du bas, comme dans Snap. Chaque nouveau message apparaît avec une petite animation (léger glissement vers le haut + fondu, ~150 ms), jamais d'un coup.
- Emojis en couleur (🔥 👀).

Plan 3 (≈ 3,8 s) : Quatrepixel écrit… (≈ 0,9 s) → ding + « Ton flyer est prêt 🔥 » → écrit… (≈ 0,7 s) → ding + « Mets-le en story ». Laisse le temps de lire chaque message.

Plan 5 (≈ 3,6 s) : il tape « C'est posté » lettre par lettre dans le champ en bas → son d'envoi → le message part (« MOI », bleu, « C'est posté 🔥 ») → Quatrepixel écrit… → ding + « Regarde dehors 👀 ». En même temps, une notification glisse du haut : carte blanche arrondie, pastille jaune avec 👀, « Ma story » en gras, et dessous « Vue par N personnes », N qui s'emballe vite (12 → 85 → 340 → 1 200 → 2 800 → 6 400 → 9 700 → 15 400 → 23 800).

Sons : un petit « ding » doux à chaque message reçu, un petit « swoosh » à l'envoi, des clics discrets quand il tape, un tick léger quand le compteur monte. Volume modéré, rien d'agressif.

## Transitions (retour de Sofiane : les effets spéciaux étaient bizarres, il n'en veut plus)

- Toutes les transitions sont NORMALES : des coupes nettes, comme dans un vrai film. Pas de zoom punch, pas de whip pan, pas de tremblement, pas de flou de mouvement, pas de flash.
- Seule exception douce : un fondu enchaîné très court (≈ 0,15 s) pour entrer dans les écrans Snap et en sortir (2 → 3, 3 → 4, 4 → 5, 5 → 6).
- 6 → 7 (début du zbeul) : coupe nette, le son des motos part d'un coup.
- La coupe interne du zbeul (fenêtre → sol, vers 3,75 s) reste une coupe nette.
- 8 → 9 (zbeul → calme d'après) : transition « changement de monde », POUSSIÈRE + FONDU AU NOIR (validé par Sofiane), ≈ 1,1 s au total :
  1. sur la fin du plan AirPods, un nuage de poussière dorée (fumée réaliste, éclairée par le coucher de soleil, qui monte du bas et des côtés) envahit l'écran en ≈ 0,5 s, pendant que le son de la foule s'étouffe (filtre passe-bas qui descend, comme une tête sous l'eau) ;
  2. la poussière s'assombrit jusqu'au noir complet (≈ 0,3 s) ;
  3. ≈ 0,3 s de noir et de silence ;
  4. le plan du calme apparaît depuis le noir (fondu ≈ 0,4 s) avec le vent ; quelques grains de poussière flottent encore dans les rayons du soleil pendant la première seconde, puis disparaissent.
  AUCUN texte (pas de « quelques minutes plus tard »). La poussière doit avoir l'air vraie, pas un filtre plat.
- 9 → 10 (calme → flyer) : fondu enchaîné court (≈ 0,3 s).

## Qualité de l'image (retour de Sofiane : le premier montage était devenu moche)

- Les sources sont en 2160x3840 (`clip_4` en 1440x2560). Ne les dégrade jamais avant l'export final.
- Pas de compressions en cascade : intermédiaires sans perte (images PNG ou vidéo en `-crf 0` / ProRes 4444), un seul encodage final.
- Redimensionnement en `lanczos`, sans netteté artificielle ni débruitage.
- Dans HyperFrames, prends le réglage de rendu le plus haut (images PNG, pas JPEG, qualité maximale) ; vérifie les options avec `--help`.
- Export final : 1080x1920 en H.264 `-crf 14 -preset slow -pix_fmt yuv420p`, débit ≥ 15 Mb/s, AAC 320 kb/s. Fais AUSSI une version 2160x3840 (`quatrepixel_presentation_4K.mp4`), même réglages.
- Le retrait du logo « Ai » ne doit laisser ni tache ni flou visible. Si `delogo` abîme le ciel, recadre légèrement à la place.
- Avant de livrer, compare une image de chaque plan à la même image dans la source : la netteté et les couleurs doivent être les mêmes.

## Flyer de fin (plan 10, 2,5 s)

Base : `flyer_tmax.jpg`, mise à l'échelle en 1080x1920 sans déformer (recadre légèrement si besoin), avec un très léger zoom avant continu (1,00 → 1,04). Zones libres pour les textes : le ciel en haut (au-dessus des personnages, environ le premier quart de l'image) et le sol en bas (sous la roue avant, environ le dernier cinquième).

Snapcode : pose `snapcode_quatrepixel.jpg` en carte (le carré jaune à coins arrondis, recadré sans le texte du dessous), dans la zone du bas, avec une ombre douce. Il doit rester net et scannable : au moins 260 px de côté en 1080x1920. Ne le pose sur aucun personnage ni sur le TMAX.

Textes (uniquement ceux-là, pas de prix, pas de délai, pas de liste de commerces) :

1. En haut, sur le ciel : « TON FLYER VIDÉO », très gros et très lisible.
2. Sur un bandeau à côté du titre, plus petit : « Démarque-toi de la concurrence ».
3. En bas, à côté de la carte Snapcode : un bouton « Ajoute-moi sur Snapchat », et dessous le nom d'utilisateur « quatrepixel ».
4. Sur une ligne d'info avec une icône de repère de carte : « LYON · 38 · 69 ».

Direction artistique : inspire-toi FORTEMENT de `references/flyer/exemple_style_flyer.png` (flyer que Sofiane adore), en gardant nos textes et nos couleurs. PAS de police banale (pas d'Arial, pas d'Inter, pas de police système). Ce qu'il faut reprendre de cet exemple :

- les textes sont posés sur des **bandeaux noirs inclinés** (légère rotation, environ -4°), avec des bords nets et une ombre portée : ça fait affiche de rue premium ;
- le **titre** « TON FLYER VIDÉO » est énorme, en capitales grasses condensées (Anton, dans `montage/flyer/fonts/`), blanc sur bandeau noir incliné, avec « VIDÉO » en jaune Snap (#FFFC00) ;
- le **sous-titre** « Démarque-toi de la concurrence » va sur un bandeau noir plus fin, juste au-dessus ou en dessous du titre, en petites capitales ;
- une **ligne d'info avec une icône** (comme la main de l'exemple) : une icône de repère de carte + « LYON · 38 · 69 », sur un petit bandeau ;
- en bas, un **gros bouton brillant et arrondi** comme le bouton bleu de l'exemple, mais en **jaune Snap** avec un léger dégradé et un reflet. À l'intérieur : une pilule noire « AJOUTE-MOI SUR SNAPCHAT » en capitales blanches, puis l'icône fantôme Snapchat + « QUATREPIXEL » en très gros, noir et gras ;
- la **carte Snapcode** juste au-dessus ou à côté du bouton, pour qu'on puisse la scanner ;
- du **relief partout** : ombres portées nettes, légers contours, contraste fort. Ça doit claquer comme l'exemple, sans surcharger : seulement nos textes, rien d'autre.

Ajoute des dégradés sombres discrets en haut et en bas pour que tout se lise sur l'image. Laisse les deux visages, le TMAX et la liasse de billets bien visibles : aucun texte dessus.

Animation d'entrée, dans l'ordre et rapide (tout est en place avant 1,2 s, puis l'image tient) :

- titre qui arrive avec un petit rebond ;
- sous-titre en fondu ;
- la carte Snapcode qui apparaît avec un léger rebond et un petit halo jaune ;
- bouton jaune Snapchat qui « pop » ;
- la ligne « LYON · 38 · 69 » qui glisse sur le côté.

## Vérifications avant de livrer (obligatoires)

1. Durée totale ≈ 32 s (entre 30 et 33 s). Les durées de chaque plan correspondent au tableau.
2. Extrais une image au milieu de chaque plan et regarde-la. Vérifie qu'il n'y a pas de logo « Ai », pas de bord noir, pas de déformation, et que les textes Snap sont lisibles et sans faute.
3. Flyer en pleine résolution : Snapcode net, sans aucun vert visible, textes lisibles et pas sur le visage.
4. Son : pas de saturation (pic < -1 dB), son synchro sur les plans accélérés, coupe sèche bien nette entre le plan 8 et le plan 9.
5. Fais une planche contact de tout le montage (1 image toutes les 0,5 s) et regarde-la en entier avant de déclarer que c'est fini.

À la fin, donne à Sofiane en quelques lignes simples, en français :
- où est la vidéo ;
- sa durée ;
- ce que tu as fait pour les transitions et le flyer ;
- s'il reste un défaut.

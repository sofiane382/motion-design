# Montage final « Présentation Quatrepixel » avec HyperFrames

Tu fais le montage final d'une pub verticale pour Quatrepixel (Sofiane, créateur de flyers vidéo, Lyon). Tout est déjà décidé : ne change pas l'histoire, l'ordre ni les textes. Ton travail est d'assembler, de rendre ça fluide et beau, puis de livrer un MP4.

Dépôt GitHub `sofiane382/motion-design`, branche `claude/charming-feynman-3yb2ow`. Tout est dans `projets/presentation-quatrepixel/` :

- `sources/clip_1.mp4` … `clip_6.mp4` : les 6 clips finaux (2160x3840, 9:16, avec son).
- `references/flyer/flyer_ecran_vert.webp` : l'image du flyer de fin (1116x2000), avec un téléphone à écran vert.
- `references/flyer/snapcode_quatrepixel.jpg` : le Snapcode à incruster dans cet écran.
- `montage/snap/maquette_snap_v3.py` : la maquette validée des écrans Snap. C'est la référence visuelle et de rythme : reproduis-la en mieux (animations), sans changer les textes ni l'ordre.
- `README.md` : tout l'historique des décisions (à lire en entier avant de commencer).

Sofiane parle français, n'est pas technique, et ajoutera lui-même la musique dans CapCut. Ne lui pose de questions que si quelque chose est vraiment bloquant.

## Outil

HyperFrames (CLI npm `hyperframes`, compositions HTML rendues en vidéo). Commence par `npx hyperframes@latest --help` et sa doc pour connaître la vraie syntaxe ; n'invente pas d'options. Pour ce que HyperFrames ne sait pas faire (découpe, vitesse, son, retrait du logo), prépare les fichiers avec ffmpeg avant, puis compose dans HyperFrames.

## Sortie attendue

- `projets/presentation-quatrepixel/export/quatrepixel_presentation.mp4` : 1080x1920, 30 i/s, H.264, AAC 48 kHz stéréo, environ 31 s.
- Sons des clips GARDÉS (motos, foule, vent…) + les petits sons des écrans Snap. AUCUNE musique.
- Aucun sous-titre, aucun texte en dehors de ceux listés ici.
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
| 7 | LE ZBEUL : vue d'une fenêtre (motos, parachutes noirs, foule) puis coupe au sol, la foule vide les cartons | `clip_4` entier | x1 | ≈ 6,0 s |
| 8 | AirPods + billets, gros plan | `clip_5` entier | x1 | ≈ 3,2 s |
| 9 | Le calme d'après : seul, cartons vides, billets, grand sourire | `clip_6` de 0 à 3,5 s | x1 | 3,5 s |
| 10 | FLYER DE FIN (voir plus bas) | image + Snapcode | — | 2,5 s |

Quand tu accélères un clip, accélère aussi son son (atempo) pour qu'il reste synchro.

## Logo « Ai » à enlever

Un petit logo blanc « Ai » est en haut à gauche de `clip_1`, `clip_2`, `clip_3`, `clip_5`, `clip_6` et du flyer (environ x 60-150, y 60-140 sur 2160x3840 ; environ x 25-75, y 25-70 sur l'image du flyer). `clip_4` n'en a pas, mais vérifie quand même. Enlève-le proprement : ffmpeg `delogo` sur le ciel, ou un léger recadrage (~8 %) si `delogo` laisse une tache visible. Vérifie sur une image de chaque plan, en zoomant, qu'il n'en reste aucune trace.

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

## Transitions et effets (fluide, dynamique, propre)

- 1 → 2 : petit zoom punch vers lui avec flou de mouvement (≈ 0,25 s).
- 2 → 3 : zoom dans l'écran du téléphone qui s'allume, l'écran Snap grandit depuis la position du téléphone jusqu'au plein écran (≈ 0,3 s).
- 3 → 4 : l'écran Snap se rétracte / zoom arrière rapide vers le gros plan (≈ 0,25 s).
- 4 → 5 : de nouveau zoom dans son téléphone vers l'écran Snap (≈ 0,3 s).
- 5 → 6 : whip pan vertical vers le haut (flou de mouvement), calé sur le moment où il lève la tête (≈ 0,2 s).
- 6 → 7 : IMPACT. Coupe sèche sur le zbeul avec un court tremblement de caméra et un zoom punch (≈ 0,3 s), le son des motos qui part d'un coup.
- La coupe interne du zbeul (fenêtre → sol, vers 3,33 s) reste une coupe nette.
- 7 → 8 : whip pan horizontal (≈ 0,2 s).
- 8 → 9 : COUPE SÈCHE volontaire, sans effet : le bruit de la foule s'arrête net et on tombe dans le calme (vent). C'est le gag, ne le lisse pas.
- 9 → 10 : la dernière image du calme glisse vers le flyer avec un fondu court et lumineux (≈ 0,4 s).
- Pas de flash blanc plein écran. Pas d'effets gadgets en trop : chaque transition doit servir le rythme.

## Flyer de fin (plan 10, 2,5 s)

Base : `flyer_ecran_vert.webp` (logo « Ai » retiré), mise à l'échelle en 1080x1920 sans déformer (recadre légèrement si besoin), avec un très léger zoom avant continu (1,00 → 1,04).

Snapcode dans le téléphone : remplace tout le vert de l'écran (environ coins (190,442), (330,438), (354,742), (212,752) sur l'image 1116x2000) par `snapcode_quatrepixel.jpg`, en perspective pour suivre l'inclinaison du téléphone. Utilise le vert comme masque (incrustation chroma) pour garder les coins arrondis, et ne laisse aucun liseré vert. Le Snapcode doit rester net et scannable.

Textes (uniquement ceux-là, pas de prix, pas de délai, pas de liste de commerces) :

1. En haut, sur le ciel : « TON FLYER VIDÉO », très gros et très lisible.
2. Juste en dessous, plus petit : « qui fait venir tout le quartier ».
3. En bas : un bouton « Ajoute-moi sur Snapchat », et dessous le nom d'utilisateur « quatrepixel ».
4. Tout en bas : « LYON · 38 · 69 ».

Direction artistique : PAS de police banale (pas d'Arial, pas d'Inter, pas de police système). Rendu très clean, beau et attirant, ambiance street / rap premium. Par exemple :

- titre dans une grosse police condensée (Anton ou Bebas Neue, Google Fonts), blanc avec une ombre portée nette ou un léger relief, et « VIDÉO » en jaune Snap (#FFFC00) ;
- sous-titre dans une police plus fine ou au style marqueur (Permanent Marker) ;
- bouton Snapchat en pilule jaune Snap, texte noir gras ;
- « LYON · 38 · 69 » espacé, en capitales.

Ajoute des dégradés sombres discrets en haut et en bas pour que tout se lise sur l'image. Laisse son visage, le téléphone et les billets bien visibles : aucun texte dessus.

Animation d'entrée, dans l'ordre et rapide (tout est en place avant 1,2 s, puis l'image tient) :

- titre qui arrive avec un petit rebond ;
- sous-titre en fondu ;
- l'écran du téléphone qui s'allume avec un léger halo ;
- bouton Snapchat qui « pop » ;
- « LYON · 38 · 69 » qui glisse depuis le bas.

## Vérifications avant de livrer (obligatoires)

1. Durée totale ≈ 31 s (entre 29 et 32 s). Les durées de chaque plan correspondent au tableau.
2. Extrais une image au milieu de chaque plan et regarde-la. Vérifie qu'il n'y a pas de logo « Ai », pas de bord noir, pas de déformation, et que les textes Snap sont lisibles et sans faute.
3. Flyer en pleine résolution : Snapcode net, sans aucun vert visible, textes lisibles et pas sur le visage.
4. Son : pas de saturation (pic < -1 dB), son synchro sur les plans accélérés, coupe sèche bien nette entre le plan 8 et le plan 9.
5. Fais une planche contact de tout le montage (1 image toutes les 0,5 s) et regarde-la en entier avant de déclarer que c'est fini.

À la fin, donne à Sofiane en quelques lignes simples, en français :
- où est la vidéo ;
- sa durée ;
- ce que tu as fait pour les transitions et le flyer ;
- s'il reste un défaut.

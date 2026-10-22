# Vidéo de présentation Quatrepixel (flyers vidéo)

Format : vertical 9:16, 720x1280, 24 i/s. Clips générés avec Seedance (CapCut), montage CapCut.

## Ordre du montage

| # | Plan | Source | Statut |
|---|---|---|---|
| 1 | Le calme : seul sur sa chaise, boule de foin | `clip_1` en entier (10 s) | ✅ validé |
| 2 | Plan sur lui, il s'ennuie, prend son tel | `clip_1_rater` à partir de **2,04 s** (6 s) | ✅ monté par Sofiane |
| 3 | ~~Notif Snapchat de Quatrepixel~~ | — | ❌ enlevée |
| 3b | Il lève la tête, inspire, petit sourire (il entend arriver le quartier) | `clip_2_refais` de 0 à **3,0 s** | ✅ gardé |
| 4 | **Le zbeul** (vue fenêtre puis coupe au sol) | Seedance, `prompts/zbeul_seedance_v4_fenetre.json` | ✅ validé (un peu juste en monde) |
| 5 | Il distribue les AirPods, billets dans les mains | `clip_2` de **6,83 s à la fin** (3,2 s) | ✅ gardé |
| 5b | ~~Flash blanc + sifflement~~ : abandonné, transition à trouver au montage | HyperFrames (Claude) | ⏳ |
| 6 | Le calme d'après : même plan que le début, plus personne, cartons vides façon « après l'apocalypse » ; vue de côté, contre-jour ; sourire touché comme un cadeau (pas fier) ; quelques liasses | Seedance, `prompts/calme_seedance.json` | ⏳ à générer |
| 7 | Flyer : Snap quatrepixel + Lyon 38/69 | HyperFrames | ⏳ à faire |

Jeté : `clip_2_refais` après 3,0 s (les bécanes écrasent le stock et continuent tout droit ;
la fin avec la foule cagoulée est bien mais casse la cohérence), et `clip_2` avant 6,83 s.

## Le zbeul : ce qu'on veut

- Les bécanes déboulent en roue arrière et **s'arrêtent devant lui**. Elles n'écrasent rien, ne repartent pas derrière.
- Des gens tombent du ciel en **parachutes noirs**.
- Il **se lève et lève les bras** (comme dans `clip_2_refais`), tout le monde vient vers lui.
- Jeunes de quartier : beaucoup cagoulés, beaucoup non, coupes dégradées, casquettes, survêts.
- Tout le monde crie, saute, se bat pour atteindre les cartons, prend les articles et **lui tend des billets**.
- Stock : AirPods, parfums, puffs, casquettes de luxe, sacoches de luxe.
- Bécanes : 2-3 sautent par-dessus le muret du fond, quelques-unes sortent du passage à droite (couloir du bâtiment), quelques-unes passent à côté de la caméra. Toutes S'ARRÊTENT autour du stand.
- Plan large : comme dans `16.9_clip_2` (caméra au ras du sol, très loin, lui petit au fond), mais en 9:16 → nouveau décor à faire d'abord (Seedance copie le cadrage du décor).
- Raté dans `16.9_clip_2` : bécanes et gens vont tout droit, le dépassent et écrasent le stock ; parachutes arc-en-ciel (les vouloir NOIRS) ; les cagoulés se servent dans les cartons = on dirait un braquage. Il faut qu'ils ACHÈTENT : billets tendus vers lui, il encaisse, ils se battent pour acheter.
- Ambiance : vraiment la street. Ça crie, saute, se bouscule, se rentre dedans, jette des trucs, arrive en roue arrière. Le chaos est AUTOUR ; LE VENDEUR et LE STAND restent stables et lisibles.
- Doit finir serré sur lui entouré de mains, pour raccorder avec le plan AirPods (`references/raccord_airpods_debut.png`).

## Prompt Seedance

`prompts/zbeul_seedance.json` — Images : 1 = `1_visage_vendeur.jpg`, 2 = `2_en_pied_vendeur.jpg`, 3 = `3_decor_stand.jpg`. Réglages : 9:16, 8 s (x1,25 au montage), Seedance 2.0 normale, Référence de tout type, son activé, sous-titres décochés.

## Points à régler avant le prompt

- Durée (réglée) : clip_1 en x2 = 5 s, clip_1_rater en x1,25 = 4,8 s, Snap ~2,5 s, **zbeul ~7 s** (1 clip, 2-3 plans), AirPods 3,2 s, flyer ~2,5 s → ~25 s.
- Foule (validé) : surtout des cagoules, quelques visages pas vraiment nets, rendu réaliste. Un seul visage net : LE VENDEUR.
- Références (reçues) : `references/1_visage_vendeur.jpg`, `2_en_pied_vendeur.jpg`, `3_decor_stand.jpg` (logo « Ai » recadré). La fiche multi-vues sert seulement à valider le perso.

## Essai Seedance du zbeul (1er essai) : retour

- Plan 1 : plan large au ras du sol, parachutes noirs, cross qui sautent le muret, TMAX : OK. MAIS le décor a été réinventé (grand mur tagué) et LE STAND + LE VENDEUR sont collés au muret, minuscules ; les bécanes atterrissent devant lui et foncent vers la caméra.
  Cause probable : j'ai demandé un cadrage « beaucoup plus loin et plus bas que @Image 3 » → Seedance a reconstruit le décor au lieu de garder @Image 3.
- Plan 2 : il se lève et lève les bras : OK. MAIS cadré pile au centre face caméra (le 3/4 sur le tiers gauche a été ignoré) et la foule est 100 % cagoules noires → effet bande / braquage.
- Plan 3 : il encaisse et donne les AirPods, visage stable : le meilleur plan. MAIS billets en DOLLARS : j'avais écrit « billets de banque » sans préciser euros.
- Logo « Ai » en haut à gauche.

## Zbeul v2 : décisions validées

- Ce qui manque = UNIQUEMENT l'arrivée de tout le monde pour acheter. Pas de plan où il encaisse (le plan AirPods de `clip_2` existe déjà).
- 2 plans : (1) plan large, cadrage identique à `3_decor_stand.jpg`, bécanes de partout qui s'arrêtent autour du stand, parachutes noirs, foule qui accourt, il se lève et ouvre grand les bras sur les côtés comme dans `clip_2_refais` vers 7 s ; (2) plan moyen, foule autour de lui qui crie, saute, se bouscule et agite des billets.
- Billets : DOLLARS (raccord avec le plan AirPods).
- Perso identique à la fiche : lentilles C.P. Company (bonnet, manche gauche, poche cuisse gauche), baskets Mizuno noires.
- Dreamina, Seedance 2.0, Référence Omni, 9:16, 6 s (~90 crédits sur 200 → un 2e essai possible).

## Essai v3 (vue fenêtre) : retour de Sofiane

- Bécanes SANS PILOTE : le prompt ne disait jamais « avec un pilote dessus ».
- Foule pas « mecs de quartier » : « flous » + description trop courte → foule générique.
- Ils n'achètent pas, ne vident pas le stock : le prompt interdisait de toucher LE STAND (« totalement immobile », « personne ne touche »). Erreur : il veut qu'ils se jettent tous sur les cartons ET paient (billets tendus), et que le stock soit vidé d'un coup.

## Montage final

- Fait par Claude avec HyperFrames quand Sofiane envoie tous les clips.
- Musique : Sofiane ajoute lui-même son rap dans CapCut après le montage. Le montage HyperFrames sort SANS musique.

## Plan calme, essai 1 : retour

- Beaucoup trop proche (il est coupé à droite), seulement 2 cartons, posés proprement.
- Il passe à travers les cartons, s'enfonce dans le sol, chaise minuscule, il paraît tout petit, carton bizarre.
- Sourire pas aimé. Choix validé : JOIE FRANCHE, grand sourire avec les dents, yeux qui brillent, content comme un gamin.
- À corriger : plan large (en entier, un tiers de la hauteur), cartons à un mètre de lui sur les côtés (jamais devant son corps), pieds à plat, chaise taille normale, cartons simples vides et renversés.

## Clips finaux reçus (22:41) — analyse

Tous en 2160x3840 (9:16, 4K), avec leur son. Le son des clips est GARDÉ ; Sofiane ajoute la musique dans CapCut ; Claude ajoute un son « Desert Cowboy » (western) fourni par Sofiane.

| Fichier | Durée | i/s | Contenu | Coupes | Logo « Ai » |
|---|---|---|---|---|---|
| `clip_1-1.mp4` | 8,55 s | 60 | Le calme, plan large, boule de foin qui arrive et finit en gros plan devant la caméra | aucune | oui, haut gauche |
| `clip_2-1.mp4` | 6,00 s | 30 | Il s'ennuie, prend son tel, puis gros plan surpris → sourire | 3,13 s | oui |
| `clip_3-1.mp4` | 2,55 s | 30 | Il tape sur son tel, lève la tête, sourit | aucune | oui |
| `clip_4-1.mp4` | 6,04 s | 30 | Zbeul : vue fenêtre (cross, parachutes noirs, foule) puis coupe au sol, la foule vide les cartons, il a les bras ouverts | 3,33 s | non |
| `clip_5-1.mp4` | 3,20 s | 30 | AirPods + billets, gros plan, surpris → grand sourire | (mouvements rapides, pas de vraie coupe) | oui |

Total : 26,35 s sans le calme ni le flyer → il faudra raccourcir (règle ≤ 25 s).
Volumes moyens : clip_1 -44 dB, clip_2 -50 dB (quasi muets), clip_3 -28 dB, clip_4 -18 dB, clip_5 -16 dB.

## Reçus aussi (22:44)

- `clip_6-1.mp4` : 4,07 s, 2160x3840, 30 i/s. Le calme d'après : plan large, il est assis en entier, pieds au sol, cartons vides autour, billets dans les mains, sourire qui monte. Logo « Ai » à vérifier. Bon.
- `cowboy-standoff.mp3` : 19,2 s, musique western continue (~-16 dB), sans silence ni pic.
- Flyer : image fixe 9:16 du VENDEUR debout, cartons vides, liasse de dollars, téléphone à écran VERT tendu vers nous (écran incliné, coin haut gauche ≈ (190,440), coin bas droit ≈ (355,750) sur 1116x2000). Logo « Ai » en haut à gauche. Fichier à récupérer (pas encore sur le disque).

## Scénario de montage proposé (≈ 25 s)

| # | Plan | Source et coupe | Vitesse | Durée finale |
|---|---|---|---|---|
| 1 | Le calme, la boule de foin | `clip_1-1` 0,0 → 8,55 s | x1,6 | 5,3 s |
| 2 | Il s'ennuie, prend son tel, gros plan surpris → sourire | `clip_2-1` 1,0 → 6,0 s | x1,2 | 4,2 s |
| 3 | Il tape sur son tel, lève la tête, sourit | `clip_3-1` entier | x1,25 | 2,0 s |
| 4 | LE ZBEUL : vue fenêtre puis coupe au sol | `clip_4-1` entier | x1 | 6,0 s |
| 5 | AirPods + billets | `clip_5-1` entier | x1,25 | 2,6 s |
| 6 | Coupe sèche → le calme d'après | `clip_6-1` 0,0 → 3,0 s | x1 | 3,0 s |
| 7 | Flyer : image fixe, Snapcode incrusté dans l'écran vert, léger zoom avant | image | — | 2,5 s |

Son : sons des clips gardés. ANNULÉ : le son western (`cowboy-standoff.mp3`), Sofiane gère toute la musique dans CapCut.

À AJOUTER (HyperFrames) : la séquence Snap. Quand il est sur son téléphone, on voit l'écran Snap : Quatrepixel lui envoie « ton flyer est terminé… » (texte à choisir), puis il le met en story. Très court.
Logo « Ai » : recadré sur tous les plans et le flyer (léger zoom ~6 %).

## Scénario de montage v2 (Sofiane : jusqu'à 30 s max, c'est OK)

| # | Plan | Source et coupe | Vitesse | Durée |
|---|---|---|---|---|
| 1 | Le calme, la boule de foin | `clip_1-1` entier | **x1,9** (demandé par Sofiane) | 4,5 s |
| 2 | Il s'ennuie, prend son tel, l'écran s'allume | `clip_2-1` 0 → 3,13 s | x1,25 | 2,5 s |
| 3 | Écran Snap : conversation Quatrepixel, « en train d'écrire… » puis ding + « Ton flyer est prêt 🔥 Mets-le en story » | HyperFrames | — | 1,3 s |
| 4 | Gros plan : il lit, surpris → sourire | `clip_2-1` 3,13 → 6,0 s | x1 | 2,9 s |
| 5 | Il tape sur son tel (bulle « Ajouté à ta story ✓ »), lève la tête, sourit | `clip_3-1` entier | x1,25 | 2,0 s |
| 6 | LE ZBEUL | `clip_4-1` entier | x1 | 6,0 s |
| 7 | AirPods + billets | `clip_5-1` entier | x1 | 3,2 s |
| 8 | Coupe sèche → le calme d'après | `clip_6-1` 0 → 3,5 s | x1 | 3,5 s |
| 9 | Flyer : image fixe, Snapcode incrusté dans l'écran vert, léger zoom | image | — | 2,5 s |

Total ≈ 30 s. Maquette de la séquence 2-5 : `montage/snap/maquette_snap.py` (aperçu validé ou non : en attente).

## Séquence Snap : retour sur l'exemple 2

- ✅ Validé : la conversation Snap (en train d'écrire… → ding « Ton flyer est prêt 🔥 » → en train d'écrire… → ding « Mets-le en story »), ~3,8 s, avec le Bitmoji de Quatrepixel.
- ❌ Pas aimé : l'écran « Envoyer à… / Ma story » (mal fait) et les images dedans (miniature du flyer, avatar du vendeur).

## ✅ Montage final validé (v3, ≈ 31 s)

| # | Plan | Source et coupe | Vitesse | Durée |
|---|---|---|---|---|
| 1 | Le calme, la boule de foin | `clip_1-1` entier | x1,9 | 4,5 s |
| 2 | Il s'ennuie, prend son tel, l'écran s'allume | `clip_2-1` 0 → 3,13 s | x1,25 | 2,5 s |
| 3 | Snap partie 1 : Quatrepixel écrit… ding « Ton flyer est prêt 🔥 », écrit… ding « Mets-le en story » | HyperFrames | — | 3,8 s |
| 4 | Gros plan : il lit, surpris → sourire | `clip_2-1` 3,13 → 6,0 s | x1 | 2,9 s |
| 5 | Snap partie 2 : il tape « C'est posté 🔥 » (MOI, bleu), Quatrepixel écrit… ding « Regarde dehors 👀 » + notification « Ma story · Vue par N personnes » (12 → 23 800) | HyperFrames | — | 3,6 s |
| 6 | Il lève la tête et sourit | `clip_3-1` 1,0 → 2,55 s | x1,25 | 1,2 s |
| 7 | LE ZBEUL | `clip_4-1` entier | x1 | 6,0 s |
| 8 | AirPods + billets | `clip_5-1` entier | x1 | 3,2 s |
| 9 | Coupe sèche → le calme d'après | `clip_6-1` 0 → 3,5 s | x1 | 3,5 s |
| 10 | Flyer : image fixe, Snapcode incrusté dans l'écran vert, léger zoom | image flyer | — | 2,5 s |

Référence visuelle des écrans Snap : `montage/snap/maquette_snap_v3.py` (validée « on garde, on pourra changer plus tard »).
Son : sons des clips gardés + ding / envoi des écrans Snap. Pas de musique (Sofiane l'ajoute dans CapCut).
Logo « Ai » à recadrer sur clips 1, 2, 3, 5, 6 et sur le flyer.

## Flyer de fin : textes validés

- Image : `references/flyer/flyer_ecran_vert.webp` (1116x2000, logo « Ai » à recadrer), Snapcode `references/flyer/snapcode_quatrepixel.jpg` à incruster dans l'écran vert.
- En haut : « TON FLYER VIDÉO » + « qui fait venir tout le quartier ».
- « Ajoute-moi sur Snapchat » + nom d'utilisateur (à confirmer par Sofiane ; le Snapcode affiche « quatrepixel »).
- « LYON · 38 · 69 ».
- PAS de liste de commerces, PAS de délai, PAS de prix.
- Typo : pas de police banale. Rendu très clean, beau, attirant (titre gras condensé avec effet, hiérarchie nette, peu de texte).

## Zbeul : à refaire (retour sur `clip_4`)

- Pas assez « zbeul », pas assez de monde.
- Bécanes : elles doivent arriver du côté de la caméra ET un peu d'en face. Là, seulement d'en face.
- Foule floue, bizarre, on ne comprend pas ce que c'est. Cause : mon prompt imposait « la foule reste floue ».
- Pas des jeunes maghrébins / arabes de cité comme voulu. Il veut de vrais jeunes du quartier, typés.
- Tout le monde a la même tenue : il faut des tenues variées.
- En plus : on les voit SAUTER DU BÂTIMENT en parachute (noir). Vraiment beaucoup de monde qui se bouscule dans tous les sens.
- Durée : on peut ajouter 1 s → zbeul ≈ 7 s.
- Décidé : on reste sur la VUE DE LA FENÊTRE (plan 1), puis coupe au sol (plan 2). 7 s.
  Depuis la fenêtre : « côté caméra » = bécanes qui sortent du passage juste sous la fenêtre ; « en face » = bécanes qui sautent le muret du fond. Parachutistes qui sautent du toit de la tour d'en face.
- LE VENDEUR dans `clip_4` : raide, tout droit, « réaction IA », pas naturel. À corriger : vraie réaction humaine, il bouge, il se fait bousculer, il ne pose pas.

## Zbeul final (remplace `clip_4`)

- `sources/clip_4.mp4` = nouvelle version validée par Sofiane (`plan_becane_ect.mp4`) : 7,07 s, 1440x2560, 60 i/s, coupe fenêtre → sol à 3,75 s, pas de logo « Ai » visible.
- Montage total ≈ 32 s.

## Flyer de fin v2 (remplace l'écran vert)

- `references/flyer/flyer_tmax.jpg` : le Bitmoji de Quatrepixel (3D Pixar, lunettes vertes, tenue à pois) au guidon d'un TMAX, le vendeur derrière avec une liasse de dollars, sans casque, à l'arrêt, chaise et cartons vides à côté. Validé. Pas de logo « Ai ».
- Snapcode posé en carte jaune en bas (au montage), plus de téléphone.
- Prompt image : `prompts/flyer_tmax_image.json`.

- Sous-titre du flyer changé : « Démarque-toi de la concurrence » (remplace « qui fait venir tout le quartier »).

## Retours sur le premier montage HyperFrames

- Effets de transition bizarres → transitions normales (coupes nettes, fondus courts pour les écrans Snap).
- Transition zbeul → calme : la coupe sèche ne marche pas, il faut un vrai « changement de monde ». Choix en attente : poussière / fondu au noir / « Quelques minutes plus tard… ».
- Qualité de l'image dégradée → section « Qualité de l'image » ajoutée au prompt (pas de compressions en cascade, export haut débit + version 4K).
- Transition zbeul → calme choisie : poussière dorée qui envahit l'écran + son étouffé → noir → silence → le calme apparaît avec le vent. Aucun texte. JAMAIS de sous-titres.

# Vidéo de présentation Quatrepixel (flyers vidéo)

Format : vertical 9:16, 720x1280, 24 i/s. Clips générés avec Seedance (CapCut), montage CapCut.

## Ordre du montage

| # | Plan | Source | Statut |
|---|---|---|---|
| 1 | Le calme : seul sur sa chaise, boule de foin | `clip_1` en entier (10 s) | ✅ validé |
| 2 | Plan sur lui, il s'ennuie, prend son tel | `clip_1_rater` à partir de **2,04 s** (6 s) | ✅ monté par Sofiane |
| 3 | Notif Snapchat de Quatrepixel « ton flyer est fini » + il poste en story | HyperFrames | ⏳ à faire |
| 3b | Il lève la tête, inspire, petit sourire (il entend arriver le quartier) | `clip_2_refais` de 0 à **3,0 s** | ✅ gardé |
| 4 | **Le zbeul** | Seedance (prompt ci-dessous) | ⏳ à générer |
| 5 | Il distribue les AirPods, billets dans les mains | `clip_2` de **6,83 s à la fin** (3,2 s) | ✅ gardé |
| 6 | Fin | à définir | ❓ |

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

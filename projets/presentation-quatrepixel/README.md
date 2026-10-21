# Vidéo de présentation Quatrepixel (flyers vidéo)

Format : vertical 9:16, 720x1280, 24 i/s. Clips générés avec Seedance (CapCut), montage CapCut.

## Ordre du montage

| # | Plan | Source | Statut |
|---|---|---|---|
| 1 | Le calme : seul sur sa chaise, boule de foin | `clip_1` en entier (10 s) | ✅ validé |
| 2 | Plan sur lui, il s'ennuie, prend son tel | `clip_1_rater` à partir de **2,04 s** (6 s) | ✅ monté par Sofiane |
| 3 | Notif Snapchat de Quatrepixel « ton flyer est fini » + il poste en story | HyperFrames | ⏳ à faire |
| 4 | **Le zbeul** | Seedance (prompt ci-dessous) | ⏳ à générer |
| 5 | Il distribue les AirPods, billets dans les mains | `clip_2` de **6,83 s à la fin** (3,2 s) | ✅ gardé |
| 6 | Fin | à définir | ❓ |

Jeté : `clip_2_refais` (les bécanes écrasent le stock et continuent tout droit ;
la fin avec la foule cagoulée est bien mais casse la cohérence), et `clip_2` avant 6,83 s.

## Le zbeul : ce qu'on veut

- Les bécanes déboulent en roue arrière et **s'arrêtent devant lui**. Elles n'écrasent rien, ne repartent pas derrière.
- Des gens tombent du ciel en **parachutes noirs**.
- Il **se lève et lève les bras** (comme dans `clip_2_refais`), tout le monde vient vers lui.
- Jeunes de quartier : beaucoup cagoulés, beaucoup non, coupes dégradées, casquettes, survêts.
- Tout le monde crie, saute, se bat pour atteindre les cartons, prend les articles et **lui tend des billets**.
- Stock : AirPods, parfums, puffs, casquettes de luxe, sacoches de luxe.
- Doit finir serré sur lui entouré de mains, pour raccorder avec le plan AirPods (`references/raccord_airpods_debut.png`).

## Prompt Seedance

Pas encore écrit : on valide d'abord l'idée et la durée (skill pub-virale-seedance).
Le prompt sera en JSON, en français, sans secondes, et passera le garde-fou.

## Points à régler avant le prompt

- Durée (réglée) : clip_1 en x2 = 5 s, clip_1_rater en x1,25 = 4,8 s, Snap ~2,5 s, **zbeul ~7 s** (1 clip, 2-3 plans), AirPods 3,2 s, flyer ~2,5 s → ~25 s.
- Foule (validé) : surtout des cagoules, quelques visages pas vraiment nets, rendu réaliste. Un seul visage net : LE VENDEUR.
- Références : recadrer le logo « Ai » ; il faut un gros plan visage seul + une image en pied du VENDEUR, et un décor sans perso avec de la place devant le stand pour que les bécanes s'arrêtent.

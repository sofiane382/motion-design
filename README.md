# Motion Design — vidéos IA

Bibliothèque de prompts pour générer des vidéos de motion design avec des modèles
texte→vidéo et image→vidéo (Kling 3.0 Pro, MiniMax H3 Max, FLUX 3, Gemini Omni…),
utilisables dans FLORA, Higgsfield ou tout autre outil de génération.

## Structure

- `prompts/` — un fichier par catégorie de vidéo, chaque prompt prêt à copier.

| Catégorie | Fichier | Usage |
|---|---|---|
| Logo reveal | `prompts/01-logo-reveal.md` | Intros de marque, outros |
| Typographie cinétique | `prompts/02-typo-cinetique.md` | Titres, citations, réseaux sociaux |
| Produit 3D | `prompts/03-produit-3d.md` | Pubs e-commerce, packshots |
| Abstrait / boucles | `prompts/04-abstrait-boucles.md` | Fonds animés, visuels de scène |
| Transitions | `prompts/05-transitions.md` | Raccords entre plans |
| Pub virale / UGC | `prompts/06-pub-virale.md` | TikTok, Reels, Shorts |

## Conseils de prompt

1. **Sujet** — ce qui est à l'écran.
2. **Mouvement** — ce qui bouge et comment (morph, extrusion, rebond, éclatement).
3. **Caméra** — dolly in, orbite 180°, top-down, plan fixe.
4. **Style** — flat 2D, 3D clay, chrome, néon, papier découpé, isométrique.
5. **Lumière / couleurs** — palette précise (2–3 couleurs + fond).
6. **Rythme** — durée, easing (« ease-in-out », « snappy overshoot »), boucle parfaite ou non.

Format conseillé : 5 s, 16:9 pour YouTube, 9:16 pour Reels/TikTok, 1:1 pour le feed.

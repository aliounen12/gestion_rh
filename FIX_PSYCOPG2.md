# 🔧 Correction du problème psycopg2-binary sur Netlify

## ❌ Problème identifié

Netlify utilisait Python 3.14 par défaut, qui n'a pas de wheel précompilé pour `psycopg2-binary==2.9.9`. 
Pip essayait de compiler depuis la source mais `pg_config` n'était pas disponible.

**Erreur** :
```
Error: pg_config executable not found.
pg_config is required to build psycopg2 from source.
```

## ✅ Solution appliquée

### Option B : Utiliser Python 3.11.8

**Fichier créé** : `runtime.txt`
```
python-3.11.8
```

**Pourquoi Python 3.11.8 ?**
- Cette version a des wheels précompilés pour `psycopg2-binary==2.9.9`
- Pas besoin de compiler depuis la source
- Pas besoin d'installer `libpq-dev` dans le build

## 📋 Fichiers modifiés

- ✅ `runtime.txt` créé avec `python-3.11.8`
- ✅ `netlify.toml` mis à jour avec commentaire

## 🚀 Redéploiement

1. **Commiter les changements** :
   ```bash
   git add runtime.txt netlify.toml
   git commit -m "Fix: Use Python 3.11.8 for psycopg2-binary compatibility"
   git push
   ```

2. **Netlify redéploiera automatiquement**

3. **Vérifier les logs** :
   - Netlify Dashboard > "Deploys" > Votre déploiement
   - Vérifiez que Python 3.11.8 est utilisé
   - Vérifiez que `psycopg2-binary` s'installe correctement

## 🔍 Vérification

Après le déploiement, dans les logs vous devriez voir :
- Python 3.11.8 détecté depuis `runtime.txt`
- `psycopg2-binary` téléchargé comme wheel (pas de compilation)
- Installation réussie

## 💡 Alternative (si Python 3.11 ne fonctionne pas)

Si pour une raison quelconque Python 3.11 ne fonctionne pas, vous pouvez utiliser l'Option A :

**Modifier `netlify.toml`** :
```toml
[build]
  command = "apt-get update && apt-get install -y libpq-dev && python -m pip install -r requirements.txt && echo 'Build complete'"
  functions = "netlify/functions"
  publish = "."
```

Mais l'Option B (Python 3.11.8) est recommandée car plus simple et plus rapide.

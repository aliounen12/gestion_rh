import pandas as pd
import re

# Charger le fichier
df = pd.read_csv("C:/Users/LENOVO/Desktop/GestionRH/CodeCSV.csv", encoding="ISO-8859-1", sep=';')
df = df.dropna(how="all")
df.columns = ['Contenu'] + [f'Col_{i}' for i in range(1, len(df.columns))]
df = df[['Contenu']]
df['Contenu'] = df['Contenu'].astype(str).str.encode('latin1', errors='ignore').str.decode('latin1')
df['Contenu'] = df['Contenu'].str.replace(r'[\t\r\n]+', ' ', regex=True)
df['Contenu'] = df['Contenu'].str.strip()

# Extraire les articles
articles = []
current_article_number = None
current_article_contes
for line in df['Contenu']:
    match = re.match(r'^(Art\.L\.\d+)[\s\-–:.]*', line)
    if match:
        if current_article_number:
            articles.append({
                'Article': current_article_number,
                'Contenu': ' '.join(current_article_content).strip()
            })
        current_article_number = match.group(1)
        remaining = line.replace(current_article_number, '', 1).strip(" .:-–")
        current_article_content = [remaining]
    elif current_article_number:
        current_article_content.append(line)

# Ajouter le dernier article
if current_article_number:
    articles.append({
        'Article': current_article_number,
        'Contenu': ' '.join(current_article_content).strip()
    })

# DataFrame final
df_articles = pd.DataFrame(articles)
df_articles.to_csv("articles_structures.csv", index=False, encoding="utf-8")

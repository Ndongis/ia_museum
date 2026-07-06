
def build_text_bien(bien):

  text=f"""
Type de bien culturel: {bien.get('type','Aucun')}
Œuvre : {bien.get('titre','Aucun')}
Description : {bien.get('description','Aucun')}
Historique : {bien.get('historique','Aucun ')}
Technique : {bien.get('technique','')}
Sujet : {bien.get('sujet','Aucun')}
Inscription : {bien.get('inscription','')}
Auteur : {bien.get('auteur','Aucun')}
Contexte: c'est un bien culturel qui appartient à une institution

"""
  categories=bien.get('categories')
 # print(categories[0]["nom"])
  print(f"categorie {type(categories)}")
  if categories is not None :
    for categorie in categories:
      if type(categorie)!=str:
        text+=f"Categorie : {categorie.get('nom')}"
      break

  institution=None
  institution_id=bien.get("institution_id")

  if institution_id is not None:
    for inst in institutions:
        if inst.get("id") == institution_id:
            institution = inst
            text+=f" Institution : {institution.get("nom")}"
            break


  return text.strip()


def embed_biens(biens):
    texts = [build_text_bien(b) for b in biens]

    embeddings = model.encode(
        texts,
        batch_size=32,   # important pour performance
        show_progress_bar=True
    )

    return texts, embeddings

def insert_biens(biens):
    texts, embeddings = embed_biens(biens)

    for i, bien in enumerate(biens):
        print("embedding")
        cur.execute("""
            INSERT INTO rag_documents (content, embedding, metadata)
            VALUES (%s, %s, %s)
        """, (
            texts[i],
            embeddings[i].tolist(),
            json.dumps({
                "type": "bien",
                "id": bien.get("id"),
                "institution_id": bien.get("institution_id"),
                "artiste_id": bien.get("artiste_id"),
            })
        )),


    conn.commit()
print(data['biens'])
#insert_biens(data['biens'])ù

conn.rollback()

# ============================================================
# BUILD TEXT FUNCTIONS
# ============================================================

def build_text_categorie(item):
    text = f"""
Type: Catégorie
Nom : {item.get('nom', 'Aucun')}
Description : {item.get('description', 'Aucun')}
Contexte: C'est une catégorie de classification des biens culturels
"""
    return text.strip()

def embed_categories(items):
    texts = [build_text_categorie(i) for i in items]
    embeddings = EMBED.encode(texts, batch_size=32, show_progress_bar=True)
    return texts, embeddings

def insert_categories(items):
    texts, embeddings = embed_categories(items)
    for i, item in enumerate(items):
        print(f"embedding categorie {i+1}/{len(items)}")
        cur.execute("""
            INSERT INTO rag_documents (content, embedding, metadata)
            VALUES (%s, %s, %s)
        """, (
            texts[i],
            embeddings[i].tolist(),
            json.dumps({
                "type": "categorie",
                "id": item.get("id"),
            })
        ))
    conn.commit()
    print(f"✅ {len(items)} catégories insérées.")

#insert_categories(data['categories'])

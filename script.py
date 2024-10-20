import openai
import os
import time

# Load OpenAI API key from file
def load_api_key(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip().split('=')[1]

# Set OpenAI API keys
openai_api_key = load_api_key('/Users/simonazoulay/PBN-TEST/keys.txt')

# Create the OpenAI client
client = openai.Client(api_key=openai_api_key)

# Function to generate article titles based on history and destination
def generate_article_titles(history_context, destination_context, num_titles=10, temperature=0.3):
    prompt = f"""
    Ton objectif est de générer {num_titles} sujets d'articles pertinents. Ces articles doivent faire le lien entre l'historique du site {history_context} et son nouveau contexte {destination_context}. 
    
    C'est dans le contexte d'un rachat du nom de domaine {history_url} par {destination_url} -> tu pourras explorer ces urls pour te faire ton idée. Afin de conserver une cohérence entre l'ancien et le nouveau site, ton rôle est de trouver un "liant" le plus pertinent possible tout en ayant une approche originale. Tu te baseras sur l'ancrage (thématique et géogrpahique de {history_context} pour générer les sujets).
    
    - 80% des sujets doivent être étroitement liés entre Historique et Destination.
    - 20% des sujets doivent être plus transversaux, apportant une perspective plus générale ou alternative qui reste en lien indirect avec la destination.

    Ces articles doivent répondre aux préoccupations des lecteurs professionnels, avec une valeur ajoutée tangible dans les domaines économiques, juridiques ou organisationnels, tout en restant subtil dans l'évocation des services offerts par {destination_url}.
    
    Génère {num_titles} sujets d'articles uniques, granulaire et sans redondance.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un responsable éditorial spécialisé dans le domaine entrepreneurial et la création d'arborescence de sujets d'articles pertinents."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )

    # Extract individual titles from the response text
    titles = response.choices[0].message.content.strip().split('\n\n')
    return titles

# Function to generate HTML articles based on titles
def generate_article_html(title, global_context, temperature=0.3):
    prompt = f"""
    Rédige un article d'au moins 1900 mots sur le sujet suivant : "{title}". 

    {global_context}
    
    Cet article doit être structuré clairement avec une introduction percutante d'environ 60 mots (optimisée pour le SEO) en balise <h1>. Utilise des balises <h2> pour chaque section, en gardant des titres concis, explicites et optimisés pour le SEO (exemple : "Optimiser la gestion des flux financiers en PME"). 

    - Chaque section doit être informative, apportant une réelle valeur ajoutée au lecteur.
    - Les points essentiels doivent être mis en valeur avec des balises <strong>.
    - Le ton doit rester professionnel mais engageant.
    - Infonet ne doit pas être mentionné.

    La dernière section, en balise <h2>, doit offrir une perspective future ou une réflexion sans utiliser le mot "conclusion". 

    Termine l'article avec une balise <div>. L'ensemble de l'article doit rester lisible, bien structuré, avec au moins 1600 mots, et utiliser les balises HTML appropriées pour le formatage. Tu n'utiliseras pas de markdown et je n'ai pas besoin des en-têtes HTML (tu commences directement avec le <h1>).
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un expert rédacteur dans le monde de l'entreprise, et tu écris des articles de fond riches en informations."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )

    article_html = response.choices[0].message.content.strip()
    return article_html

# Save each article as a separate HTML file
def save_article_html(article_html, file_name):
    file_path = f"{file_name}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(article_html)

# Function to generate SEO optimizations based on title and first 500 words
def generate_seo_optimizations(title, first_500_words):
    # Prompt to generate SEO title
    seo_title_prompt = f"""
    En tant qu'expert SEO, génère un titre optimisé pour le SEO de moins de 42 caractères pour l'article suivant : "{title}". 

    Prends en compte les 500 premiers mots suivants pour optimiser le titre : {first_500_words}. N'ajoute aucun commentaire ou explication supplémentaire, retourne uniquement le titre.
    """

    response_title = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": seo_title_prompt}]
    )

    # Prompt to generate SEO description
    seo_description_prompt = f"""
    Génère une description SEO optimisée de moins de 126 caractères pour l'article suivant : "{title}". Utilise les 500 premiers mots suivants pour t'assurer que la description soit pertinente et reflète bien le contenu.

    Ne renvoie que la description sans commentaire ou explication supplémentaire.
    """

    response_description = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": seo_description_prompt}]
    )

    # Clean and return results
    seo_title = response_title.choices[0].message.content.strip().replace('"', '')
    seo_description = response_description.choices[0].message.content.strip()

    return seo_title, seo_description

# Insert SEO metadata into the article HTML
def insert_seo_metadata(article_html, seo_title, seo_description):
    meta_data = f'<meta name="description" content="{seo_description}">\n<title>{seo_title}</title>\n'
    updated_html = meta_data + article_html
    return updated_html

# Main function to process the articles, one iteration per article to ensure more tokens and context
def process_articles(history_context, destination_context, global_context, num_articles=10):
    # Generate titles for all articles once and store them
    titles = generate_article_titles(history_context, destination_context, num_articles)

    for i, title in enumerate(titles, 1):  # One loop with proper article index
        try:
            # Generate the article
            article_html = generate_article_html(title, global_context)

            # Extract the first 500 words for SEO optimization
            first_500_words = ' '.join(article_html.split()[:500])

            # Generate SEO title and description based on the title and first 500 words
            seo_title, seo_description = generate_seo_optimizations(title, first_500_words)
            article_with_seo = insert_seo_metadata(article_html, seo_title, seo_description)

            # Save the article with SEO metadata
            file_name = f"article-{i}"
            save_article_html(article_with_seo, file_name)

            # Pause to avoid API rate limits
            time.sleep(1)
        except Exception as e:
            print(f"Erreur lors de la génération de l'article {i}: {e}")
            continue  # Continue with the next article if an error occurs

# Example usage
if __name__ == "__main__":
    history_url = "https://web.archive.org/web/20210614032815/https://www.courants-porteurs.com/"
    history_context = "Un réseau professionnel, ancré sur le territoire(Finitère) depuis 2004. Un repère et une force vive pour les indépendants, TPE, PME. Il permet de contribuer à une dynamique de territoire, trouver des appuis, du conseil pour chercher avec vous les solutions et les partenaires dont vous avez besoin pour faire grandir votre entreprise."
    destination_url = "https://infonet.fr/"
    destination_context = """Un site d'information légale et financière, et plus précisément ici, pousser des landings comme :
    - Accord d'entreprise
    - Actes
    - Actionnaires et Filiales
    - Analyse financière
    - Annonces BODACC
    - Annonces légales
    - Avis de situation SIRENE
    - Bilan financier
    - Brevet
    - Code APE
    - Comptes annuels
    - Contacts entreprises
    - Contacts salariés
    - Convention collective
    - Cotation Banque de France
    - Diagnostic AFDCC
    - Diagnostic NOTA-PME
    - Encours financier
    - Étude de solvabilité
    - Extrait d'immatriculation
    - Extrait RNE
    - Fiche entreprise
    - Justificatif d’immatriculation
    - Kbis
    - Marques
    - Numéro de TVA intracommunautaire
    - Numéro DUNS
    - Numéro EORI
    - Procédures collectives
    - RCS
    - SIREN / SIRET
    - Statuts (pour télécharger des documents officiels)
    
    Infonet permet de vérifier la santé financière et juridique de vos clients, fournisseurs et partenaires. Infonet vous dévoile toute la vérité sur votre réseau professionnel et son marché.
    """
    # Global context for all articles to ensure coherence and avoid redundancy
    global_context = "Tous les articles doivent être cohérents entre eux et éviter les redondances, tout en maintenant une perspective unique pour chaque sujet traité. Ils doivent refléter une analyse fine du marché et des services proposés par Infonet."

    process_articles(history_context, destination_context, global_context, num_articles=10)

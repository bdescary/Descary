#!/usr/bin/env python3
"""
Exemple avancé d'utilisation du Google Business Reviews Scraper
Inclut des analyses statistiques et des exports multiples
"""

from google_business_scraper import GoogleBusinessScraper
import pandas as pd
from datetime import datetime
import os


def analyze_reviews(reviews_data):
    """
    Analyse détaillée des reviews

    Args:
        reviews_data: Liste des reviews

    Returns:
        Dictionnaire avec les statistiques
    """
    if not reviews_data:
        print("❌ Aucune review à analyser")
        return None

    df = pd.DataFrame(reviews_data)

    # Statistiques de base
    stats = {
        'total_reviews': len(df),
        'avg_rating': df['note'].mean(),
        'median_rating': df['note'].median(),
        'min_rating': df['note'].min(),
        'max_rating': df['note'].max(),
        'avg_sentiment': df['sentiment_score'].mean(),
    }

    # Distribution des notes
    rating_distribution = df['note'].value_counts().sort_index()
    stats['rating_distribution'] = rating_distribution.to_dict()

    # Distribution des sentiments
    sentiment_distribution = df['sentiment'].value_counts()
    stats['sentiment_distribution'] = sentiment_distribution.to_dict()

    # Pourcentage de reviews positives (4-5 étoiles)
    positive_reviews = len(df[df['note'] >= 4])
    stats['positive_percentage'] = (positive_reviews / stats['total_reviews']) * 100

    # Pourcentage de reviews négatives (1-2 étoiles)
    negative_reviews = len(df[df['note'] <= 2])
    stats['negative_percentage'] = (negative_reviews / stats['total_reviews']) * 100

    # Reviews avec commentaires
    reviews_with_text = len(df[df['commentaire'] != ''])
    stats['reviews_with_text'] = reviews_with_text
    stats['text_percentage'] = (reviews_with_text / stats['total_reviews']) * 100

    # Longueur moyenne des commentaires
    df['comment_length'] = df['commentaire'].str.len()
    stats['avg_comment_length'] = df['comment_length'].mean()

    return stats


def print_detailed_report(stats):
    """
    Affiche un rapport détaillé des statistiques

    Args:
        stats: Dictionnaire des statistiques
    """
    print("\n" + "="*70)
    print("📊 RAPPORT DÉTAILLÉ DES REVIEWS")
    print("="*70)

    print(f"\n📈 STATISTIQUES GÉNÉRALES")
    print(f"  Total de reviews: {stats['total_reviews']}")
    print(f"  Reviews avec commentaire: {stats['reviews_with_text']} ({stats['text_percentage']:.1f}%)")
    print(f"  Longueur moyenne des commentaires: {stats['avg_comment_length']:.0f} caractères")

    print(f"\n⭐ NOTES")
    print(f"  Note moyenne: {stats['avg_rating']:.2f}/5")
    print(f"  Note médiane: {stats['median_rating']:.0f}/5")
    print(f"  Note minimale: {stats['min_rating']:.0f}/5")
    print(f"  Note maximale: {stats['max_rating']:.0f}/5")

    print(f"\n📊 DISTRIBUTION DES NOTES")
    for rating in sorted(stats['rating_distribution'].keys(), reverse=True):
        count = stats['rating_distribution'][rating]
        percentage = (count / stats['total_reviews']) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {rating}⭐: {bar} {count} ({percentage:.1f}%)")

    print(f"\n😊 SENTIMENTS")
    print(f"  Score de sentiment moyen: {stats['avg_sentiment']:.3f}")
    print(f"  Reviews positives (4-5⭐): {stats['positive_percentage']:.1f}%")
    print(f"  Reviews négatives (1-2⭐): {stats['negative_percentage']:.1f}%")

    print(f"\n📈 DISTRIBUTION DES SENTIMENTS")
    for sentiment, count in sorted(stats['sentiment_distribution'].items(),
                                   key=lambda x: x[1], reverse=True):
        percentage = (count / stats['total_reviews']) * 100
        print(f"  {sentiment}: {count} ({percentage:.1f}%)")

    print("\n" + "="*70)


def export_filtered_reviews(df, scraper, base_filename):
    """
    Exporte les reviews filtrées par catégories

    Args:
        df: DataFrame pandas avec les reviews
        scraper: Instance du scraper
        base_filename: Nom de base pour les fichiers
    """
    # Créer un dossier exports si nécessaire
    os.makedirs('exports', exist_ok=True)

    # Reviews positives (4-5 étoiles)
    positive = df[df['note'] >= 4]
    if len(positive) > 0:
        filename = f"exports/{base_filename}_positives.csv"
        scraper.export_to_csv(positive.to_dict('records'), filename)
        print(f"✅ {len(positive)} reviews positives → {filename}")

    # Reviews négatives (1-2 étoiles)
    negative = df[df['note'] <= 2]
    if len(negative) > 0:
        filename = f"exports/{base_filename}_negatives.csv"
        scraper.export_to_csv(negative.to_dict('records'), filename)
        print(f"✅ {len(negative)} reviews négatives → {filename}")

    # Reviews neutres (3 étoiles)
    neutral = df[df['note'] == 3]
    if len(neutral) > 0:
        filename = f"exports/{base_filename}_neutres.csv"
        scraper.export_to_csv(neutral.to_dict('records'), filename)
        print(f"✅ {len(neutral)} reviews neutres → {filename}")

    # Reviews avec sentiment très positif
    very_positive_sentiment = df[df['sentiment'] == 'Très Positif']
    if len(very_positive_sentiment) > 0:
        filename = f"exports/{base_filename}_sentiment_tres_positif.csv"
        scraper.export_to_csv(very_positive_sentiment.to_dict('records'), filename)
        print(f"✅ {len(very_positive_sentiment)} reviews (sentiment très positif) → {filename}")

    # Reviews avec sentiment très négatif
    very_negative_sentiment = df[df['sentiment'] == 'Très Négatif']
    if len(very_negative_sentiment) > 0:
        filename = f"exports/{base_filename}_sentiment_tres_negatif.csv"
        scraper.export_to_csv(very_negative_sentiment.to_dict('records'), filename)
        print(f"✅ {len(very_negative_sentiment)} reviews (sentiment très négatif) → {filename}")


def main():
    """Fonction principale pour l'exemple avancé"""

    print("="*70)
    print("🚀 GOOGLE BUSINESS REVIEWS SCRAPER - MODE AVANCÉ")
    print("="*70)

    # Configuration
    business_name = input("\n📍 Entrez le nom du business (ex: 'Café Olimpico Montreal'): ").strip()

    if not business_name:
        print("❌ Nom du business requis")
        return

    max_reviews = input("📊 Nombre maximum de reviews (par défaut: 100): ").strip()
    max_reviews = int(max_reviews) if max_reviews else 100

    headless = input("🖥️  Mode headless (masquer le navigateur)? (O/n): ").strip().lower()
    headless = headless != 'n'

    # Créer le scraper
    print(f"\n🔧 Initialisation du scraper...")
    scraper = GoogleBusinessScraper(headless=headless)

    try:
        # Scraper les reviews
        print(f"🔍 Récupération des reviews pour '{business_name}'...")
        reviews = scraper.scrape_reviews(
            search_query=business_name,
            max_reviews=max_reviews
        )

        if not reviews:
            print("❌ Aucune review trouvée. Vérifiez le nom du business.")
            return

        # Convertir en DataFrame pour analyse
        df = pd.DataFrame(reviews)

        # Créer un nom de fichier basé sur le business et la date
        safe_business_name = "".join(c for c in business_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_business_name = safe_business_name.replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{safe_business_name}_{timestamp}"

        # Export complet
        os.makedirs('exports', exist_ok=True)
        main_filename = f"exports/{base_filename}_complet.csv"
        scraper.export_to_csv(reviews, main_filename)
        print(f"\n📁 Export complet → {main_filename}")

        # Exporter les reviews filtrées
        print(f"\n📂 Création des exports filtrés...")
        export_filtered_reviews(df, scraper, base_filename)

        # Analyser les reviews
        print(f"\n🔬 Analyse des reviews...")
        stats = analyze_reviews(reviews)

        if stats:
            # Afficher le rapport détaillé
            print_detailed_report(stats)

            # Top 5 meilleures reviews
            print("\n🌟 TOP 5 MEILLEURES REVIEWS (par sentiment)")
            print("-"*70)
            top_reviews = df.nlargest(5, 'sentiment_score')
            for idx, row in top_reviews.iterrows():
                print(f"\n{row['auteur']} - {row['note']}⭐ - Score: {row['sentiment_score']:.3f}")
                comment = row['commentaire'][:150]
                if len(row['commentaire']) > 150:
                    comment += "..."
                print(f"  \"{comment}\"")

            # Top 5 pires reviews
            if len(df[df['note'] <= 3]) > 0:
                print("\n⚠️  TOP 5 PIRES REVIEWS (par sentiment)")
                print("-"*70)
                worst_reviews = df.nsmallest(5, 'sentiment_score')
                for idx, row in worst_reviews.iterrows():
                    print(f"\n{row['auteur']} - {row['note']}⭐ - Score: {row['sentiment_score']:.3f}")
                    comment = row['commentaire'][:150]
                    if len(row['commentaire']) > 150:
                        comment += "..."
                    print(f"  \"{comment}\"")

            # Sauvegarder les statistiques
            stats_filename = f"exports/{base_filename}_statistiques.txt"
            with open(stats_filename, 'w', encoding='utf-8') as f:
                f.write(f"RAPPORT D'ANALYSE - {business_name}\n")
                f.write(f"Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*70 + "\n\n")
                f.write(f"Total de reviews: {stats['total_reviews']}\n")
                f.write(f"Note moyenne: {stats['avg_rating']:.2f}/5\n")
                f.write(f"Sentiment moyen: {stats['avg_sentiment']:.3f}\n")
                f.write(f"Reviews positives: {stats['positive_percentage']:.1f}%\n")
                f.write(f"Reviews négatives: {stats['negative_percentage']:.1f}%\n")

            print(f"\n📄 Statistiques sauvegardées → {stats_filename}")

        print("\n" + "="*70)
        print("✅ ANALYSE TERMINÉE AVEC SUCCÈS!")
        print("="*70)

    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

    finally:
        scraper.close()
        print("\n👋 Au revoir!")


if __name__ == "__main__":
    main()

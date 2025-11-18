#!/usr/bin/env python3
"""
Google Business Profile Reviews Scraper
Récupère les commentaires, notes et sentiments d'une fiche Google Business Profile
"""

import time
import re
from datetime import datetime
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
from sentiment_analyzer import SentimentAnalyzer


class GoogleBusinessScraper:
    """Scraper pour les reviews Google Business Profile"""

    def __init__(self, headless: bool = True):
        """
        Initialise le scraper

        Args:
            headless: Si True, le navigateur s'exécute en arrière-plan
        """
        self.headless = headless
        self.driver = None
        self.sentiment_analyzer = SentimentAnalyzer()

    def setup_driver(self):
        """Configure le driver Selenium"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

    def close(self):
        """Ferme le navigateur"""
        if self.driver:
            self.driver.quit()

    def get_business_url(self, place_id: str = None, search_query: str = None) -> str:
        """
        Génère l'URL Google Maps pour un business

        Args:
            place_id: L'ID Google Place du business
            search_query: Requête de recherche (nom + adresse du business)

        Returns:
            URL Google Maps
        """
        if place_id:
            return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        elif search_query:
            return f"https://www.google.com/maps/search/{search_query}"
        else:
            raise ValueError("Vous devez fournir soit un place_id soit une search_query")

    def scroll_reviews(self, max_scrolls: int = 10):
        """
        Fait défiler la section des reviews pour charger plus de commentaires

        Args:
            max_scrolls: Nombre maximum de défilements
        """
        try:
            # Trouver le conteneur scrollable des reviews
            scrollable_div = self.driver.find_element(
                By.CSS_SELECTOR,
                'div[role="main"]'
            )

            last_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", scrollable_div
            )

            scrolls = 0
            while scrolls < max_scrolls:
                # Scroll vers le bas
                self.driver.execute_script(
                    "arguments[0].scrollTo(0, arguments[0].scrollHeight)",
                    scrollable_div
                )

                time.sleep(2)

                # Calculer la nouvelle hauteur
                new_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight", scrollable_div
                )

                if new_height == last_height:
                    break

                last_height = new_height
                scrolls += 1

        except Exception as e:
            print(f"Erreur lors du défilement: {e}")

    def click_all_more_buttons(self):
        """Clique sur tous les boutons 'Plus' pour développer les reviews"""
        try:
            more_buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                'button[aria-label*="Plus"]'
            )

            for button in more_buttons:
                try:
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(0.5)
                except:
                    continue

        except Exception as e:
            print(f"Erreur lors du clic sur les boutons 'Plus': {e}")

    def extract_rating(self, review_element) -> Optional[int]:
        """
        Extrait la note d'une review

        Args:
            review_element: Élément Selenium de la review

        Returns:
            Note sur 5 ou None
        """
        try:
            rating_element = review_element.find_element(
                By.CSS_SELECTOR,
                'span[role="img"]'
            )
            aria_label = rating_element.get_attribute('aria-label')

            # Extraire le nombre d'étoiles
            match = re.search(r'(\d+)', aria_label)
            if match:
                return int(match.group(1))

        except NoSuchElementException:
            pass

        return None

    def extract_review_text(self, review_element) -> str:
        """
        Extrait le texte d'une review

        Args:
            review_element: Élément Selenium de la review

        Returns:
            Texte de la review
        """
        try:
            text_element = review_element.find_element(
                By.CSS_SELECTOR,
                'span.wiI7pd'
            )
            return text_element.text.strip()
        except NoSuchElementException:
            return ""

    def extract_reviewer_name(self, review_element) -> str:
        """
        Extrait le nom de l'auteur de la review

        Args:
            review_element: Élément Selenium de la review

        Returns:
            Nom de l'auteur
        """
        try:
            name_element = review_element.find_element(
                By.CSS_SELECTOR,
                'div.d4r55'
            )
            return name_element.text.strip()
        except NoSuchElementException:
            return "Anonyme"

    def extract_review_date(self, review_element) -> str:
        """
        Extrait la date de la review

        Args:
            review_element: Élément Selenium de la review

        Returns:
            Date de la review
        """
        try:
            date_element = review_element.find_element(
                By.CSS_SELECTOR,
                'span.rsqaWe'
            )
            return date_element.text.strip()
        except NoSuchElementException:
            return ""

    def scrape_reviews(
        self,
        place_id: str = None,
        search_query: str = None,
        max_reviews: int = 100
    ) -> List[Dict]:
        """
        Scrape les reviews d'un Google Business Profile

        Args:
            place_id: L'ID Google Place du business
            search_query: Requête de recherche (nom + adresse du business)
            max_reviews: Nombre maximum de reviews à récupérer

        Returns:
            Liste de dictionnaires contenant les informations des reviews
        """
        if not self.driver:
            self.setup_driver()

        url = self.get_business_url(place_id, search_query)
        print(f"Accès à l'URL: {url}")

        self.driver.get(url)
        time.sleep(3)

        try:
            # Cliquer sur l'onglet "Avis" si disponible
            reviews_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@aria-label, 'Avis') or contains(., 'Reviews')]")
                )
            )
            reviews_tab.click()
            time.sleep(2)
        except TimeoutException:
            print("Onglet Avis non trouvé, tentative de scraping direct...")

        # Faire défiler pour charger plus de reviews
        print("Chargement des reviews...")
        self.scroll_reviews(max_scrolls=max_reviews // 10)

        # Développer toutes les reviews
        print("Développement des reviews complètes...")
        self.click_all_more_buttons()

        # Extraire les reviews
        print("Extraction des reviews...")
        reviews_data = []

        try:
            review_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                'div.jftiEf'
            )

            print(f"Nombre de reviews trouvées: {len(review_elements)}")

            for idx, review_element in enumerate(review_elements[:max_reviews]):
                try:
                    reviewer_name = self.extract_reviewer_name(review_element)
                    rating = self.extract_rating(review_element)
                    review_text = self.extract_review_text(review_element)
                    review_date = self.extract_review_date(review_element)

                    # Analyser le sentiment
                    sentiment_score, sentiment_label = self.sentiment_analyzer.analyze(review_text)

                    review_data = {
                        'id': idx + 1,
                        'auteur': reviewer_name,
                        'note': rating,
                        'date': review_date,
                        'commentaire': review_text,
                        'sentiment_score': sentiment_score,
                        'sentiment': sentiment_label
                    }

                    reviews_data.append(review_data)

                    print(f"Review {idx + 1}: {reviewer_name} - {rating}⭐ - {sentiment_label}")

                except Exception as e:
                    print(f"Erreur lors de l'extraction de la review {idx + 1}: {e}")
                    continue

        except Exception as e:
            print(f"Erreur lors de la recherche des reviews: {e}")

        return reviews_data

    def export_to_csv(
        self,
        reviews_data: List[Dict],
        filename: str = None
    ) -> str:
        """
        Exporte les reviews en CSV

        Args:
            reviews_data: Liste des reviews
            filename: Nom du fichier CSV (optionnel)

        Returns:
            Nom du fichier créé
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"google_reviews_{timestamp}.csv"

        if not filename.endswith('.csv'):
            filename += '.csv'

        if not reviews_data:
            print("Aucune review à exporter")
            return filename

        # Écrire le CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'auteur', 'note', 'date', 'commentaire',
                         'sentiment_score', 'sentiment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(reviews_data)

        print(f"\n✅ Export réussi: {filename}")
        print(f"📊 Nombre de reviews exportées: {len(reviews_data)}")

        return filename


def main():
    """Fonction principale pour tester le scraper"""

    # Exemple d'utilisation
    scraper = GoogleBusinessScraper(headless=False)

    try:
        # Option 1: Utiliser un place_id
        # reviews = scraper.scrape_reviews(place_id="ChIJN1t_tDeuEmsRUsoyG83frY4")

        # Option 2: Utiliser une recherche
        search_query = input("Entrez le nom et l'adresse du business (ex: 'Restaurant ABC Montreal'): ")

        max_reviews = int(input("Nombre maximum de reviews à récupérer (ex: 50): ") or "50")

        reviews = scraper.scrape_reviews(
            search_query=search_query,
            max_reviews=max_reviews
        )

        if reviews:
            # Exporter en CSV
            filename = scraper.export_to_csv(reviews)

            # Afficher un résumé
            print("\n" + "="*60)
            print("RÉSUMÉ DES REVIEWS")
            print("="*60)

            total_reviews = len(reviews)
            avg_rating = sum(r['note'] for r in reviews if r['note']) / total_reviews

            sentiments = {}
            for review in reviews:
                sentiment = review['sentiment']
                sentiments[sentiment] = sentiments.get(sentiment, 0) + 1

            print(f"Total de reviews: {total_reviews}")
            print(f"Note moyenne: {avg_rating:.2f} ⭐")
            print(f"\nRépartition des sentiments:")
            for sentiment, count in sentiments.items():
                percentage = (count / total_reviews) * 100
                print(f"  {sentiment}: {count} ({percentage:.1f}%)")

        else:
            print("❌ Aucune review n'a pu être récupérée")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

    finally:
        scraper.close()


if __name__ == "__main__":
    main()

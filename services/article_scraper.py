import trafilatura


class ArticleScraper:
    """
    Robust article text extractor using trafilatura.
    Works on JS-heavy and protected news sites.
    """

    def fetch_article_text(self, source_url: str):
        """
        Download and extract clean article content.
        """

        try:
            downloaded = trafilatura.fetch_url(source_url)

            if not downloaded:
                return None

            extracted_text = trafilatura.extract(downloaded)

            if not extracted_text or len(extracted_text) < 200:
                return None

            return extracted_text

        except Exception as error:
            print(f"Article extraction failed: {error}")
            return None

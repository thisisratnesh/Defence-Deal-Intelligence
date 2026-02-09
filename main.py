# -------------------- Imports --------------------
from datetime import datetime

from services.gnews_fetcher import GNewsFetcher
from services.keyword_engine import KeywordEngine
from services.deal_classifier import DealClassifier
from services.ollama_llm_extractor import OllamaLLMExtractor
from utils.json_parser import parse_llm_json

from services.csv_storage_writer import CSVStorageWriter
from services.database_storage_writer import DatabaseStorageWriter

from services.multi_query_fetcher import MultiQueryFetcher
from utils.confidence_scorer import ConfidenceScorer
from utils.value_quantity_normalizer import ValueQuantityNormalizer

from utils.deal_deduplicator import DealDeduplicator






# -------------------- Main Pipeline --------------------

def main():
    """
    Defense deal intelligence pipeline using GNews full article content
    and local Ollama LLM extraction.
    """

    # Capture pipeline run time
    pipeline_run_timestamp = datetime.utcnow().isoformat()

    # ---------- STEP 1: Initialize services ----------


    GNEWS_API_KEY = "69872e57ea29b49a4a49dbae78677d5e"

    news_fetcher = GNewsFetcher(
        api_key=GNEWS_API_KEY
    )

    llm_extractor = OllamaLLMExtractor(
        model_name="llama3"
    )

    # ---------- STEP 2: Keyword groups ----------

    product_keywords = [
        "drone",
        "uav",
        "counter drone",
        "unmanned vehicle",
        "CUAS"
    ]

    deal_keywords = [
        "contract",
        "deal",
        "procurement",
        "order",
        "awarded",
        "signed"
    ]

    context_keywords = [
        "military",
        "army",
        "defense",
        "navy",
        "air force"
    ]

    # ---------- STEP 3: Engines ----------

    keyword_engine = KeywordEngine(
        product_keywords=product_keywords,
        deal_keywords=deal_keywords,
        context_keywords=context_keywords
    )

    deal_classifier = DealClassifier(
        score_threshold=3
    )

    # ---------- STEP 4: Multi-query deal fetch ----------

    queries = [
        "defense company secured contract",
        "military procurement order awarded",
        "arms manufacturer won deal",
        "drone company signed agreement army",
        "defense firm to supply systems",
        "military modernization contract",
        "government defense contract awarded",
    ]

    multi_fetcher = MultiQueryFetcher(news_fetcher)

    raw_articles = multi_fetcher.fetch_from_queries(
        queries=queries,
        max_per_query=5
    )

    print(f"Raw fetched from multi-query: {len(raw_articles)}")

    # ---------- STEP 5: Keyword filtering ----------

    keyword_filtered_articles =  raw_articles

    print(f"After keyword filter: {len(keyword_filtered_articles)}")

    # ---------- STEP 6: Deal classification ----------

    deal_articles = deal_classifier.filter_deal_articles(
        keyword_filtered_articles
    )

    print(f"Confirmed deal articles: {len(deal_articles)}")

    if deal_articles:
        print(deal_articles[0]["title"])

    # ---------- STEP 7: Ollama extraction ----------

    structured_deals = []

    for article in deal_articles:

        article_text = article.get("content", "")

        if not article_text:
            continue

        raw_llm_output = llm_extractor.extract_json(
            article_text
        )

        structured_deal = parse_llm_json(raw_llm_output)

        if structured_deal:
            # Initialize confidence scorer
            confidence_scorer = ConfidenceScorer()

            # Calculate confidence score
            confidence_value = confidence_scorer.calculate_confidence(structured_deal)

            # Initialize normalizer
            value_quantity_normalizer = ValueQuantityNormalizer()

            # Normalize deal value
            normalized_deal_value = value_quantity_normalizer.normalize_deal_value(
                structured_deal.get("deal_value"),
                structured_deal.get("currency")
            )

            # Normalize quantity
            normalized_quantity = value_quantity_normalizer.normalize_quantity(
                structured_deal.get("quantity")
            )

            # Attach normalized fields
            structured_deal["deal_value_normalized"] = normalized_deal_value
            structured_deal["quantity_normalized"] = normalized_quantity

            # Attach confidence and source
            structured_deal["confidence"] = confidence_value
            structured_deal["source_url"] = article.get("url")
            structured_deal["ingestion_timestamp"] = pipeline_run_timestamp

            # Append to final list
            structured_deals.append(structured_deal)

    # Initialize deduplicator
    deal_deduplicator = DealDeduplicator()

    # Remove duplicate deals
    deduplicated_deals = deal_deduplicator.deduplicate_deals(structured_deals)

    print(f"Structured deals extracted: {len(structured_deals)}")
    print(f"After deduplication: {len(deduplicated_deals)}")

    # Use deduplicated list for storage
    structured_deals = deduplicated_deals

    if structured_deals:
        print(structured_deals[0])

    # ---------- STEP 8: Store CSV ----------

    csv_storage_writer = CSVStorageWriter(
        file_path="deals_database.csv"
    )

    csv_storage_writer.save_structured_deals(
        structured_deals
    )

    print("Stored in CSV successfully.")

    # ---------- STEP 9: Store database ----------

    database_storage_writer = DatabaseStorageWriter(
        database_path="deals_database.db"
    )

    database_storage_writer.save_structured_deals(
        structured_deals
    )

    print("Stored in SQLite successfully.")


# -------------------- Entry Point --------------------

if __name__ == "__main__":
    main()

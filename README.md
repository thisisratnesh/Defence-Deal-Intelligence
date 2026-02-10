# Defence-Deal-Intelligence
#System Architecture

The Defence Deal Intelligence system is designed as a modular, multi-stage pipeline that progressively filters, understands, and structures defence procurement information from large volumes of news data.

High-level architecture:

News APIs (GNews)
        ↓
Multi-Query Fetch Layer
        ↓
Relevance Filtering (Keywords + Classifier)
        ↓
LLM-based Deal Extraction (Local LLM)
        ↓
Normalization (Value & Quantity)
        ↓
Confidence Scoring
        ↓
Duplicate Deal Merging
        ↓
Structured Storage (CSV / SQLite)

# Pipeline Flow

1. Multi-query news fetching retrieves high-signal defence-related articles.
2. Keyword relevance filtering removes unrelated news.
3. Deal classifier scores articles for contract likelihood.
4. Full article content is processed by a local LLM for structured extraction.
5. Financial values and quantities are normalized into machine-readable form.
6. Confidence scoring evaluates extraction reliability.
7. Duplicate deals are merged using semantic keys.
8. Clean structured data is stored in CSV and SQLite for analysis.


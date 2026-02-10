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

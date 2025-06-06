"""
Configuration for Research Q/A Bot
"""

class AppConfig:
    """Main application settings"""
    
    # LlamaCloud settings
    INDEX_NAME = "Arxiv 2024-2025. Key: Volatility / Parsing Preset: Balanced, Chunk size: 256, Chunk Overlap: 50"
    PROJECT_NAME = "Default"
    ORGANIZATION_ID = "858afa1e-d3dc-4a96-8783-d4f3798b0643"
    
    # OpenAI settings
    DEFAULT_MODEL = "gpt-4o-mini"  # More cost-effective model for MVP
    DEFAULT_TEMPERATURE = 0.2  # Low temperature for precise answers
    MAX_TOKENS = 1000  # Maximum tokens in response
    
    # Search settings
    DEFAULT_TOP_K = 3  # Default number of documents to retrieve
    MIN_SIMILARITY_SCORE = 0.1  # Minimum relevance threshold
    
    # UI settings
    MAX_QUERY_LENGTH = 500  # Maximum query length
    MIN_QUERY_LENGTH = 10   # Minimum query length
    
    # Prompts
    SYSTEM_PROMPT = """
    You are an expert research analyst specializing in academic paper analysis.
    
    Your task:
    1. Analyze provided scientific paper fragments
    2. Give accurate, fact-based answers to user questions
    3. Cite specific sources of information
    4. If information is insufficient - honestly state this
    
    Rules:
    - Answer only based on provided context
    - Do not make up information
    - Structure answers logically
    - Use scientific terminology
    - Be concise but informative
    """
    
    QUERY_PROMPT_TEMPLATE = """
    Context from scientific papers:
    {context}
    
    User question: {query}
    
    Analyze the provided context and answer the question. If there is insufficient information in the context for a complete answer, indicate this and answer based on available data.
    
    Structure your answer as follows:
    1. Brief direct answer to the question
    2. Detailed explanation with facts from sources
    3. If there are data limitations - specify them
    
    Answer:
    """
    
    # User messages
    MESSAGES = {
        "no_results": "No results found for your query. Try rephrasing your question or using different keywords.",
        "processing": "Processing your request...",
        "error_general": "An error occurred while processing the request. Please try again.",
        "error_api": "API error. Please check your access key settings.",
        "query_too_short": "Query too short. Please formulate a more detailed question.",
        "query_too_long": "Query too long. Please shorten your request."
    }
    
    # Example queries to help users
    EXAMPLE_QUERIES = [
        "What methods are used for volatility analysis in financial markets?",
        "What are GARCH models and how are they applied?",
        "What factors influence stock volatility?",
        "Compare different approaches to volatility forecasting",
        "What metrics are used to assess portfolio risk?",
        "How do neural networks perform in volatility prediction?",
        "What is the relationship between market microstructure and volatility?",
        "Describe the main volatility clustering phenomena"
    ]
    
    # Caching settings (for future use)
    CACHE_TTL = 3600  # Cache lifetime in seconds (1 hour)
    ENABLE_CACHING = True
    
    # Limits
    MAX_DAILY_REQUESTS = 100  # Maximum requests per day
    REQUEST_TIMEOUT = 30  # API request timeout in seconds
    
    # Response formatting
    MAX_RESPONSE_LENGTH = 2000  # Maximum response length in characters
    
    # Metadata fields to display
    METADATA_FIELDS = [
        'file_name',
        'page_label', 
        'title',
        'author',
        'creation_date',
        'document_type'
    ]
    
    # Error handling
    MAX_RETRIES = 3  # Maximum number of retries for failed requests
    RETRY_DELAY = 1  # Delay between retries in seconds

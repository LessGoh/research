"""
Utility functions for Research Q/A Bot
"""

import streamlit as st
from typing import List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime
import time

# LlamaIndex imports
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import NodeWithScore

from config import AppConfig

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_resource
def initialize_llamacloud_index() -> LlamaCloudIndex:
    """
    Initialize LlamaCloud index with caching
    
    Returns:
        LlamaCloudIndex: Initialized index
    """
    try:
        llamacloud_api_key = st.secrets["api_keys"]["llamacloud_api_key"]
        
        index = LlamaCloudIndex(
            name=AppConfig.INDEX_NAME,
            project_name=AppConfig.PROJECT_NAME,
            organization_id=AppConfig.ORGANIZATION_ID,
            api_key=llamacloud_api_key,
        )
        
        logger.info("LlamaCloud index successfully initialized")
        return index
        
    except Exception as e:
        logger.error(f"Error initializing LlamaCloud index: {e}")
        raise e

def initialize_openai_llm(temperature: float = AppConfig.DEFAULT_TEMPERATURE) -> OpenAI:
    """
    Initialize OpenAI LLM
    
    Args:
        temperature: Temperature for response generation
        
    Returns:
        OpenAI: Initialized model
    """
    try:
        openai_api_key = st.secrets["api_keys"]["openai_api_key"]
        
        llm = OpenAI(
            model=AppConfig.DEFAULT_MODEL,
            temperature=temperature,
            max_tokens=AppConfig.MAX_TOKENS,
            api_key=openai_api_key,
            system_prompt=AppConfig.SYSTEM_PROMPT
        )
        
        logger.info(f"OpenAI LLM initialized with model {AppConfig.DEFAULT_MODEL}")
        return llm
        
    except Exception as e:
        logger.error(f"Error initializing OpenAI LLM: {e}")
        raise e

def search_knowledge_base(
    index: LlamaCloudIndex, 
    query: str, 
    top_k: int = AppConfig.DEFAULT_TOP_K
) -> List[NodeWithScore]:
    """
    Search for relevant documents in knowledge base
    
    Args:
        index: LlamaCloud index
        query: Search query
        top_k: Number of documents to return
        
    Returns:
        List[NodeWithScore]: List of found documents with scores
    """
    try:
        logger.info(f"Performing search for query: '{query}' (top_k={top_k})")
        
        # Get retriever
        retriever = index.as_retriever(similarity_top_k=top_k)
        
        # Perform search
        nodes = retriever.retrieve(query)
        
        # Filter by minimum relevance threshold
        filtered_nodes = [
            node for node in nodes 
            if node.score >= AppConfig.MIN_SIMILARITY_SCORE
        ]
        
        logger.info(f"Found {len(filtered_nodes)} relevant documents")
        return filtered_nodes
        
    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}")
        raise e

def structure_response(
    llm: OpenAI, 
    query: str, 
    search_results: List[NodeWithScore]
) -> str:
    """
    Structure response using OpenAI
    
    Args:
        llm: OpenAI model
        query: Original user query
        search_results: Search results from index
        
    Returns:
        str: Structured response
    """
    try:
        # Prepare context from found documents
        context_parts = []
        for i, node in enumerate(search_results, 1):
            context_part = f"""
Source {i} (relevance: {node.score:.2f}):
{node.text}
---"""
            context_parts.append(context_part)
        
        context = "\n".join(context_parts)
        
        # Format prompt
        prompt = AppConfig.QUERY_PROMPT_TEMPLATE.format(
            context=context,
            query=query
        )
        
        logger.info("Sending request to OpenAI for response structuring")
        
        # Get response from LLM
        response = llm.complete(prompt)
        
        logger.info("Response successfully received from OpenAI")
        return response.text
        
    except Exception as e:
        logger.error(f"Error structuring response: {e}")
        raise e

def format_sources(search_results: List[NodeWithScore]) -> List[Dict[str, Any]]:
    """
    Format source information
    
    Args:
        search_results: Search results
        
    Returns:
        List[Dict]: Formatted source information
    """
    sources = []
    
    for node in search_results:
        source_info = {
            'text': node.text,
            'score': node.score,
            'node_id': node.node_id,
            'metadata': {}
        }
        
        # Extract metadata if available
        if hasattr(node, 'metadata') and node.metadata:
            metadata = node.metadata
            
            # Extract standard metadata fields
            source_info['metadata'] = {
                field: metadata.get(field, 'Unknown')
                for field in AppConfig.METADATA_FIELDS
                if field in metadata
            }
        
        sources.append(source_info)
    
    return sources

def validate_query(query: str) -> Tuple[bool, str]:
    """
    Validate user query
    
    Args:
        query: User input query
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not query or not query.strip():
        return False, "Query cannot be empty"
    
    if len(query.strip()) < AppConfig.MIN_QUERY_LENGTH:
        return False, f"Query too short. Minimum {AppConfig.MIN_QUERY_LENGTH} characters required"
    
    if len(query.strip()) > AppConfig.MAX_QUERY_LENGTH:
        return False, f"Query too long. Maximum {AppConfig.MAX_QUERY_LENGTH} characters allowed"
    
    return True, ""

def log_query(query: str, processing_time: float, num_results: int):
    """
    Log query statistics for monitoring
    
    Args:
        query: User query
        processing_time: Time taken to process
        num_results: Number of results returned
    """
    logger.info(f"Query processed: '{query[:50]}...' | "
                f"Time: {processing_time:.2f}s | "
                f"Results: {num_results}")

def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_metadata_display(metadata: Dict[str, Any]) -> str:
    """
    Format metadata for display
    
    Args:
        metadata: Metadata dictionary
        
    Returns:
        str: Formatted metadata string
    """
    formatted_items = []
    for key, value in metadata.items():
        if value and value != 'Unknown':
            formatted_key = key.replace('_', ' ').title()
            formatted_items.append(f"**{formatted_key}:** {value}")
    
    return "\n".join(formatted_items) if formatted_items else "No metadata available"

def calculate_avg_relevance(search_results: List[NodeWithScore]) -> float:
    """
    Calculate average relevance score
    
    Args:
        search_results: List of search results with scores
        
    Returns:
        float: Average relevance score
    """
    if not search_results:
        return 0.0
    
    total_score = sum(node.score for node in search_results)
    return total_score / len(search_results)

def retry_operation(func, max_retries: int = AppConfig.MAX_RETRIES, delay: float = AppConfig.RETRY_DELAY):
    """
    Retry operation with exponential backoff
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        delay: Initial delay between retries
        
    Returns:
        Result of successful function call
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (2 ** attempt))
            logger.warning(f"Retry attempt {attempt + 1} for operation")
    
    return None

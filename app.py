import streamlit as st
import time
from datetime import datetime
from typing import List, Dict, Optional
import traceback

from config import AppConfig
from utils import (
    initialize_llamacloud_index,
    initialize_openai_llm,
    search_knowledge_base,
    structure_response,
    format_sources,
    validate_query
)

# Page configuration
st.set_page_config(
    page_title="Research Q/A Bot",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_secrets():
    """Check if required API keys are available in Streamlit secrets"""
    try:
        openai_key = st.secrets["api_keys"]["openai_api_key"]
        llama_key = st.secrets["api_keys"]["llamacloud_api_key"]
        return True
    except KeyError as e:
        st.error(f"❌ Missing API key: {e}")
        st.error("Please configure API keys in Streamlit Secrets")
        st.info("""
        **How to set up Streamlit Secrets:**
        
        1. **Locally:** Create file `.streamlit/secrets.toml`
        2. **On Streamlit Cloud:** Add secrets through web interface
        
        **Required structure:**
        ```toml
        [api_keys]
        openai_api_key = "your_openai_key"
        llamacloud_api_key = "your_llamacloud_key"
        ```
        """)
        return False

def main():
    """Main application function"""
    
    # Check API keys
    if not check_secrets():
        st.stop()
    
    # Application header
    st.title("🔬 Research Q/A Assistant")
    st.markdown("*Intelligent assistant for analyzing scientific papers*")
    
    # Sidebar with settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Number of documents to retrieve
        num_docs = st.slider(
            "Number of documents to analyze",
            min_value=1,
            max_value=10,
            value=AppConfig.DEFAULT_TOP_K,
            help="More documents = more comprehensive answer, but slower"
        )
        
        # OpenAI temperature
        temperature = st.slider(
            "Response creativity (temperature)",
            min_value=0.0,
            max_value=1.0,
            value=AppConfig.DEFAULT_TEMPERATURE,
            step=0.1,
            help="0.0 = precise answers, 1.0 = creative answers"
        )
        
        st.markdown("---")
        st.markdown("**💡 Tip:** Ask specific questions for better results")
        
        # Example queries
        with st.expander("📝 Example queries"):
            for example in AppConfig.EXAMPLE_QUERIES:
                if st.button(f"💬 {example[:50]}...", key=example):
                    st.session_state.example_query = example
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Query input field
        default_query = st.session_state.get('example_query', '')
        query = st.text_area(
            "Enter your research question:",
            value=default_query,
            placeholder="e.g., What methods are used for volatility analysis in financial markets?",
            height=100,
            help="Ask specific questions to get more accurate answers"
        )
        
        # Clear example query from session state
        if 'example_query' in st.session_state:
            del st.session_state.example_query
        
        # Search button
        search_button = st.button(
            "🔍 Find Answer",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        # Index information
        with st.expander("📊 Index Information", expanded=True):
            st.markdown(f"""
            **Name:** {AppConfig.INDEX_NAME.split('.')[0]}...
            
            **Project:** {AppConfig.PROJECT_NAME}
            
            **Period:** 2024-2025
            
            **Topic:** Volatility Research
            
            **Chunk Size:** 256 tokens
            """)
    
    # Process search
    if search_button and query.strip():
        # Validate query
        is_valid, error_message = validate_query(query)
        if not is_valid:
            st.warning(f"⚠️ {error_message}")
            return
        
        with st.spinner("🔍 Searching for relevant information..."):
            try:
                # Initialize components
                start_time = time.time()
                
                # Initialize LlamaCloud index
                index = initialize_llamacloud_index()
                
                # Search knowledge base
                search_results = search_knowledge_base(index, query, top_k=num_docs)
                
                if not search_results:
                    st.warning("🤷‍♂️ No results found for your query. Try rephrasing your question.")
                    return
                
                # Initialize OpenAI
                llm = initialize_openai_llm(temperature=temperature)
                
                # Structure response
                with st.spinner("🤖 Analyzing and structuring response..."):
                    structured_response = structure_response(llm, query, search_results)
                
                end_time = time.time()
                processing_time = end_time - start_time
                
                # Display results
                display_results(structured_response, search_results, processing_time, query)
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.error("Please check your API key settings and try again.")
                
                # Show error details in debug mode
                if st.checkbox("Show error details"):
                    st.code(traceback.format_exc())
    
    elif search_button and not query.strip():
        st.warning("⚠️ Please enter a question to search.")
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔗 **Powered by:** LlamaIndex + OpenAI")
    with col2:
        st.markdown(f"⏰ **Time:** {datetime.now().strftime('%H:%M:%S')}")
    with col3:
        st.markdown("📚 **Database:** Arxiv 2024-2025")

def display_results(response: str, search_results: List, processing_time: float, query: str):
    """Display search results"""
    
    # Main response
    st.markdown("## 💬 Answer")
    
    # Response in beautiful container
    with st.container():
        st.markdown(
            f'<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">'
            f'{response}'
            f'</div>',
            unsafe_allow_html=True
        )
    
    # Sources
    st.markdown("## 📚 Sources")
    
    sources_info = format_sources(search_results)
    
    for i, source in enumerate(sources_info, 1):
        with st.expander(f"📄 Source {i} (Relevance: {source['score']:.2f})"):
            st.markdown("**Text fragment:**")
            st.markdown(f'"{source["text"]}"')
            
            if source.get('metadata'):
                st.markdown("**Metadata:**")
                for key, value in source['metadata'].items():
                    if value and value != 'Unknown':
                        st.markdown(f"- **{key}:** {value}")
    
    # Query statistics
    st.markdown("## 📊 Query Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Processing time", f"{processing_time:.2f} sec")
    
    with col2:
        st.metric("Sources found", len(search_results))
    
    with col3:
        avg_score = sum(source['score'] for source in sources_info) / len(sources_info)
        st.metric("Average relevance", f"{avg_score:.2f}")
    
    with col4:
        total_chars = sum(len(source['text']) for source in sources_info)
        st.metric("Context volume", f"{total_chars} chars")
    
    # Export button
    if st.button("📥 Export Result"):
        export_data = {
            "query": query,
            "response": response,
            "sources": sources_info,
            "timestamp": datetime.now().isoformat(),
            "processing_time": processing_time
        }
        
        st.download_button(
            label="Download JSON",
            data=str(export_data),
            file_name=f"research_qa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()

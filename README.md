# Research Q/A Bot 🔬

An intelligent Q/A assistant for analyzing scientific papers using LlamaIndex and OpenAI, deployed with Streamlit.

## Features

- **Semantic Search**: Find relevant information from scientific papers using vector similarity
- **Structured Answers**: Get organized, fact-based responses powered by OpenAI GPT models
- **Source Citations**: View exact sources and relevance scores for transparency
- **Interactive UI**: Clean, user-friendly Streamlit interface
- **Configurable Settings**: Adjust search parameters and response creativity

## Tech Stack

- **Frontend**: Streamlit
- **Search Engine**: LlamaIndex with LlamaCloud
- **LLM**: OpenAI GPT-4o-mini
- **Deployment**: Streamlit Cloud
- **Language**: Python 3.8+

## Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd research-qa-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Secrets

#### Local Development
Create `.streamlit/secrets.toml`:
```toml
[api_keys]
openai_api_key = "sk-proj-your-openai-key"
llamacloud_api_key = "llx-your-llamacloud-key"
```

#### Streamlit Cloud Deployment
1. Deploy your app to Streamlit Cloud
2. Go to app settings → Secrets
3. Add the same structure as above

### 4. Run Application
```bash
streamlit run app.py
```

## Configuration

### API Keys Required
- **OpenAI API Key**: For response generation and structuring
- **LlamaCloud API Key**: For accessing the pre-built research index

### Index Configuration
The app is configured to use:
- **Index**: "Arxiv 2024-2025. Key: Volatility"
- **Organization ID**: "858afa1e-d3dc-4a96-8783-d4f3798b0643"
- **Project**: "Default"

## Usage

1. **Enter Question**: Type your research question in the text area
2. **Adjust Settings**: Use sidebar to configure:
   - Number of documents to analyze (1-10)
   - Response creativity (0.0-1.0)
3. **Search**: Click "Find Answer" to get results
4. **Review Results**: 
   - Read the structured answer
   - Check source citations
   - View relevance scores
5. **Export**: Download results as JSON for later use

## Example Queries

- "What methods are used for volatility analysis in financial markets?"
- "What are GARCH models and how are they applied?"
- "What factors influence stock volatility?"
- "Compare different approaches to volatility forecasting"
- "What metrics are used to assess portfolio risk?"

## File Structure

```
research-qa-bot/
├── app.py              # Main Streamlit application
├── config.py           # Configuration settings
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── .streamlit/
    └── secrets.toml   # API keys (local only)
```

## Security Notes

- **Never commit API keys** to version control
- Use Streamlit Secrets for secure key management
- `.streamlit/secrets.toml` is excluded in `.gitignore`
- Different keys can be used for development and production

## Deployment

### Streamlit Cloud
1. Push code to GitHub (without secrets)
2. Connect repository to Streamlit Cloud
3. Configure secrets in the web interface
4. Deploy automatically

### Local Development
1. Create `.streamlit/secrets.toml` with your API keys
2. Run `streamlit run app.py`
3. Access at `http://localhost:8501`

## Troubleshooting

### Common Issues

**API Key Errors**
- Ensure secrets are properly configured
- Check key format and validity
- Verify organization access for LlamaCloud

**No Search Results**
- Try rephrasing your question
- Use more specific terms
- Check if the topic is covered in the index

**Slow Performance**
- Reduce number of documents in settings
- Use more specific queries
- Check internet connection

### Debug Mode
Enable "Show error details" checkbox for detailed error information.

## Customization

### Modify Search Parameters
Edit `config.py`:
- `DEFAULT_TOP_K`: Default number of documents
- `MIN_SIMILARITY_SCORE`: Relevance threshold
- `DEFAULT_TEMPERATURE`: Response creativity

### Change Prompts
Update prompts in `config.py`:
- `SYSTEM_PROMPT`: System instructions for AI
- `QUERY_PROMPT_TEMPLATE`: Response formatting template

### Add Features
Extend functionality in `utils.py`:
- Add new metadata processing
- Implement caching
- Add export formats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check troubleshooting section
2. Review configuration settings
3. Open an issue on GitHub

---

**Built with ❤️ using LlamaIndex and OpenAI**

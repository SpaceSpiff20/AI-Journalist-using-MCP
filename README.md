# 📰 AI Journalist using MCP

An AI-powered digital journalist that scrapes news and Reddit discussions, analyzes them using cutting-edge LLMs (Claude + Groq), and generates a professional audio news broadcast using ElevenLabs TTS.

This project leverages MCP (Model Context Protocol), LangGraph, and FastAPI + Streamlit to deliver a seamless end-to-end pipeline:
 👉 Collects live news & Reddit content
 👉 Summarizes into broadcast-style scripts
 👉 Converts to realistic voice audio

## 🚀 Features

- Multi-source Content Aggregation

- Google News scraping with BrightData

- Reddit discussions analysis (last 2 weeks only)

- AI-Powered Summarization

- News transformed into broadcast-ready scripts using Claude (Anthropic)

- Sentiment and trend analysis from Reddit

- Groq-powered summarization for scalability

- Text-to-Speech (TTS) Conversion

- ElevenLabs SDK for realistic audio

- Fallback with Google gTTS

- Interactive Frontend

- Built with Streamlit

- Add/remove up to 3 topics

- Choose source: News, Reddit, or Both

- Generate & download audio summaries instantly

- Backend API

- FastAPI endpoint /generate-news-audio

- Returns MP3 audio response

## 🛠️ Tech Stack

- Frontend: Streamlit (user-friendly dashboard)

- Backend: FastAPI (REST API for news/audio generation)

- AI Models:

- Anthropic Claude (news + Reddit summarization)

-  Groq LLaMA-3 (news summarization alternative)

- MCP (Model Context Protocol): Reddit & BrightData integration

- Text-to-Speech: ElevenLabs SDK, gTTS fallback

- Others: LangGraph, Tenacity, AsyncLimiter, BeautifulSoup

##📂 Project Structure
```
AI-Journalist-using-MCP/
│── backend.py         # FastAPI backend (serves audio API)
│── frontend.py        # Streamlit UI
│── models.py          # Pydantic models (request validation)
│── news_scraper.py    # Google News scraper + summarizer
│── reddit_scraper.py  # Reddit scraper + summarizer
│── utils.py           # Helper functions (scraping, TTS, summarization)
│── audio/             # Generated audio files
│── requirements.txt   # Dependencies
│── .env               # API keys & configs
```
## ⚙️ Setup & Installation

Clone the repository
```
git clone https://github.com/yourusername/ai-journalist-mcp.git
cd ai-journalist-mcp
```

Create a virtual environment
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

Install dependencies
```
pip install -r requirements.txt
```

Set up environment variables (.env)
```
ANTHROPIC_API_KEY=your_anthropic_key
GROQ_API_KEY=your_groq_key
BRIGHTDATA_API_KEY=your_brightdata_key
BRIGHTDATA_WEB_UNLOCKER_ZONE=your_zone
ELEVEN_API_KEY=your_elevenlabs_key
API_TOKEN=your_brightdata_key
WEB_UNLOCKER_ZONE=your_web_unlocker_zone
```

Run the backend (FastAPI)
```
uvicorn backend:app --host 0.0.0.0 --port 1234 --reload
```

Run the frontend (Streamlit)
```
streamlit run frontend.py
```
## 🎯 Usage

- Open the Streamlit app in your browser.

- Enter topics (up to 3, e.g., Artificial Intelligence, Global Economy).

- Select data sources: News / Reddit / Both.

- Click Generate Summary 🚀.

- Listen to the AI-generated audio news broadcast 🎙️.

- Download the MP3 file.

## 🔮 Future Improvements

- Multi-language support for non-English news

- Live podcast streaming mode

- Sentiment-based voice modulation

- Integration with YouTube & Twitter scraping

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve.

## 📜 License

This project is licensed under the MIT License.

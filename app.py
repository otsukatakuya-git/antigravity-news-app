import streamlit as st
import feedparser
from urllib.parse import quote

# Configure page
st.set_page_config(page_title="Antigravity News", page_icon="📰", layout="wide")

# CSS for Card-style design and dark mode compatibility if needed
st.markdown("""
<style>
.news-card {
    background-color: #262730;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    border: 1px solid #444;
    color: #FAFAFA;
}
@media (prefers-color-scheme: light) {
    .news-card {
        background-color: #f9f9f9;
        border-color: #ddd;
        color: #333;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
}
.news-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 10px;
    color: #1E88E5;
}
.news-date {
    font-size: 0.9rem;
    color: #888;
    margin-bottom: 15px;
}
.news-summary {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 20px;
}
.news-link {
    display: inline-block;
    background-color: #1E88E5;
    color: white !important;
    padding: 10px 18px;
    text-decoration: none;
    border-radius: 6px;
    font-weight: bold;
    transition: background-color 0.3s;
}
.news-link:hover {
    background-color: #1565C0;
}
</style>
""", unsafe_allow_html=True)

st.title("📰 Antigravity ニュース収集ダッシュボード")

# Sidebar for search
st.sidebar.header("検索設定")
search_query = st.sidebar.text_input("検索キーワード", value="Antigravity")

@st.cache_data(ttl=600)
def get_news(query):
    # Construct Google News RSS URL for Japan
    encoded_query = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(url)
    return feed.entries

if search_query:
    st.write(f"**「{search_query}」**の最新ニュース")
    
    with st.spinner("ニュースを取得中..."):
        entries = get_news(search_query)
        
        if entries:
            for entry in entries:
                title = entry.get("title", "タイトルなし")
                published = entry.get("published", "日付不明")
                summary = entry.get("summary", "要約なし")
                link = entry.get("link", "#")
                
                # Render using HTML for the card layout
                st.markdown(f"""
                <div class="news-card">
                    <div class="news-title">{title}</div>
                    <div class="news-date">📅 {published}</div>
                    <div class="news-summary">{summary}</div>
                    <a class="news-link" href="{link}" target="_blank">🔗 元記事を読む</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("ニュースが見つかりませんでした。別のキーワードをお試しください。")
else:
    st.info("サイドバーから検索キーワードを入力してください。")

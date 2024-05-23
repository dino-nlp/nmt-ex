import mwparserfromhell
import wikipedia
import ollama
from wikipedia.exceptions import DisambiguationError, PageError

def summarize_article(content, model="llama2"):
    """Tóm tắt nội dung bài viết Wikipedia bằng Ollama API."""
    prompt = f"Vui lòng tóm tắt bài viết Wikipedia sau:\n\n{content}"
    # Initialize the Ollama client with your model (e.g., llama2)
    generator = ollama.Ollama(model=model) 
    response = generator.generate(prompt)
    return response.text

def search_and_summarize_ai_articles(topic_name, num_articles=5):
    """Tìm kiếm các bài viết Wikipedia về AI và tóm tắt chúng."""
    try:
        wikipedia.set_lang("vi")  # Đặt ngôn ngữ tiếng Việt
        search_results = wikipedia.search(topic_name)

        summaries = []
        for title in search_results[:num_articles]:
            try:
                page = wikipedia.page(title, auto_suggest=False)
                wikicode = mwparserfromhell.parse(page.content)
                plain_text = wikicode.strip_code()  # Loại bỏ wikicode
                summary = summarize_article(plain_text)
                summaries.append((title, summary))
            except (DisambiguationError, PageError):
                pass  # Bỏ qua các trang không rõ ràng hoặc không tồn tại

        return summaries
    except wikipedia.exceptions.WikipediaException as e:
        print(f"Lỗi khi tìm kiếm trên Wikipedia: {e}")
        return []

def main():
    topic_name = input("Nhập chủ đề liên quan đến AI: ")
    summaries = search_and_summarize_ai_articles(topic_name)

    if summaries:
        print("\nCác bài viết được tìm thấy và tóm tắt:")
        for title, summary in summaries:
            print(f"\nTiêu đề: {title}")
            print(f"Tóm tắt: {summary}")
    else:
        print("Không tìm thấy bài viết nào về chủ đề này.")

if __name__ == "__main__":
    main()

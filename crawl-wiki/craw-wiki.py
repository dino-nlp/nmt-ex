import sys
import mwparserfromhell
import wikipedia

def summarize_wikipedia_articles(topic, num_articles=5):
    wikipedia.set_lang("vi")
    search_results = wikipedia.search(topic, results=num_articles)

    summaries = []
    for title in search_results:
        print(f"--- title: {title}")
        try:
            page = wikipedia.page(title, auto_suggest=False)
            wikicode = mwparserfromhell.parse(page.content)
            # print(wikicode)

            first_paragraph = None
            for node in wikicode.nodes:
                if isinstance(node, mwparserfromhell.nodes.tag.Tag) and node.tag == "p":
                    first_paragraph = node.contents.strip_code()
                    break

            if first_paragraph:
                summaries.append(f"**{title}:** {first_paragraph}")
        except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
            pass  # Bỏ qua các trang không rõ ràng hoặc không tồn tại

    return summaries

def main():
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        summaries = summarize_wikipedia_articles(topic)
        for summary in summaries:
            print(summary)
            print("-" * 20)
    else:
        print("Vui lòng cung cấp chủ đề tìm kiếm (ví dụ: python script.py AI)")

if __name__ == "__main__":
    main()

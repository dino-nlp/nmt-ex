from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import sys
import mwparserfromhell
import wikipedia
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer 
import nltk
nltk.download('punkt')

language = "english"

def summary_paragraph(text):
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = LsaSummarizer()  # You can try other summarizers here
    summary = summarizer(parser.document, 4)  # Summarize into 2 sentences
    return summary

def summarize_wikipedia_articles(topic, num_articles=5):
    wikipedia.set_lang(language)
    search_results = wikipedia.search(topic, results=num_articles)

    summaries = []
    for title in search_results:
        print(f"======= title: {title}")
        try:
            page = wikipedia.page(title, auto_suggest=False)
            wikicode = mwparserfromhell.parse(page.content)

            for template in wikicode.filter_templates():
                if template.name.matches(["Infobox", "Navigation", "Cite"]):
                    wikicode.remove(template)
            text = wikicode.strip_code()
            sumary = summary_paragraph(text)
            print(sumary)
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

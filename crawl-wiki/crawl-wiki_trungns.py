import wikipedia
import re
import os

wiki_links_folder = "wiki_links"  # Folder containing wiki link files
output_folder = "contextual_data"  # Folder to save output files

template_wiki_link_filename = "_wiki_links.txt"
template_output_filename = "_contextual_data.en"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def split_paragraph_alternating(text, lengths=[2, 3]):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    
    paragraphs = []
    current_paragraph = []
    length_index = 0

    for sentence in sentences:
        current_paragraph.append(sentence.strip())  # Trim leading/trailing whitespace
        if len(current_paragraph) == lengths[length_index]:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = current_paragraph[-1:]
            length_index = (length_index + 1) % len(lengths)

    if current_paragraph and current_paragraph[0]:  # Check for non-empty paragraph
        paragraphs.append(" ".join(current_paragraph))

    return paragraphs

for filename in os.listdir(wiki_links_folder):
    if filename.endswith(template_wiki_link_filename):
        category = filename.split("_")[0]  # Extract category from filename
        wiki_links_file = os.path.join(wiki_links_folder, filename)
        output_file = os.path.join(output_folder, filename.replace(template_wiki_link_filename, template_output_filename))

        try:
            with open(wiki_links_file, "r") as file:
                wikipedia_links = [line.strip() for line in file if line.strip()]

            with open(output_file, "w") as outfile:
                for url in wikipedia_links:
                    try:
                        page_id = url.split("/")[-1]
                        page = wikipedia.page(page_id, auto_suggest=False)
                    except wikipedia.exceptions.DisambiguationError as e:
                        found_category = False
                        for option in e.options:
                            if category.lower() in option.lower():
                                try:
                                    page = wikipedia.page(option)
                                    found_category = True
                                    break
                                except wikipedia.exceptions.PageError:
                                    pass
                        if not found_category:
                            page = wikipedia.page(e.options[0])  # Select the first option if category not found

                    summary = re.sub(r'\n+', ' ', page.summary).strip()
                    paragraphs = split_paragraph_alternating(summary)
                    for paragraph in paragraphs:
                        if paragraph:
                            outfile.write(paragraph + "\n")

        except FileNotFoundError:
            print(f"Error: The file '{wiki_links_file}' was not found.")
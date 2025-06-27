import re
import json

def parse_single_chapter_content(file_content_string: str, original_filename: str):
    """
    Parses the string content of a single chapter file.
    Identifies chapter info, sections, text blocks, and code blocks.
    Returns a structured representation.
    """
    chapter_match = re.search(r"Rozdział (\d+):\s*(.*)", file_content_string)
    chapter_number = int(chapter_match.group(1)) if chapter_match else 0
    chapter_title = chapter_match.group(2).strip() if chapter_match else "Unknown Chapter"

    # Remove the chapter title line to avoid it being part of content
    if chapter_match:
        file_content_string = file_content_string[chapter_match.end():]

    # Split content by section headers "Krok X.Y: Title" or "Wprowadzenie" or "Podsumowanie"
    # Using a positive lookahead to keep the delimiters
    raw_sections = re.split(r"(Krok \d+\.\d+:\s*.*|Wprowadzenie|Podsumowanie|Omówienie Kluczowych Zmian|Jak to uruchomić\?|Czego się spodziewać\?|Jak to działa\?)", file_content_string)

    parsed_sections = []
    current_section_title = "Wprowadzenie" # Default for content before first "Krok" or if "Wprowadzenie" is first

    # The first element of raw_sections might be content before the first explicit section title
    # or empty if the content starts directly with a known title.

    # Handle content before the first recognized section delimiter
    if raw_sections[0].strip():
        # If the first part is not a delimiter and not empty, treat it as part of an implicit "Wprowadzenie"
        # or initial content block if no "Wprowadzenie" delimiter matched first.
        # This logic is tricky because "Wprowadzenie" is also a delimiter.
        # Let's adjust: if the first delimiter is not "Wprowadzenie", the first block of text is introductory.
        if not (len(raw_sections) > 1 and raw_sections[1].strip() == "Wprowadzenie"):
             first_block_content = raw_sections[0].strip()
             if first_block_content:
                parsed_sections.append({
                    "sectionTitle": "Wstęp" if chapter_title != "Unknown Chapter" else "Zawartość Pliku", # Generic title if no chapter title
                    "contentBlocks": parse_content_blocks(first_block_content)
                })

    idx = 1
    while idx < len(raw_sections):
        section_title_candidate = raw_sections[idx].strip()
        section_content = raw_sections[idx+1].strip() if idx+1 < len(raw_sections) else ""

        current_section_title = section_title_candidate

        if section_content: # Only add section if there's content
            parsed_sections.append({
                "sectionTitle": current_section_title,
                "contentBlocks": parse_content_blocks(section_content)
            })
        idx += 2

    return {
        "originalFileName": original_filename,
        "chapterNumber": chapter_number,
        "title": chapter_title,
        "sections": parsed_sections,
    }

def parse_content_blocks(section_content: str):
    """
    Parses the content of a section into text and code blocks.
    """
    content_blocks = []
    lines = section_content.splitlines()
    current_block = []
    in_code_block = False
    code_language = None

    # Common language keywords that might indicate start of a code block
    # if not explicitly marked by ```
    code_keywords = ["Python", "Bash", "JavaScript", "JSON", "HTML", "CSS", "PowerShell"]

    for line in lines:
        stripped_line = line.strip()

        # Check for explicit code block markers or language keywords
        # This is a simple heuristic and might need to be more robust
        is_code_keyword_line = any(stripped_line.startswith(keyword) for keyword in code_keywords) and len(stripped_line.split()) < 4

        if is_code_keyword_line and not in_code_block: # Potential start of a new code block
            if current_block: # Save previous text block
                content_blocks.append({"type": "text", "value": "\n".join(current_block).strip()})
                current_block = []

            in_code_block = True
            code_language = stripped_line # Assume the keyword line is the language
            # Don't add the keyword line itself to the code content if it's just the language name
            if any(stripped_line == kw for kw in code_keywords):
                continue # Skip this line, it's just a language marker

        elif in_code_block:
            # Heuristic to end a code block:
            # 1. Empty line followed by non-indented text (potential start of new paragraph)
            # 2. Line that looks like a new section title (though sections are split earlier)
            # 3. Or simply, if the next line doesn't look like code.
            # This is tricky without explicit markers. For now, we assume code continues
            # until a very clear break. If the content structure implies code is often
            # followed by explanatory text without blank lines, this needs adjustment.

            # For now, let's assume code blocks are contiguous lines after the "Python" / "Bash" keyword
            # and end when a non-indented line appears or a new section starts (handled by main parser)
            # A simple way: if a line is not indented and not empty, and we are in a code block,
            # it might be the start of a new text paragraph.
            if not line.startswith(" ") and stripped_line != "" and not is_code_keyword_line: # Potential end of code block
                if current_block:
                    content_blocks.append({
                        "type": "code",
                        "language": code_language.lower() if code_language else "unknown",
                        "value": "\n".join(current_block).strip()
                    })
                    current_block = []
                in_code_block = False
                code_language = None
                current_block.append(line) # This line is part of the new text block
            else:
                current_block.append(line)

        else: # Regular text line
            current_block.append(line)

    # Add any remaining block
    if current_block:
        block_type = "code" if in_code_block else "text"
        lang = code_language.lower() if code_language and in_code_block else "unknown"
        if block_type == "code":
             content_blocks.append({"type": "code", "language": lang, "value": "\n".join(current_block).strip()})
        else:
             content_blocks.append({"type": "text", "value": "\n".join(current_block).strip()})

    return [block for block in content_blocks if block["value"]] # Filter out empty blocks


def process_all_chapter_contents(file_contents_map: dict):
    """
    Takes a dictionary of {original_filename: file_content_string}.
    Parses each chapter's content and returns a consolidated structure.
    """
    parsed_chapters = []
    for filename, content_string in file_contents_map.items():
        if content_string: # Ensure content is not empty
            chapter_data = parse_single_chapter_content(content_string, filename)
            parsed_chapters.append(chapter_data)

    # Sort chapters by their extracted chapterNumber
    parsed_chapters.sort(key=lambda x: x.get("chapterNumber", 0))

    return {
        "courseTitle": "AI Agents Development Course", # This could be made dynamic later
        "chapters": parsed_chapters
    }

if __name__ == '__main__':
    # Example usage for testing the parser independently
    sample_content = """Rozdział 3: Budowa Agenta – Pisanie Kodu
W folderze moj-agent-scraper stwórz plik o nazwie scraper_agent.py.

Krok 3.1: Importy i Konfiguracja
import os
import asyncio

Python
# Krok 3.1: Importy i Konfiguracja
import os

To jest jakiś tekst wyjaśniający.

Bash
echo "Hello World"
ls -l

To jest kolejny tekst.
A to kontynuacja.

Krok 3.2: Sercem Operacji – Klasa SandboxedBrowser
Ta klasa jest ważna.
    """

    parsed_chapter = parse_single_chapter_content(sample_content, "test_file.txt")
    print(json.dumps(parsed_chapter, indent=2, ensure_ascii=False))

    # Test process_all_chapter_contents
    file_map = {
        "test_file1.txt": sample_content,
        "test_file2.txt": "Rozdział 1: Wstęp do AI\nTo jest wstęp."
    }
    all_data = process_all_chapter_contents(file_map)
    print("\n--- All Data ---")
    print(json.dumps(all_data, indent=2, ensure_ascii=False))

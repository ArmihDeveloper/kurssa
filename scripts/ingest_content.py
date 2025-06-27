import os
import json
import sys

# Adjust the path to import from the backend directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.content_parser import process_all_chapter_contents

# This script now expects to read its input from a JSON file
# that the agent prepares.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_INPUT_FILE = os.path.join(SCRIPT_DIR, "temp_fetched_contents.json")

def main():
    """
    Main logic for content ingestion.
    Reads fetched content from a temporary JSON file, parses it,
    and saves the structured course data.
    """
    print(f"Starting content ingestion script. Reading from {TEMP_INPUT_FILE}...")

    file_contents_map = {}
    try:
        with open(TEMP_INPUT_FILE, 'r', encoding='utf-8') as f:
            file_contents_map = json.load(f)
        print(f"Successfully loaded fetched contents from {TEMP_INPUT_FILE}.")
    except FileNotFoundError:
        print(f"[FATAL ERROR] Temporary input file not found: {TEMP_INPUT_FILE}")
        print("This script expects the agent to create this file with fetched contents.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[FATAL ERROR] Could not decode JSON from {TEMP_INPUT_FILE}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[FATAL ERROR] An unexpected error occurred while reading {TEMP_INPUT_FILE}: {e}")
        sys.exit(1)

    if not file_contents_map:
        print("No content found in the input file. Aborting detailed parsing.")
        course_data = {"courseTitle": "AI Agents Development Course - INGESTION FAILED (No Content in Input File)", "chapters": []}
    else:
        print("\nParsing all loaded chapter contents...")
        # The parser already expects a map of filename to content string
        course_data = process_all_chapter_contents(file_contents_map)

        # If some files had errors during fetching (now done by agent),
        # those errors might be part of the content string.
        # The parser should ideally handle this, or we can pre-filter here.
        # For now, process_all_chapter_contents should be robust.
        # Let's assume errors are stored as string values in file_contents_map by the agent.
        # The parser will then include these errors in its output.

        # Example: check if any "chapters" have an error field if agent added it,
        # or if content string itself is an error message.
        processed_chapters_count = 0
        failed_files_count = 0
        if "chapters" in course_data:
            for chapter in course_data["chapters"]:
                # A simple check: if a chapter has an "error" key, or its content is very short
                # and starts with "Error", it might be a fetch failure.
                # The current parser `process_all_chapter_contents` will create chapters
                # even for error strings, the `parse_single_chapter_content` will try to parse them.
                # This might result in chapters with "Unknown Title" etc.
                # For now, we rely on the parser output.
                if chapter.get("error") or (isinstance(chapter.get("title"), str) and chapter.get("title") == "Unknown Chapter"): # Heuristic
                     failed_files_count +=1
                else:
                     processed_chapters_count +=1
            print(f"Parsing complete. Successfully processed chapters: {processed_chapters_count}, Failed/Error chapters: {failed_files_count}")


    output_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', 'data')
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, 'course_data.json')

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(course_data, f, indent=2, ensure_ascii=False)
        print(f"\nSuccessfully processed content and saved to: {output_file_path}")

        if course_data and "chapters" in course_data:
            print(f"Total chapter entries in JSON: {len(course_data['chapters'])}")
            for i, chap in enumerate(course_data['chapters']):
                status = "OK" if "error" not in chap and chap.get("title") != "Unknown Chapter" else "ERROR" # Adjusted status check
                print(f"  {i+1}. Ch No: {chap.get('chapterNumber', 'N/A')}, Title: {chap.get('title', 'N/A')}, Sections: {len(chap.get('sections', []))}, Status: {status}")
                if status == "ERROR":
                    if chap.get("error"):
                        print(f"     Error details: {chap.get('error')}")
                    else:
                        print(f"     Note: Chapter title is 'Unknown Chapter', may indicate parsing issue or error content.")

    except IOError as e: print(f"Error writing processed data to file: {e}")
    except TypeError as e: print(f"Error serializing data to JSON: {e}. Check data structures.")

# This script is intended to be run by an agent that has already fetched
# the content and placed it into TEMP_INPUT_FILE.
if __name__ == "__main__":
    # For local testing of this script:
    # 1. Manually create a 'temp_fetched_contents.json' in the same directory as this script.
    #    It should have the format: {"filename1": "content1", "filename2": "content2", ...}
    # 2. Then run `python scripts/ingest_content.py`
    print("Running ingest_content.py. Ensure 'temp_fetched_contents.json' exists for local testing.")

    # Example of creating a dummy temp_fetched_contents.json for testing:
    if not os.path.exists(TEMP_INPUT_FILE):
        print(f"Creating dummy {TEMP_INPUT_FILE} for local test run.")
        dummy_contents = {
            "KOD Solagents 2. Budowa Agenta.txt": "Rozdział 3: Budowa Agenta – Pisanie Kodu\nTo jest testowy kontent dla budowy agenta.",
            "Smolagenta 4 Agent Ktory Mysli.txt": "Rozdział 7: Agent, który Myśli\nTestowy kontent dla myślącego agenta.\nKrok 7.1: Coś tam\nJakiś tekst.",
            "NonExistentFile.txt": "Error fetching content for NonExistentFile.txt: Simulated HTTP Error"
        }
        with open(TEMP_INPUT_FILE, 'w', encoding='utf-8') as f_dummy:
            json.dump(dummy_contents, f_dummy, indent=2)

    main()

import os
from tavily import TavilyClient
from dotenv import load_dotenv
from LanguageModelProcessor import*

# Load environment variables from .env file
load_dotenv()

class CreateAdvisor:
    def __init__(self, AI_ADVISOR_NAME):
        """
        Initialize the CreateAdvisor class with the AI advisor name and Tavily client.
        """
        self.AI_ADVISOR_NAME = AI_ADVISOR_NAME
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please set TAVILY_API_KEY in the .env file.")
        self.tavily_client = TavilyClient(api_key)
    
    def tavily_search(self, query):
        """
        Perform a search on Tavily using the provided query (URL).
        """
        try:
            search_result = self.tavily_client.get_search_context(query, search_depth="advanced", max_tokens=10000)
            return search_result
        except Exception as e:
            print(f"An error occurred while searching with Tavily: {e}")
            return None
    
    def process_urls(self, WEBSITE_URLs):
        """
        Process a list of URLs, sending each to Tavily and saving the results in separate .txt files.
        """
        for i, url in enumerate(WEBSITE_URLs):
            result = self.tavily_search(url)
            if result:
                filename = f"{self.AI_ADVISOR_NAME}_url_result_{i + 1}.txt"
                with open(filename, 'w') as file:
                    file.write(result)
                print(f"Result for URL {url} saved in {filename}")
            else:
                print(f"Skipping URL {url} due to an error.")

if __name__ == "__main__":
    manager = ConversationManager()
    asyncio.run(manager.main())

    Friendly = ["Relatable", "Kind", "Even-Tempered", "Sunny", "Empathetic"]
    Sweet = ["Quietly Confident", "Wise", "Gentle", "Warm", "Calm"]
    Conscientious = ["Intelligent", "Thoughtful", "Resourceful", "Perfectionist"]
    Bubbly = ["Fun", "Expressive", "Dynamic", "High Energy", "Peppy"]
    Free_Spirited = ["Adventurous", "Experimenting", "Nonconforming", "Genuine", "Unpretentious"]
    BEHAVIOUR_OPTION = [Friendly, Sweet, Conscientious, Bubbly, Free_Spirited]

    print("Please select a behavior option by entering the corresponding number:")
    for i, option in enumerate(BEHAVIOUR_OPTION):
        print(f"{i + 1}: {option}")

    choice = int(input("Enter your choice (1-5): ")) - 1
    
    if 0 <= choice < len(BEHAVIOUR_OPTION):
        selected_behaviour = BEHAVIOUR_OPTION[choice]
        print(f"You have selected: {selected_behaviour}")
    else:
        print("Invalid choice, please select a number between 1 and 5.")
    AI_ADVISOR_NAME = input(" AI ADVISOR NAME: ")
    # Dictionary to map language names to their respective codes
    languages = {
        "Bulgarian": "bg",
        "Catalan": "ca",
        "Chinese (Mandarin, Simplified)": "zh, zh-CN, zh-Hans",
        "Chinese (Mandarin, Traditional)": "zh-TW, zh-Hant",
        "Czech": "cs",
        "Danish": "da, da-DK",
        "Dutch": "nl",
        "English": "en, en-US, en-AU, en-GB, en-NZ, en-IN",
        "Estonian": "et",
        "Finnish": "fi",
        "Flemish": "nl-BE",
        "French": "fr, fr-CA",
        "German": "de",
        "German (Switzerland)": "de-CH",
        "Greek": "el",
        "Hindi": "hi",
        "Hungarian": "hu",
        "Indonesian": "id",
        "Italian": "it",
        "Japanese": "ja",
        "Korean": "ko, ko-KR",
        "Latvian": "lv",
        "Lithuanian": "lt",
        "Malay": "ms",
        "Multilingual (Spanish + English)": "multi",
        "Norwegian": "no",
        "Polish": "pl",
        "Portuguese": "pt, pt-BR",
        "Romanian": "ro",
        "Russian": "ru",
        "Slovak": "sk",
        "Spanish": "es, es-419",
        "Swedish": "sv, sv-SE",
        "Thai": "th, th-TH",
        "Turkish": "tr",
        "Ukrainian": "uk",
        "Vietnamese": "vi"
    }

    # Display available languages
    print("Available languages:")
    for language in languages:
        print(f"{language}: {languages[language]}")

    # Prompt user for language selection
    selected_language = input("Which language do you select? (Enter the language name or code): ").strip()

    # Check if the input is a language name or code
    if selected_language in languages:
        selected_code = languages[selected_language]
        print(f"You have selected: {selected_language} with code(s): {selected_code}")
    elif selected_language in [code for codes in languages.values() for code in codes.split(", ")]:
        # Find the corresponding language name for the entered code
        selected_language = next(language for language, codes in languages.items() if selected_language in codes.split(", "))
        selected_code = languages[selected_language]
        print(f"You have selected: {selected_language} with code(s): {selected_code}")
    else:
        print("Invalid selection. Please enter a valid language name or code.")


###################################################### Creating Instructions #######################        
    INSTRUCTIONS = input(" INSTRUCTIONS")

#     KNOWLEDGE_FILE_PDF = []
#     ADVISOR_ROLE = input(" DESCRIBE AI ADVISOR ROLE: ")
#     ADDITIONAL_PROMPTING = input(" ADDITIONAL PROMPTING: ")
#     KNOWLEDGE_SCRIPT = ""
#     DO_NOT_TALK_ABOUT = input(" DO NOT TALK ABOUT POINTS: ")
#     WELCOME_MESSAGE = input(" ENTER THE WELCOME MESSAGE: ")
#     STARTER_QUESTION = input(" STARTER QUESTIONS SEPERATED BY COMMAS: ").split(',')
#     STARTER_QUESTION_LIST = [url.strip() for url in STARTER_QUESTION]
    


#     VOICE = {
#     "Asteria": "aura-asteria-en",
#     "Orion": "aura-orion-en",
#     "Luna": "aura-luna-en",
#     "Echo": "aura-echo-en",
#     "Nova": "aura-nova-en"
# }
    
    WEBSITE_URLs = input("Please enter the URLs separated by commas: ").split(',')
    WEBSITE_URLs = [url.strip() for url in WEBSITE_URLs]
    
    advisor = CreateAdvisor(AI_ADVISOR_NAME)
    advisor.process_urls(WEBSITE_URLs)

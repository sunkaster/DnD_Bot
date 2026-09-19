from datetime import datetime, timedelta
import json
import random
import requests

# Quote caching system
class QuoteCache:
    def __init__(self):
        self.quotes = []
        self.last_refresh = None
        self.daily_quote = None
        self.daily_quote_date = None
        self.word_library = self.load_word_library()

    def load_word_library(self):
        """Load the local word library JSON file into memory."""
        try:
            with open("the_word_library.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                return {str(key): value for key, value in data.items()}
        except FileNotFoundError:
            print("Word library file not found.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in word library: {e}")
            return {}

    def get_random_word_library_quote(self):
        """Get a random quote from the local word library."""
        if not self.word_library:
            self.word_library = self.load_word_library()

        if not self.word_library:
            return None

        available_keys = sorted(int(key) for key in self.word_library.keys())
        if not available_keys:
            return None

        selected_key = random.randint(1, max(available_keys))
        quote_entry = self.word_library.get(str(selected_key))

        if quote_entry is None:
            fallback_key = random.choice(available_keys)
            quote_entry = self.word_library.get(str(fallback_key))

        if not quote_entry:
            return None

        text, author = quote_entry
        return {'text': text, 'author': author}

    def needs_refresh(self):
        """Check if cache needs to be refreshed (once per day)"""
        if not self.last_refresh:
            return True
        return datetime.now() - self.last_refresh > timedelta(days=1)
    
    def fetch_quotes(self):
        """Fetch a batch of quotes from zenquotes.io"""
        try:
            response = requests.get("https://zenquotes.io/api/quotes")
            if response.status_code == 200:
                quotes_data = response.json()
                self.quotes = [
                    {'text': q['q'], 'author': q['a']} 
                    for q in quotes_data if q['q'] and q['a']
                ]
                self.last_refresh = datetime.now()
                print(f"Refreshed quote cache with {len(self.quotes)} quotes")
                return True
            else:
                print(f"Failed to fetch quotes: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"Error fetching quotes: {e}")
            return False
    
    def get_random_quote(self):
        """Get a random quote from cache"""
        if self.needs_refresh() or not self.quotes:
            if not self.fetch_quotes():
                return None
        
        if self.quotes:
            return random.choice(self.quotes)
        return None
    
    def get_daily_quote(self):
        """Get the quote of the day (cached daily)"""
        today = datetime.now().date()
        
        # Check if we need to fetch today's quote
        if self.daily_quote_date != today or not self.daily_quote:
            try:
                response = requests.get("https://zenquotes.io/api/today")
                if response.status_code == 200:
                    quote_data = response.json()[0]
                    self.daily_quote = {
                        'text': quote_data['q'],
                        'author': quote_data['a']
                    }
                    self.daily_quote_date = today
                    print("Refreshed daily quote")
                else:
                    print(f"Failed to fetch daily quote: HTTP {response.status_code}")
                    return None
            except Exception as e:
                print(f"Error fetching daily quote: {e}")
                return None
        
        return self.daily_quote
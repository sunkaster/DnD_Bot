from datetime import datetime, timedelta
import requests
import random

# Quote caching system
class QuoteCache:
    def __init__(self):
        self.quotes = []
        self.last_refresh = None
        self.daily_quote = None
        self.daily_quote_date = None
    
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
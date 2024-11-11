from kiwipiepy import Kiwi
from datetime import datetime, timedelta
import spacy


class WeatherAssistant:
    def __init__(self):
        self.days_of_week = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6
        }

    def next_weekday(self, target_day):
        today = datetime.now().weekday()
        days_until = (target_day - today + 7) % 7
        days_until = days_until if days_until != 0 else 7
        return (datetime.now() + timedelta(days=days_until)).date()

    def extract_city_and_day(self, query):
        city = None
        day = None

        raise NotImplementedError(
            "This method should be implemented by the subclass.")

    def is_valid_day(self, day):
        if day is None:
            return False

        return 0 <= day <= 5


class WeatherAssistantEN(WeatherAssistant):
    def __init__(self):
        super().__init__()
        self.nlp_en = spacy.load("en_core_web_sm")

    def extract_city_and_day(self, query):
        city = None
        day = None

        query_lower = query.lower()
        doc = self.nlp_en(query)
        for ent in doc.ents:
            if ent.label_ == "GPE":
                city = ent.text
            elif ent.label_ == "DATE":
                day = ent.text.lower()
        for day_name, day_num in self.days_of_week.items():
            if day_name in query_lower:
                day = day_num
                break

        if self.is_valid_day(day):
            day = self.next_weekday(day)
        return city, day


class WeatherAssistantKR(WeatherAssistant):
    def __init__(self):
        super().__init__()
        self.kiwi = Kiwi()

        self.korean_days_of_week = {
            "월요일": 0,
            "화요일": 1,
            "수요일": 2,
            "목요일": 3,
            "금요일": 4,
            "토요일": 5,
            "일요일": 6
        }

    def process_relative_dates(self, day):
        if day == "오늘":
            return datetime.now().date()
        elif day == "내일":
            return (datetime.now() + timedelta(days=1)).date()
        elif day == "모레":
            return (datetime.now() + timedelta(days=2)).date()
        else:
            if self.is_valid_day(day):
                day = self.next_weekday(day)
                print(day)
                return day
            return False

    def extract_city_and_day(self, query: str):
        tokens = self.kiwi.analyze(query)[0][0]
        city = None
        day = None

        for token in tokens:
            word, pos = token.form, token.tag

            if pos == "NNP":
                city = word

            elif word in ["오늘", "내일", "모레"]:
                day = word

        if day is None:
            for day_name, day_num in self.korean_days_of_week.items():
                if day_name in query:
                    day = day_num
                    break
        day = self.process_relative_dates(day)
        return city, day

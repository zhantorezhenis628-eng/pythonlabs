import re
import json

class Parser():
    def __init__(self, file):
        with open(file, encoding="utf-8") as f:
            self.content = f.read()

    def parse_price(self):
        pattern = r"(?<=Стоимость\n)[\d\s]+,\d{2}"
        return re.findall(pattern, self.content)

    def parse_title(self):
        pattern = r"\d+\.\n(.+)"
        return re.findall(pattern, self.content)

    def calculate_total_amount(self):
        pattern = r"\d+\.\n"
        return len(re.findall(pattern, self.content))

    def payment(self):
        pattern = r"Банковская карта"
        match = re.search(pattern, self.content)
        return match.group(0) if match else "Unknown"

    def parse_date(self):
        pattern = r"(?<=Время:\s)(.+)"
        match = re.search(pattern, self.content)
        return match.group(1) if match else ""

    def export_to_json(self):
        data = {
            "date": self.parse_date(),
            "payment_method": self.payment(),
            "total_count": self.calculate_total_amount(),
            "items": []
        }

        titles = self.parse_title()
        prices = self.parse_price()

        for t, p in zip(titles, prices):
            data["items"].append({
                "name": t.strip(),
                "price": p.strip()
            })

        return json.dumps(data, ensure_ascii=False, indent=4)


parser = Parser("raw (1).txt")
print(parser.export_to_json())
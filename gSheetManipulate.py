import gspread
from google.oauth2.service_account import Credentials
import datetime
import os
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()


class SpreadsheetManipulation:
    MY_SHEET = os.getenv("MY_SHEET_ID")
    def __init__(self):
        """Initializes the SpreadsheetSearcher object."""

        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets"
        ]
        self.creds = Credentials.from_service_account_file("credentials.json", scopes=self.scopes)
        self.client = gspread.authorize(self.creds)
        self.sheet_id = self.MY_SHEET
        self.workbook = self.client.open_by_key(self.sheet_id)

    def row_in_workbook(self, val):

        results = {}
        worksheets = map(lambda x: x.title, self.workbook.worksheets())
        for worksh in worksheets:
            sheet = self.workbook.worksheet(worksh)
            result = sheet.find(val)
            if result:
                results = [worksh, result.row]
        #print(results)
        return results

    def next_seven_days(self):

        all_results = []
        today = datetime.date.today()
        for i in range(7):
            next_day = today + datetime.timedelta(days=i)
            next_day_formatted = next_day.strftime("%d.%m.%Y")
            results = self.row_in_workbook(next_day_formatted)
            if results: 
                all_results.append(results)
        return all_results
    
    def check_tomorrow(self):
        next_seven = self.next_seven_days()
        for one_day in next_seven:
            sheet = self.workbook.worksheet(one_day[0])
            spread_sheet_data = sheet.row_values(one_day[1])
            only_hours = spread_sheet_data[:]
            only_hours.pop(0)
            if self.can_hangout(only_hours):
                print(f'{spread_sheet_data[0]} - you can play')
            else:
                print(f'{spread_sheet_data[0]} - cant')

    def can_hangout(self, ranges):
        all_times = []
        for range in ranges:
            start, end = range.split(" - ")
            start_minutes = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
            end_minutes = int(end.split(":")[0]) * 60 + int(end.split(":")[1])
            all_times.append([start_minutes, end_minutes])

        if len(all_times) != 4:
            print("Please provide free time ranges for exactly four friends.")
            return False

        for i in __builtins__.range(len(all_times)):
            for j in __builtins__.range(i + 1, len(all_times)):
                for k in __builtins__.range(j + 1, len(all_times)):
                    for l in __builtins__.range(k + 1, len(all_times)):
                        min_end = min(all_times[i][1], all_times[j][1], all_times[k][1], all_times[l][1])
                        max_start = max(all_times[i][0], all_times[j][0], all_times[k][0], all_times[l][0])

                        common_time = min_end - max_start
                        if common_time >= 120:

        return False 

    
if __name__ == "__main__":

    searcher = SpreadsheetManipulation()
    searcher.check_tomorrow()

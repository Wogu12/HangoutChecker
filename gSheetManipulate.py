import gspread
from google.oauth2.service_account import Credentials
import datetime
from datetime import date, timedelta


class SpreadsheetManipulation:
    """A class to search for values in a Google Spreadsheet."""

    def __init__(self):
        """Initializes the SpreadsheetSearcher object."""

        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets"
        ]
        self.creds = Credentials.from_service_account_file("credentials.json", scopes=self.scopes)
        self.client = gspread.authorize(self.creds)
        self.sheet_id = "12Vu_i-ai0zecdrDnc-cSA-cQPdP2JzXo400U_M8L3ds"
        self.workbook = self.client.open_by_key(self.sheet_id)

    def row_in_workbook(self, val):
        """
        Searches for a value in all worksheets and returns a dictionary with results (excluding None values).

        Args:
            val: The value to search for.

        Returns:
            A dictionary where keys are worksheet names and values are the row numbers where the value is found (if found).
        """

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
        """
        Calculates the next 7 days and searches for them in all worksheets, returning a dictionary with results (excluding None values).

        Returns:
            A dictionary where keys are the next 7 days formatted as "%d.%m.%Y"
            and values are dictionaries containing row numbers from the `find_in_workbook` function for that day (if found).
        """

        all_results = []
        today = datetime.date.today()
        for i in range(7):
            next_day = today + datetime.timedelta(days=i)
            next_day_formatted = next_day.strftime("%d.%m.%Y")
            results = self.row_in_workbook(next_day_formatted)
            #print(results)
            if results:  # Check if any results were found for this day
                all_results.append(results)
                # all_results[next_day_formatted] = results
        #print(all_results)
        return all_results
    
    def check_tomorrow(self):
        # today = date.today()
        # tomorrow = today + timedelta(days = 1)
        next_seven = self.next_seven_days()
        # found_tomorrow = next_seven[f"{tomorrow.strftime("%d.%m.%Y")}"]
        # print(found_tomorrow)
        for one_day in next_seven:
            sheet = self.workbook.worksheet(one_day[0])
            spread_sheet_data = sheet.row_values(one_day[1])
            #print(spread_sheet_data)
            only_hours = spread_sheet_data[:]
            only_hours.pop(0)
            #self.can_hangout(only_hours)
            if self.can_hangout(only_hours):
                print(f'{spread_sheet_data[0]} - you can play')
            else:
                print(f'{spread_sheet_data[0]} - cant')
        # print(spread_sheet_data)
        # return spread_sheet_data

    def can_hangout(self, ranges):
        all_times = []
        for range in ranges:
            start, end = range.split(" - ")
            start_minutes = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
            end_minutes = int(end.split(":")[0]) * 60 + int(end.split(":")[1])
            all_times.append([start_minutes, end_minutes])

        # Check if there are exactly four ranges provided
        if len(all_times) != 4:
            print("Please provide free time ranges for exactly four friends.")
            return False  # Exit if not four ranges  

        # Iterate through all possible combinations of four time ranges
        for i in __builtins__.range(len(all_times)):
            for j in __builtins__.range(i + 1, len(all_times)):
                for k in __builtins__.range(j + 1, len(all_times)):
                    for l in __builtins__.range(k + 1, len(all_times)):
                        # Find minimum end time and maximum start time among the four
                        min_end = min(all_times[i][1], all_times[j][1], all_times[k][1], all_times[l][1])
                        max_start = max(all_times[i][0], all_times[j][0], all_times[k][0], all_times[l][0])

                        # Check if the common overlap is at least 2 hours
                        common_time = min_end - max_start
                        if common_time >= 120:
                            return True  # Overlap found, return True

        return False  # No common overlap of 2 hours found

    
if __name__ == "__main__":

    searcher = SpreadsheetManipulation()
    #data = searcher.check_tomorrow()
    searcher.check_tomorrow()
    # only_hr = data[:]
    # only_hr.pop(0)
    # if searcher.can_hangout(only_hr):
    #     print(f'{data[0]} - you can play')
    # else:
    #     print(f'{data[0]} - cant')
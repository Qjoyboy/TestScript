import argparse
import json
from collections import defaultdict

from utils.utils import Utils

class Src:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Обработка")
        self.parser.add_argument("files", nargs="+", help="Файлы")
        self.parser.add_argument("--report", required=True, help="Название отчета")
        self.args = self.parser.parse_args()

    def get_files(self):
        utility = Utils()
        res = []
        for file in self.args.files:
            res += utility.get_data(file)
        return res

    @staticmethod
    def sorted_data(data):
        sorted_dicts = [dict(sorted(i.items())) for i in data]
        return sorted(sorted_dicts, key=lambda row: row['department'])

    @staticmethod
    def beauty_view(data):
        deps = []
        print(
            f"{'id':<6}"
            f"{'name':<20}"
            f"{'email':<20}"
            f"{'hours_worked':<15}"
            f"{'rate':<5}"
            f"{'payout':<10}")

        for i in data:
            if i['department'] not in deps:
                print(f"--------{i['department']}--------")

                deps.append(i['department'])

            print(f"{i['id']:<6}"
                  f"{i['name']:<20}"
                  f"{i['email']:<20}"
                  f"{i['hours_worked']:<15}"
                  f"{i['rate']:<5}"
                  f"{i['payout']:<10}")

    def report_creator_csv(self, data):
        filename = f"report_{self.args.report}.csv"
        with open(filename, 'w', encoding='utf-8') as f:
            deps = []
            f.write(f"{'id':<6}"
            f"{'name':<20}"
            f"{'email':<20}"
            f"{'hours_worked':<15}"
            f"{'rate':<5}"
            f"{'payout':<10}\n")
            for i in data:
                line = (f"{i['id']:<6}"
                        f"{i['name']:<20}"
                        f"{i['email']:<20}"
                        f"{i['hours_worked']:<15}"
                        f"{i['rate']:<5}"
                        f"{i['payout']:<10}\n")
                if i['department'] not in deps:
                    f.write(f"\n--------{i['department']}--------\n")
                    f.write(line)
                    deps.append(i["department"])
                else:
                    f.write(line)

    def report_creator_json(self, data):
        filename = f"report_{self.args.report}.json"
        group = defaultdict(list)
        for item in data:
            dept = item['department']
            group[dept].append(item)

        group = dict(group)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(group, f, ensure_ascii=False, indent=4)









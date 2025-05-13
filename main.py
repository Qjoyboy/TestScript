import argparse

from src.src import Src
from utils.utils import Utils


def main():
    # parser = argparse.ArgumentParser(description="Обработка")
    # parser.add_argument("files", nargs="+", help = "Файлы")
    # parser.add_argument("--report", required=True, help="Название отчета")
    #
    # args = parser.parse_args()
    # utility = Utils()
    # print(f"Название отчета {args.report}")
    # res = []
    # for file in args.files:
    #     res+=utility.get_data(file)
    # for i in res:
    #     sorted_res = dict(sorted(i.items()))
    #     print(sorted_res)
    src = Src()
    res = src.get_files()
    sorted_res = src.sorted_data(res)
    args = src.parser.parse_args()
    print(f"{args.report.upper():>40}")
    src.report_creator_csv(sorted_res)
    src.report_creator_json(sorted_res)
    src.beauty_view(sorted_res)


if __name__ == "__main__":
    main()
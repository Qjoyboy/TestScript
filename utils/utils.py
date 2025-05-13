class Utils:
    def __init__(self):
        pass

    @staticmethod
    def normalize_keys(row):
        rate_case = {'hourly_rate', 'rate', 'salary'}
        normalized = {}
        for key, value in row.items():
            key_clean = key.strip().lower()
            if key_clean in rate_case:
                normalized['rate'] = value
            else:
                normalized[key_clean] = value
        return normalized

    @staticmethod
    def add_new_key(data):
        for i in data:
            i["payout"] = int(i["hours_worked"]) * int(i["rate"])


    def get_data(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        keys = lines[0].strip().split(',')
        data = []

        for line in lines[1:]:
            values = line.strip().split(',')
            row_dict = dict(zip(keys, values))
            norma = self.normalize_keys(row_dict)
            data.append(norma)

        self.add_new_key(data)

        return data
class Dict:
    @staticmethod
    def merge_two_dicts(x: dict, y: dict) -> dict:
        z = x.copy()
        z.update(y)
        return z

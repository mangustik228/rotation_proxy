

class Transformer:
    def __init__(self):
        self.main_keys = None
        self.result = {}

    def transform(self, data: list[dict]) -> dict:
        used = set()
        for datum in data:
            if (service := datum["name"]) not in used:
                self.result[service] = {
                    "count": 0,
                    "errors": []
                }
                used.add(service)
            self.add_errors_to_service(self.result[service], datum)
        return self.result

    def add_errors_to_service(self, service_dict: dict, datum: dict):
        service_dict["count"] += datum["error_count"]
        service_dict["errors"].append(
            {"id": datum["id"], "count": datum["error_count"]})


def transform_data_from_orm_dict(data: list[dict]) -> dict:
    t = Transformer()
    return t.transform(data)

import json, os


class Api:
    @staticmethod
    def call(equipment_id: int) -> dict:
        """
        Get the data of the equipment on the specified year.
        """
        # NOTE: We are using the data from a mocked JSON file.

        current_path = os.getcwd()
        api_path = os.path.join(current_path, "data", "api-response.json")
        with open(api_path, "r") as f:
            data = json.load(f)

        return data.get(str(equipment_id))

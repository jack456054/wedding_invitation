import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from typing import List, Union


class FirebaseDataFormatter:
    def __init__(self, node: str = ''):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('wedding-5f9df-cd4df1107ecf.json')

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(
            cred,
            {
                'databaseURL': 'https://wedding-5f9df-default-rtdb.asia-southeast1.firebasedatabase.app'
            },
        )

        # As an admin, the app has access to read and write all data, regradless of Security Rules
        self._ref = db.reference(node)
        self._all_data = self.get_data()

    @property
    def all_data(self) -> dict:
        return self._all_data

    @property
    def names(self) -> List[str]:
        return self.iterover_data('name')

    @property
    def messages(self) -> List[str]:
        return self.remove_newline(self.iterover_data('message'))

    @property
    def people(self) -> List[int]:
        return self.replace_empty_string(self.iterover_data('people'))

    @property
    def young_people(self) -> List[int]:
        return self.replace_empty_string(self.iterover_data('youngPeople'))

    @property
    def vege_people(self) -> List[int]:
        return self.replace_empty_string(self.iterover_data('vegePeople'))

    def people_summary(self) -> str:
        return f'''總人數: {sum(self.people + self.young_people)}
大人: {sum(self.people)}
小孩: {sum(self.young_people)}
素食人數: {sum(self.vege_people)}'''

    def message_summary(self) -> str:
        result = ''
        for name, message in zip(self.names, self.messages):
            result += f'{name} 說: {message}\n' if message else f'{name} 說: (無)\n'
        return result

    def iterover_data(self, fieldname: str) -> Union[List[str], List[int]]:
        fields_value: Union[List[str], List[int]] = list()
        for name, people in self._all_data.items():
            for person in people.values():
                fields_value.append(person[fieldname])
        return fields_value

    def get_data(self) -> dict:
        return self._ref.get()

    def remove_newline(
        self, value_list: Union[List[str], List[int]]
    ) -> Union[List[str], List[int]]:
        result_list: Union[List[str], List[int]] = list()
        for value in value_list:
            result_list.append(value.replace('\n', ''))
        return result_list

    def replace_empty_string(self, string_list: List[str]) -> List[int]:
        return [int(x) if x else 0 for x in string_list]


if __name__ == "__main__":
    invitation = FirebaseDataFormatter('invitation')
    print(invitation.people_summary())
    print(invitation.message_summary())

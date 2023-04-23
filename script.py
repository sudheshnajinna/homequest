import json
from travello.models import Apartment

with open('apartments.json') as f:
    data = json.load(f)

for apartment_data in data:
    apartment = Apartment(
        ApartmentID=apartment_data['ApartmentID'],
        Name=apartment_data['Name'],
        Type=apartment_data['Type'],
        Address=apartment_data['Address'],
        Image=apartment_data['Image'],
        Beds=apartment_data['Beds'],
        Bath=apartment_data['Bath'],
        Rent=apartment_data['Rent'],
        Area=apartment_data['Area'],
        Furnished=apartment_data['Furnished'],
        Parking=apartment_data['Parking'],
        Pool=apartment_data['Pool'],
        Gatedcommunity=apartment_data['Gatedcommunity'],
        Patio=apartment_data['Patio'],
        Garden=apartment_data['Garden'],
        HardwoodFloors=apartment_data['HardwoodFloors'],
        Gym=apartment_data['Gym'],
        DisabilityAccess=apartment_data['DisabilityAccess'],
        Kidfriendly=apartment_data['Kidfriendly'],
        Washerdryer=apartment_data['Washerdryer'],
        Dishwasher=apartment_data['Dishwasher'],
        Radius=apartment_data['Radius'],
    )
    apartment.save()

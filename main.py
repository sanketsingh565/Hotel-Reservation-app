import datetime
import pandas


class User:
    def __init__(self, user_id, first_name, last_name):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.user_id}: {self.first_name} {self.last_name}"


class Hotel:
    def __init__(self, hotel_id, hotel_name, city, capacity, available):
        self.hotel_id = hotel_id
        self.name = hotel_name
        self.city = city
        self.capacity = capacity
        self.available = available

    def book(self):
        self.available = False

    def unbook(self):
        self.available = True

    def __str__(self):
        return f"Hotel ID: {self.hotel_id} Name: {self.name} City: {self.city} Capacity: {self.capacity}"

class HotelSpa(Hotel):
    def __init__(self, hotel_id, hotel_name, city, capacity, available, is_spa):
        super().__init__(hotel_id, hotel_name, city, capacity, available)
        self.is_spa = is_spa
        print("You have booked a spa.")


class Ticket:
    def __init__(self, hotel, user_name):
        self.hotel = hotel
        self.user_name = user_name

    def generate(self):
        print(f"Hotel {self.hotel.name} booked for {self.user_name}")


class SpaTicket:
    def __init__(self, hotel, user_name):
        self.hotel = hotel
        self.user_name = user_name

    def generate(self):
        print(f"Spa {self.hotel.name} booked for {self.user_name}")


class CreditCard:
    def __init__(self, number, expiration, holder, cvc):
        self.number = number
        self.expiration = expiration
        self.holder = holder.title()
        self.cvc = cvc

    def __str__(self):
        return f"{self.number} {self.expiration} {self.holder} {self.cvc}"

    def validate(self):
        print("Validating card.")
        card = None
        try:
            card = [card for card in card_list if card.holder == self.holder
                    and f"{card.number}" == f"{self.number}"
                    and f"{card.cvc}" == f"{self.cvc}"
                    and f"{card.expiration}" == f"{self.expiration}"][0]
        except IndexError as error:
            pass
        if card is not None:
            return True
        else:
            return False


class SecureCard(CreditCard):
    def check_password(self, given_password):
        print("Validating password.")
        password = security_dataframe.loc[security_dataframe["number"] == int(self.number), "password"].squeeze()
        try:
            if password == given_password:
                return True
            else:
                return False
        except Exception as error:
            return False

def create_hotels():
    hotels = []
    for index, row in hotel_dataframe.iterrows():
        hotel_id = row["id"]
        hotel_name = row["name"]
        city = row["city"]
        capacity = row["capacity"]
        available = row["available"]
        temp_hotel = Hotel(hotel_id, hotel_name, city, capacity, available)
        hotels.append(temp_hotel)
    return hotels


def create_users():
    users = []
    for index, row in user_dataframe.iterrows():
        user_id = row["user_id"]
        first_name = row["first_name"]
        last_name = row["last_name"]
        user = User(user_id, first_name, last_name)
        users.append(user)
    return users


def create_cards():
    cards = []
    for index, card in card_dataframe.iterrows():
        card_number = card["number"]
        card_expiration = card["expiration"]
        card_holder = card["holder"]
        card_cvc = card["cvc"]
        card = CreditCard(card_number, card_expiration, card_holder, card_cvc)
        cards.append(card)
    return cards


def print_hotels(hotels):
    hotel_count = 1
    for index, hotel in enumerate(hotels):
        if hotel.available == "yes":
            print(f"{hotel_count}. {hotel}")
            hotel_count = hotel_count + 1


if __name__ == "__main__":
    hotel_dataframe = pandas.read_csv("files/hotels.csv")
    user_dataframe = pandas.read_csv("files/users.csv")
    card_dataframe = pandas.read_csv("files/cards.csv")
    security_dataframe = pandas.read_csv("files/card_security.csv")

    user = None
    user_list = create_users()
    hotel_list = create_hotels()
    card_list = create_cards()

    while True:
        try:
            user_type = input("Hello, are you an existing or new users: \n1. Existing\n2. New\nPlease choose: ")
            user_type = int(user_type)
            if user_type == 1 or user_type == 2:
                break
            print("Please enter a valid choice.")
        except Exception as error:
            print("Please enter a valid choice.")

    if user_type == 1:
        while True:
            try:
                user_id = input("Please enter your user ID: ")
                user_id = int(user_id)
                user = [user for user in user_list if user.user_id == user_id][0]
                if user is not None:
                    break
                print("Please enter an existing ID.")
            except Exception as error:
                print("Please enter an existing ID.")

    elif user_type == 2:
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        user = User(user_id=len(user_dataframe.index) + 1, first_name=first_name, last_name=last_name)
        user_list.append(user)
        new_dataframe = pandas.DataFrame({"user_id": [user.user_id],
                                          "first_name": [user.first_name],
                                          "last_name": [user.last_name]})

        user_dataframe = pandas.concat([user_dataframe, new_dataframe])
        user_dataframe.to_csv("files/users.csv", index=False)

    print(f"Welcome {user.first_name}! Which hotel would you like to book: ")
    print_hotels(hotel_list)

    while True:
        try:
            booked_id = int(input("State the ID of the hotel you would like to book: "))
            booked_hotel = [hotel for hotel in hotel_list if
                            hotel.hotel_id == booked_id and hotel.available == "yes"][0]
            if booked_hotel is not None:
                break
            print("Please enter a valid ID")
        except Exception as error:
            print("Please enter a valid ID")

    credit_number = input("Please enter your credit card number: ")
    credit_expiration = input("Please enter your credit card expiration date: ")
    credit_holder = input("Please enter the holder of the credit card: ")
    credit_cvc = input("Please enter the cvc of the credit card: ")
    credit_password = input("Please enter the credit card password: ")

    credit_card = SecureCard(credit_number, credit_expiration, credit_holder, credit_cvc)
    if credit_card.validate() and credit_card.check_password(credit_password):
        booked_hotel.book()
        hotel_dataframe.loc[hotel_dataframe["id"] == booked_hotel.hotel_id, "available"] = "no"
        hotel_dataframe.to_csv("files/hotels.csv", index=False)

        full_name = user.get_full_name()
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")

        user_hotel_dataframe = pandas.read_csv("files/user_hotel.csv")
        new_user_hotel_dataframe = pandas.DataFrame({"user_id": [user.user_id],
                                                     "hotel_id": [booked_hotel.hotel_id],
                                                     "date": [current_date]})
        user_hotel_dataframe = pandas.concat([user_hotel_dataframe, new_user_hotel_dataframe])
        user_hotel_dataframe.to_csv("files/user_hotel.csv", index=False)

        ticket = Ticket(booked_hotel, full_name)
        ticket.generate()
        spa_book = input("Do you want to book a spa: ")
        if spa_book == "yes":
            spa_hotel = HotelSpa(booked_hotel.hotel_id, booked_hotel.name, booked_hotel.city, booked_hotel.capacity,
                                 "yes", "yes")
            spa_ticket = SpaTicket(spa_hotel, full_name)
            spa_ticket.generate()
    else:
        print("Error, card not valid.")

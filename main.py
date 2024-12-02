import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id":str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """ Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """ Checks if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        return availability == "yes"


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass

class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel Name: {self.hotel.name}
        """
        return content

class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number":self.number, "expiration": expiration,
                     "holder":holder, "cvc": cvc}
        return card_data in df_cards

    def is_valid(self):
        return self.validate(expiration="12/26", holder="JOHN SMITH", cvc="123")


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False





class SPAReservation:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate_spa(self):
        content = f"""
        Thank you for your SPA reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel Name: {self.hotel.name}
        """
        return content


# program main loop
print(df)

hotel_ID = input("Enter the id of the hotel: ")
hotel = SpaHotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.is_valid():
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
            choice_spa = input("Do you want a spa package?")
            if choice_spa == "yes":
                hotel.book_spa_package()
                spa = SPAReservation(customer_name=name, hotel_object=hotel)
                print(spa.generate_spa())
        else:
            print("Credit card authentication failed.")
    else:
        print("There was a problem with your payment")
else:
    print("Hotel is not free.")
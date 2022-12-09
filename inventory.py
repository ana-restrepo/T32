# This program is a stock management system which keeps stock information on a text file.
# Sources for research applied on this program can be found at the end of this file.

# =========== Import libraries ===============
# Import OS module. See Source 1.
import os

# Import pycountry module. Requires installation of pycountry package. See sources 2 and 3.
import pycountry

# Import tabulate module. Requires installation of tabulate package. See source 4.
from tabulate import tabulate

# Import string module. See source 5.
import string


# ======== The beginning of the class ==========
# Definition of class Shoe.
class Shoe:

    # Initialize 5 instance variables.
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Function to get the cost of the object.
    def get_cost(self):
        return self.cost

    # Function to get the quantity of the object.
    def get_quantity(self):
        return self.quantity

    # Function to get the object's information as a string.
    def __str__(self):
        return f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}"

    # Function to get the total value of the item.
    def get_total_value(self):
        return int(self.cost) * int(self.quantity)


# =============Shoe list===========
# The list will be used to store a list of objects of shoes.
shoe_list = []


# ==========Functions outside the class==============

# Function to check the inventory file has the right format.
# This function takes in a list.
def check_file(file_list):

    # Declare variables.
    error_description = "\nErrors in the file inventory.txt:"
    errors = False
    description = []

    # Check if the file is empty. If so, change 'errors' to True and add message to error description.
    if not file_list:
        errors = True
        error_description += "\n\nThis file is empty."

    else:
        # If the list is not empty, check its format line by line.
        for line_count, line in enumerate(file_list):

            # Check that line 0 contains the titles. If not, tell the user to move any product data one line down.
            if line_count == 0 and line == "Country,Code,Product,Cost,Quantity\n":
                continue
            elif line_count == 0 and line != "Country,Code,Product,Cost,Quantity\n":
                errors = True
                error_description += "\n\nLine 1 should be equal to: 'Country,Code,Product,Cost,Quantity'." \
                                     "\nAny product information on line 1 will be ignored by the program."

            # For all the other lines in the list:
            # Check if they have empty fields and if fields cost and quantity are numbers.
            # If errors are found, add the line and field numbers to the line_description list.
            else:
                line = line.strip("\n").split(",")

                line_errors = False
                line_description = {"line": str(line_count + 1), "empty fields": [], "not number": []}

                for item_count, item in enumerate(line):
                    if item == "":
                        line_errors = True
                        line_description["empty fields"].append(str(item_count + 1))

                    if item_count == 3 or item_count == 4:
                        if not item.isdigit():
                            line_errors = True
                            line_description["not number"].append(str(item_count + 1))

                # Add information in line_description list to the error description.
                if line_errors:
                    errors = line_errors
                    description.append(line_description)

        # Format the error message for printing.
        for item in description:
            error_description += f"\n\nLine: {item['line']}"
            if item["empty fields"]:
                error_description += f"\n\tEmpty fields: {', '.join(item['empty fields'])}"
            if item["not number"]:
                error_description += f"\n\tValue is not a number: {', '.join(item['not number'])}"

    # This function returns a list two values:
    # Position 0: a boolean value indicating if there are errors in the list format.
    # Position 1: a string containing a detailed error message, formatted for print.
    return [errors, error_description]


# Function to read the inventory file.
def read_shoes_data():

    # Create inventory_list.
    inventory_list = []

    # Declare variable to exit import function.
    quit_import = False

    while True:

        # Check if the user has chosen to exit the program and, if so, break the loop.
        if quit_import:
            break

        # Look for the file 'inventory.txt' in the program's directory.
        try:
            # If the file is found, store its content on a list of lines and call the function to check its format.
            with open("inventory.txt", "r") as inventory_file:
                temp_list = inventory_file.readlines()
                file_errors = check_file(temp_list)

                # If errors have been found, print the error description for the user to fix them.
                if file_errors[0]:
                    print(file_errors[1])

                # If the file format is correct, create a Shoe object per each file line, skipping the first one.
                # Append each object to a list.
                else:
                    for line in temp_list[1: len(temp_list)]:
                        line = line.strip("\n").split(",")
                        inventory_list.append(Shoe(line[0], line[1], line[2], line[3], line[4]))

                    # This function returns a list of Shoe objects, if the file is found and in the right format.
                    return inventory_list

        # If the file is not found, print an error message.
        except FileNotFoundError:
            print(f"File 'inventory.txt' was not found.\n")

        # Ask the user if they want to try to find the file again or exit the program.
        while True:
            selection = input(f"\nPlease save the file 'inventory.txt' in {os.getcwd()}, using the correct format. "
                              f"\nWhen ready, enter 'done' to try again or 'quit' to exit the program: ").lower()

            # If user types 'done' break this loop to search again for the file.
            if selection == "done":
                break

            # If the user enters 'quit' print a message and exit the loop and the program.
            elif selection == "quit":
                quit_import = True
                print("Goodbye")
                break

            # If the users enters anything else, print an error message and ask them to choose again.
            else:
                print("Invalid selection.")


# Function to check if a value can be cast as a float.
# This function takes in a string and returns a boolean value.
def is_float(input_data):

    try:
        float(input_data)
        return True

    except ValueError:
        return False


# Function to ask user to enter a country name and validate it exists.
def validate_country():

    # Define list of characters not in country names.
    forbidden_characters = ["/", "\\", '"', "'", "*", ";", "-", "?", "[", "]", "(", ")", "~", "!", "$", "{", "}", "&lt",
                            ">", "#", "@", "&", "|", "\n", "\t"]

    # Ask user to enter a country name. Check the input is not empty, a number or a special character.
    while True:
        country = input("\nPlease enter the Country name: ")

        if country == "" or country == " " or country == "\t" or country == "\n":
            print("Entry is empty.")

        elif country.isdigit():
            print("Entry is a number not a country.")

        elif country in forbidden_characters:
            print("Invalid entry.")

        else:
            country_options_dict = {}
            country_options_table = []

            # With 'search_fuzzy', look for countries similar to the user's entry and store objects in a list.
            search_results = pycountry.countries.search_fuzzy(country)

            # Search for the name variable for each result and save it with its position in a list and a dictionary.
            for counter, result in enumerate(search_results):
                position = str(counter + 1)
                entry = result.name
                country_options_dict[position] = entry
                country_options_table.append([position, entry])

            # Check if the dictionary with the search results is empty, if so assign false to 'valid_country'.
            if not country_options_dict:
                valid_country = False

            # If there has been only one match for the search:
            # Ask user to confirm selection and assign True to 'valid_country'.
            elif len(country_options_dict) == 1:
                print(f"The only match for your entry is: {country_options_dict['1']}.")
                while True:
                    verification = input("\nDo you want to confirm this selection? (y/n): ").lower()
                    if verification == "y":
                        country = country_options_dict["1"]
                        valid_country = True
                        break
                    elif verification == "n":
                        valid_country = False
                        break
                    else:
                        print("Invalid selection.")

            # Otherwise, use tabulate to organize and print the search results.
            else:
                print(tabulate(country_options_table, headers=["No.", "Country"], tablefmt="pretty"))

                # Ask the user to enter a number to select a country.
                # If it is in the results' dictionary, assign its value to 'country' and True to 'valid_country'.
                while True:
                    number = input("\nPlease select a country from the table by entering the number: ")
                    if number in country_options_dict.keys():
                        valid_country = True
                        country = country_options_dict[number]

                        # If the country name contains a ',' replace it with '-'.
                        # This is to avoid issues when processing the file where ',' is the separator.
                        if ", " in country:
                            country = country.replace(", ", " - ")
                        print(f"You have selected: {string.capwords(country)}.")
                        break

                    else:
                        print("Invalid entry.")

            # Check the value of valid country, if True print country and return its value.
            # Else print error message and restart the process.
            if valid_country:
                return country

            else:
                print(f"No country found.")


# Function to create a new Shoe object from information entered by the user.
# This function takes in a list of Shoe objects.
def capture_shoes(inventory_list):

    # Call the function to ask the user to enter a country and validate it exists.
    country = validate_country()

    # Call the function to ask the user to enter a code and validate it is entered in the right format.
    product_code = validate_sku()

    # Ask the user to enter the product name.
    # Validate that th input is not empty and that the name is between 1 and 140 characters long.
    while True:
        product_name = input("\nPlease enter the product name: ")

        if product_name == "" or product_name == " ":
            print("Product name cannot be empty.")

        elif 0 < len(product_name) <= 140:
            break

        else:
            print("Please enter a valid product name (Max. 140 characters). ")

    # Ask the user to enter the price.
    # Validate that the user input is not empty and is a positive integer or a positive float.
    while True:
        product_cost = input("\nPlease enter the product cost: ")

        if product_cost == "":
            print("Product cost cannot be empty.")

        elif product_cost.isdigit():
            product_cost = int(product_cost)
            break

        elif "-" not in product_cost and is_float(product_cost):
            product_cost = float(product_cost)
            break

        else:
            print("Please enter a valid product cost (Must be a positive number). ")

    # Ask the user to enter the quantity.
    # Validate that the user input is not empty and is a positive integer.
    while True:
        product_qty = input("\nPlease enter the product quantity: ")

        if product_qty == "":
            print("Product quantity cannot be empty.")

        elif product_qty.isdigit():
            product_qty = int(product_qty)
            break

        else:
            print("Please enter a valid product quantity (Must be a positive number). ")

    # Create a new Shoe object with the information collected and append it to the shoe list.
    inventory_list.append(Shoe(country, product_code, string.capwords(product_name), product_cost, product_qty))

    # Print the new object's information.
    table_headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    table_content = [[country, product_code, string.capwords(product_name), product_cost, product_qty]]

    print(tabulate(table_content, headers=table_headers, tablefmt="pretty"))

    # Construct a string with the new object information and overwrite the 'inventory.txt' file.
    file_info = "Country,Code,Product,Cost,Quantity"
    for shoe in inventory_list:
        file_info += "\n" + shoe.__str__().strip("\n").replace(", ", ",")

    with open("inventory.txt", "w") as file:
        file.write(file_info)

    # Print a message announcing the task has been completed.
    print("New inventory item has been added to 'inventory.txt'.")

    # This function returns a list of Shoe objects with the new object in index -1.
    return inventory_list


# Function to ask the user to enter a code and validate it is entered in the right format.
def validate_sku():

    # Ask the user to enter the product code.
    # Validate that the input is not empty, that the first three characters are 'SKU' and the last 5 are numbers.
    while True:
        product_code = input("\nPlease enter the product code: ").upper()

        if product_code == "":
            print("Product code cannot be empty.")

        elif product_code[0:3] == "SKU" and product_code[3:8].isdigit() and len(product_code) == 8:
            break

        else:
            print("Please enter a valid product code (Correct format: SKU#####). ")
    return product_code


# Function to see all the Shoes in the inventory.
# This function takes in a list of Shoe objects.
def view_all(inventory_list):

    # Create a list of headers and a list for the rows on the table.
    # To fill the 'table_content' list loop through the object list exacting the information of each Shoe.
    table_headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    table_content = []

    for product in inventory_list:
        table_content.append(product.__str__().strip("\n").split(", "))

    # Print the information in a table.
    print(f"\n{tabulate(table_content, headers=table_headers, tablefmt='pretty')}")


# Function to find the item(s) with the lowest quantity and add more stock.
# This function takes in a list of Shoe objects.
def re_stock(inventory_list):

    lowest_qty = []

    # For each object on the list find their position and quantity.
    # Compare the quantity of each item with the quantity of the items in 'lowest_qty'.
    # If equal, append position and quantity. If lower, replace values on the list with the new position and quantity.
    for position, product in enumerate(inventory_list):
        qty = int(product.get_quantity())
        if position != 0:
            if lowest_qty[0][1] == qty:
                lowest_qty.append([position, qty])
            elif lowest_qty[0][1] > qty:
                lowest_qty = [[position, qty]]
        else:
            lowest_qty.append([position, qty])

    # Create a list with headers and an empty dictionary which will be used to create a table.
    table_headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    table_content = {}

    # From the 'inventory_list', find the objects identified in the 'lowest_qty' list.
    # To 'table_content' add the position as the key and the object's values as a list.
    for counter, item in enumerate(lowest_qty):
        table_content[item[0]] = inventory_list[item[0]].__str__().strip("\n").split(", ")

    # Print information of products with the lowest quantities on a table.
    print(f"\nItems with lowest quantities:"
          f"\n{tabulate(table_content.values(), headers=table_headers, tablefmt='pretty')}")

    # For each item with low quantity ask the user if they want to add stock.
    quantities_change = False
    for item in table_content:
        while True:
            selection = input(f"\nProduct Code: {table_content[item][-4]}"
                              "\nWould you like to restock this item? (y/n): ").lower()

            # If the user selects 'y' ask for the quantity they'd like to add.
            # If the user enters a number: change the quantity in the object list and the table content dictionary.
            if selection == "y":
                while True:
                    qty_increase = input("\nPlease enter the quantity you would like to add: ")

                    if qty_increase.isdigit():
                        inventory_list[item].quantity = int(table_content[item][-1]) + int(qty_increase)
                        table_content[item][-1] = int(table_content[item][-1]) + int(qty_increase)
                        quantities_change = True
                        break

                    # Print an error message if the user does not enter a number.
                    else:
                        print("Invalid entry. Please enter a number.")
                break

            # If the user selects 'n' let them know the quantity will remain the same.
            elif selection == "n":
                print(f"Quantity for product {table_content[item][-4]} won't be changed.")
                break

            # If the user enters something other than 'y' or 'n' print an error message.
            else:
                print("Invalid entry.")

    if quantities_change:
        # Show the user the quantities of the items after they have been changed.
        print(f"\nNew quantities:"
              f"\n{tabulate(table_content.values(), headers=table_headers, tablefmt='pretty')}")

        # Construct a string with the new object information and overwrite the 'inventory.txt' file.
        file_info = "Country,Code,Product,Cost,Quantity"
        for shoe in inventory_list:
            file_info += "\n" + shoe.__str__().strip("\n").replace(", ", ",")

        with open("inventory.txt", "w") as file:
            file.write(file_info)

        # Print a message announcing the task has been completed.
        print("Stock quantities have been updated in 'inventory.txt'.")


# Function to search for a product's information by entering its sku code.
# This function takes in a list of Shoe objects.
def search_shoe(inventory_list):

    # Create a list of shoes from 'inventory_list', where the info of each product is a list.
    shoes = []
    for item in inventory_list:
        shoes.append(item.__str__().strip("\n").split(", "))

    # Call function to ask the user to enter a code and validate it is entered in the right format.
    shoe_search = validate_sku()

    table_headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    table_content = []
    shoe_codes = []

    while True:

        # Create a list of the sku codes in the shoes list.
        for shoe in shoes:
            shoe_codes.append(shoe[1])

        # Check for the code entered by the user in the list of codes in stock.
        # If it is on the list, look for all the entries for that code and return their info to be printed.
        if shoe_search in shoe_codes:
            for shoe in shoes:
                if shoe_search == shoe[1]:
                    table_content.append(shoe)
            return tabulate(table_content, headers=table_headers, tablefmt="pretty")

        # If the code is not on the list, ask the user if they want to add this shoe to the inventory.
        else:
            while True:
                selection = input("The code entered is not in stock. "
                                  "Would you like to add this item to the inventory (y/n)?: ").lower()

                # If the user selects 'y', call the function to add the shoe to inventory and update the 'shoes' list.
                if selection == "y":
                    inventory_list = capture_shoes(inventory_list)
                    shoes = []
                    for item in inventory_list:
                        shoes.append(item.__str__().strip("\n").split(", "))

                    table_content.append(inventory_list[-1].__str__().strip("\n").split(", "))
                    return tabulate(table_content, headers=table_headers, tablefmt="pretty")

                # If the user enters 'n', ask them to if they want to search for a different code.
                elif selection == "n":

                    while True:
                        user_choice = input("\nWould you like to look for a different product? (y/n): ").lower()

                        # If they answer yes, ask for a new code and validate it.
                        if user_choice == "y":
                            print("Please enter a different product code.")
                            shoe_search = validate_sku()
                            break

                        # If they answer no, exit the function and return a message.
                        elif user_choice == "n":
                            return f"None. Code {shoe_search} not in database."
                        else:
                            print("Invalid selection.")
                    break

                else:
                    print("Invalid selection.")


# Function to calculate and display the total value of each item in stock.
# This function takes in a list of Shoe objects.
def value_per_item(inventory_list):

    table_headers = ["Code", "Product", "Total Value"]
    table_content = []

    # For each shoe object on the list add their code, name and total value to the 'table_content' list.
    for shoe in inventory_list:
        table_content.append([shoe.code, shoe.product, shoe.get_total_value()])

    # Print a table with the information collected above.
    print(f"\nTotal value of items in stock:\n{tabulate(table_content, headers=table_headers, tablefmt='pretty')}")


# Function to find the item(s) with the highest quantity and put them on sale.
# This function takes in a list of Shoe objects.
def highest_qty(inventory_list):

    highest_quantity = []

    # For each object on the list find their position and quantity.
    # Compare the quantity of each item with the quantity of the items in 'highest_quantity'.
    # If equal, append position and quantity. If higher, replace values on the list with the new position and quantity.
    for position, product in enumerate(inventory_list):
        qty = int(product.get_quantity())
        if position != 0:
            if highest_quantity[0][1] == qty:
                highest_quantity.append([position, qty])
            elif highest_quantity[0][1] < qty:
                highest_quantity = [[position, qty]]
        else:
            highest_quantity.append([position, qty])

    # Create a list with headers and an empty dictionary which will be used to create a table.
    table_headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    table_content = {}

    # From the 'inventory_list', find the objects identified in the 'highest_quantity' list.
    # To 'table_content' add the position as the key and the object's values as a list.
    for counter, item in enumerate(highest_quantity):
        table_content[item[0]] = inventory_list[item[0]].__str__().strip("\n").split(", ")

    # Print information of products with the highest quantities on a table.
    print(f"\nItems with highest quantities:"
          f"\n{tabulate(table_content.values(), headers=table_headers, tablefmt='pretty')}")

    # For each item with high quantity ask the user if they want to put on sale (reduce price).
    price_change = False

    for item in table_content:
        while True:
            selection = input(f"\nProduct Code: {table_content[item][-4]}\t\t\tPrice: {table_content[item][-2]}"
                              "\nWould you like to put this item on sale? (y/n): ").lower()

            # If the user selects 'y' ask for the new price.
            # If the user enters a lower number: change the price in the object list and the table content dictionary.
            if selection == "y":
                while True:
                    sale_price = input("\nPlease enter the new price: ")

                    if sale_price.isdigit() and int(sale_price) < int(table_content[item][-2]):
                        inventory_list[item].cost = int(sale_price)
                        table_content[item][-2] = int(sale_price)
                        price_change = True

                        # Add (ON SALE) to the product's name.
                        if " (ON SALE)" not in inventory_list[item].product:
                            inventory_list[item].product += " (ON SALE)"
                            table_content[item][-3] += " (ON SALE)"
                        break

                    # Print an error message if the user does not enter a lower number.
                    else:
                        print("Invalid entry. Please enter a number that is lower than the current price.")
                break

            # If the user selects 'n' let them know the price will remain the same.
            elif selection == "n":
                print(f"Price for product {table_content[item][-4]} won't be changed.")
                break

            # If the user enters something other than 'y' or 'n' print an error message.
            else:
                print("Invalid entry.")

    if price_change:
        # Show the user the prices of the items after they have been changed.
        print(f"\nNew prices:"
              f"\n{tabulate(table_content.values(), headers=table_headers, tablefmt='pretty')}")

        # Construct a string with the new object information and overwrite the 'inventory.txt' file.
        file_info = "Country,Code,Product,Cost,Quantity"
        for shoe in inventory_list:
            file_info += "\n" + shoe.__str__().strip("\n").replace(", ", ",")

        with open("inventory.txt", "w") as file:
            file.write(file_info)

        # Print a message announcing the task has been completed.
        print("Sale prices have been updated in 'inventory.txt'.")


# ==========Main Menu=============

# Print welcome message.
print("\nWelcome to our Stock Management System!")

while True:

    # Call function to create a list of Shoe objects from the 'inventory.txt' file.
    shoe_list = read_shoes_data()

    # Display menu options and ask the user to select one.
    menu_option = input("\nPlease select one of the following options:\n"
                        "\n\tC\t-\tCapture new shoe"
                        "\n\tVA\t-\tView all shoes"
                        "\n\tR\t-\tRe-Stock (Increase qty)"
                        "\n\tS\t-\tSearch shoe"
                        "\n\tVI\t-\tValue per item"
                        "\n\tH\t-\tHighest stock (Put ON SALE)"
                        "\n\tQ\t-\tQuit\n").upper()

    # If user selects 'C', call the function to add a new shoe to stock.
    if menu_option == "C":
        capture_shoes(shoe_list)

    # If user selects 'VA', call the function to print the whole inventory on a table.
    elif menu_option == "VA":
        view_all(shoe_list)

    # If the user selects 'R', call the function to find the item(s) with lowest qty and increase the qty.
    elif menu_option == "R":
        re_stock(shoe_list)

    # If the user selects 'S', call the function to search for a product code and print the corresponding information.
    elif menu_option == "S":
        print(f"\nSearch results:\n{search_shoe(shoe_list)}")

    # If the user selects 'VI', find the total value of each item in stock and display it on a table.
    elif menu_option == "VI":
        value_per_item(shoe_list)

    # If the user selects 'H', call the function to find the item(s) with highest qty and decrease the cost.
    elif menu_option == "H":
        highest_qty(shoe_list)

    # If the user selects 'Q', exit the program.
    elif menu_option == "Q":
        print("Goodbye!")
        break

    # If the user enters anything else, print an error message.
    else:
        print("Invalid selection.")


""" ========== Sources ============
Source 1: https://www.w3schools.blog/python-files-io
After searching for the inventory file and not finding it, I wanted to show the user where they should save the file.
That way the user can put the file where it should be and indicate to the program to search again.
To achieve this, I used the method os.getcwd() to find and print the current working directory.

Source 2: https://pypi.org/project/pycountry/
I wanted to verify that the user entered a country which existed when creating a new Shoe object. 
So, I used the pycountries package to compare the user's input to a list of countries, 
and ask the user to select an option from the search results.

Source 3: https://towardsdatascience.com/matching-country-information-in-python-7e1928583644
After finding out about the pycountry package, I used the information on the website above to install it.

Source 4: https://pypi.org/project/tabulate/
I used the information in the lik above to familiarize myself with what the tabulate module offers.
I used the tabulate module to organize the results of the pycountries search_fuzzy in a list, 
so the user could clearly see the options available and select one of the countries from the table.

Source 5: https://www.geeksforgeeks.org/python-string-capwords-method/
I used the string module to access the capwords method.
This to format a sentence entered by the user with a capital letter at the beginning of every word.

"""

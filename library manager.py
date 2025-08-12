import json

books = {
    "book_id_001": {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "available": True,
        "borrowed_by": None
    }
}

users = {
    "user_001": {
        "name": "Alice",
        "borrowed_books": ["book_id_001"]
    }
}

def generate_user_id():
    return f"user_{len(users) + 1:03d}"

def generate_books_id():
    return f"book_id_{len(books) + 1:03d}"

print("✨ Welcome to Library Management System ✨".center(80))

while True:
    print("\n📋 Menu:")
    print("1. 📖 Add Book")
    print("2. 🧑 Register User")
    print("3. 📚 Borrow Book")
    print("4. 🔁 Return Book ")
    print("5. 🔍 Search Books")
    print("6. 💾 Save to File")
    print("7. 📂 Load from File")
    print("8. 🧮 Display Stats")

    try:
        choice = int(input("\nWhat would you like to do today?\nPlease enter your choice ---> "))
    except ValueError:
        print("❌ Please enter a valid number.\n")
        continue

    if choice == 1:
        # Add Book
        while True:
            book_name = input("What is the book's name you want to add❓ ---> ").strip().lower()
            if not book_name:
                print("The name of the book cannot be empty❌. Try again.\n")
            else:
                break

        while True:
            author_name = input(f"What is the name of {book_name}'s author❓ ---> ").strip()
            if not author_name:
                print("The author's name cannot be empty❌.\n")
            elif not author_name.replace(" ", "").isalpha():
                print("The author name cannot contain digits or special characters❌.\n")
            else:
                break

        while True:
            year_input = input(f"In what year was {book_name} published❓ ")
            if not year_input:
                print("Publication year cannot be empty❌.\n")
            elif not year_input.isdigit():
                print("Publication year must contain only digits❌.\n")
            else:
                year = int(year_input)
                break

        while True:
            yes_no = input(f"Is {book_name} currently available? (yes/no): ").strip().lower()
            if yes_no == "yes":
                book_id = generate_books_id()
                books[book_id] = {
                    "title": book_name,
                    "author": author_name,
                    "year": year,
                    "available": True,
                    "borrowed_by": None
                }
                print(f"✅ {book_name} has been added successfully with ID {book_id}.\n")
                break
            elif yes_no == "no":
                borrower_id = input("Who is it borrowed to? Enter borrower ID: ").strip().lower()
                if not borrower_id:
                    print("This cannot be empty❌.\n")
                elif borrower_id not in users:
                    print("❌ This user ID does not exist. Try again.\n")
                else:
                    book_id = generate_books_id()
                    books[book_id] = {
                        "title": book_name,
                        "author": author_name,
                        "year": year,
                        "available": False,
                        "borrowed_by": borrower_id
                    }
                    users[borrower_id]["borrowed_books"].append(book_id)
                    print(f"✅ {book_name} has been added and marked as borrowed by {borrower_id}.\n")
                    break
            else:
                print("❌ Please answer with yes or no.\n")

    elif choice == 2:
        # Register User
        while True:
            user_name = input("What is the name of the new user❓ ").strip()
            if not user_name:
                print("This entry cannot be empty❌.\n")
            elif not user_name.replace(" ", "").isalpha():
                print("The name cannot contain digits or special characters❌.\n")
            else:
                break

        user_id = generate_user_id()
        borrowed_books = []

        while True:
            yes_no = input("Has this user already borrowed a book❓ (yes/no): ").strip().lower()
            if yes_no == "yes":
                try:
                    number_of_books = int(input(f"How many books did {user_name} borrow❓ "))
                    for i in range(number_of_books):
                        while True:
                            book_name_or_id = input(f"Enter book #{i+1} name or ID: ").strip().lower()
                            found = False
                            for book_id, book_info in books.items():
                                if book_name_or_id == book_id.lower() or book_name_or_id == book_info["title"].lower():
                                    borrowed_books.append(book_id)
                                    books[book_id]["available"] = False
                                    books[book_id]["borrowed_by"] = user_id
                                    print(f"✅ {book_info['title']} added to borrowed list.\n")
                                    found = True
                                    break
                            if found:
                                break
                            else:
                                print("❌ Book not found. Try again.\n")
                    break
                except ValueError:
                    print("❌ Invalid number. Try again.\n")
            elif yes_no == "no":
                print("Okay, no books borrowed.\n")
                break
            else:
                print("❌ Please answer with yes or no.\n")

        users[user_id] = {
            "name": user_name,
            "borrowed_books": borrowed_books
        }
        print(f"✅ {user_name} has been registered with ID: {user_id}.\n")

    elif choice == 3:
        # Borrow Book
        borrower = input("Enter the borrower's name or ID: ").strip()
        if not borrower:
            print("❌ Input cannot be empty.\n")
            continue

        found = False
        for user_id, user_info in users.items():
            if borrower == user_id or borrower.lower() == user_info["name"].lower():
                print(f"✅ Found user: {user_info['name']} (ID: {user_id})")
                try:
                    number_of_books = int(input("How many books do they want to borrow❓ "))
                    for i in range(number_of_books):
                        while True:
                            book_input = input(f"Enter book #{i+1} name or ID: ").strip().lower()
                            for book_id, book_info in books.items():
                                if (book_input == book_id.lower() or book_input == book_info["title"].lower()):
                                    if not book_info["available"]:
                                        print("❌ Book is currently unavailable.\n")
                                    else:
                                        users[user_id]["borrowed_books"].append(book_id)
                                        books[book_id]["available"] = False
                                        books[book_id]["borrowed_by"] = user_id
                                        print(f"✅ {book_info['title']} has been borrowed.\n")
                                    break
                            else:
                                print("❌ Book not found. Try again.\n")
                                continue
                            break
                    found = True
                    break
                except ValueError:
                    print("❌ Invalid number.\n")
        if not found:
            print("❌ Borrower not found.\n")

    elif choice == 4:
        # Return Book
        returner = input("Enter the returner name or ID: ").strip()
        if not returner:
            print("Input cannot be empty.\n")
            continue

        found = False
        for user_id, user_info in users.items():
            if returner == user_id or returner.lower() == user_info["name"].lower():
                print(f"✅ Found user: {user_info['name']} (ID: {user_id})")
                try:
                    number_of_books = int(input(f"How many books does {user_id} want to return: "))
                    for i in range(number_of_books):
                        while True:
                            book_input = input(f"Enter book #{i + 1} {user_id} wants to return: ").strip().lower()
                            if not book_input:
                                print("This entry cannot be empty.\n")
                                continue
                            for book_id, book_info in books.items():
                                if (book_input == book_id.lower() or book_input == book_info["title"].lower()):
                                    users[user_id]["borrowed_books"].remove(book_id)
                                    books[book_id]["available"] = True
                                    books[book_id]["borrowed_by"] = None
                                    print(f"✅ {book_info['title']} has been returned.\n")
                                    break
                            else:
                                print("❌ Book not found. Try again.\n")
                                continue
                            break
                    found = True
                    break
                except ValueError:
                    print("❌ Invalid number.\n")
        if not found:
            print("❌ Returner not found.\n")

    elif choice == 5:
        # Search Book
        book_researcher = input("Enter the name or the ID of the book you are looking for --->\n").strip()
        if not book_researcher:
            print("This input cannot be empty. Please try again.\n")
            continue

        found = False
        for book_id, book_info in books.items():
            if book_researcher == book_id or book_info["title"].lower() == book_researcher.lower():
                print(f"{book_info['title']} has been found ✅.")
                print("Here is the information:")
                print(f"Name: {book_info['title']}")
                print(f"Author: {book_info['author']}")
                print(f"Year of Release: {book_info['year']}")
                print(f"Availability: {'Yes' if book_info['available'] else 'No'}")
                print(f"Borrowed by: {book_info['borrowed_by']}\n")
                found = True
                break

        if not found:
            print(f"The book '{book_researcher}' was not found. Try again.\n")

    elif choice == 6:
        try:
            data = {
                "books": books,
                "users": users
            }
            with open("library_data.json", "w") as file:
                json.dump(data, file, indent=4)
            print("✅ Library data saved successfully to 'library_data.json'.\n")
        except Exception as e:
            print(f"❌ Error saving to file: {e}\n")

    elif choice == 7:
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)
                books.clear()
                users.clear()
                books.update(data["books"])
                users.update(data["users"])
            print("✅ Library data loaded successfully from 'library_data.json'.\n")
        except FileNotFoundError:
            print("❌ File not found. Make sure 'library_data.json' exists.\n")
        except json.JSONDecodeError:
            print("❌ Error decoding file. File might be corrupted or not in JSON format.\n")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}\n")


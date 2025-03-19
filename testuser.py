import bcrypt
import csv

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# User details
users = [
    {"username": "admin", "password": "admin123"},
    {"username": "user", "password": "user123"}
]

# Hash passwords for both users
for user in users:
    hashed_password = hash_password(user["password"])
    user["hashed_password"] = hashed_password.decode('utf-8')  # Storing the hashed password as a string

# Save the users' data to a CSV file
csv_file = "users.csv"
fieldnames = ["username", "password"]

with open(csv_file, mode="w", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Write the header row
    for user in users:
        # Write each user's username and hashed password
        writer.writerow({"username": user["username"], "password": user["hashed_password"]})

print(f"Users have been saved to {csv_file}")

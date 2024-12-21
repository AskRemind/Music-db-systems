import csv
from models import db, User
from app import app

def import_users_from_csv(file_path):
    with app.app_context():
        db.create_all()

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    existing_user = User.query.filter_by(Email=row['email']).first()
                    if not existing_user:
                        user = User(
                            UserID=row['User_id'],
                            FirstName=row['first_name'],
                            LastName=row['last_name'],
                            Email=row['email'],
                            Gender=row.get('gender', 'Unknown'),
                            Country=row.get('Country', 'Unknown'),
                            PasswordHash=row['Password'],
                        )
                        db.session.add(user)
                except KeyError as e:
                    print(f"Missing key in row: {e}")
                except Exception as e:
                    print(f"Error importing user {row['email']}: {str(e)}")

            db.session.commit()
            print("Users imported successfully.")


if __name__ == '__main__':
    import_users_from_csv('data/users.csv')

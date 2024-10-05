from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"S": "Study", "R": "Relaxation"}

# Easier to get today's date
def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    # To keep it in the format that we want
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        # Keeps recalling the method
        return get_date(prompt, allow_default)

def get_hours():
    try:
        hours = float(input("Enter the hours: "))
        if hours <= 0 or hours >= 24:
            raise ValueError("Hours must be a non-negative non-zero value and cannot exceed 24 hours.")
        return hours
    except ValueError as e:
        print(e)
        return get_hours()

def get_category():
    category = input("Enter the category ('S' for Study or 'R' for Relaxation): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid category. Please enter 'S' for Study or 'R' for Relaxation.")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")

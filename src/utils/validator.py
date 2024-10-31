class Validator:

    @staticmethod
    def is_valid_rating(rating):
        try:
            # convert to a number if required
            rating = int(rating)

        except ValueError:
            return False
        
        if rating < 1 or rating > 5:
            return False
    
        return True
    
    @staticmethod
    def validate_age(age):
        try:
            age = int(age)

        except ValueError:
            raise ValueError("Age must be a positive integer")
        
        if age < 0:
            raise ValueError("Age must be a positive integer")
    
    @staticmethod
    def validate_gender(gender):
        # normalize the gender
        gender = gender.upper()

        if gender not in ['M', 'F']:
            raise ValueError("Invalid gender")
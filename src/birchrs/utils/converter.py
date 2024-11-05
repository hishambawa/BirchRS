from birchrs.utils.validator import Validator

class Converter:

    @staticmethod
    def age_to_category(age):
        """
        Convert the given age value into a predefined age range.

        This function takes an age as input and categorizes it into one of 
        the following predefined age ranges:
        - "Under 18"
        - "18-24"
        - "25-34"
        - "35-44"
        - "45-49"
        - "50-55"
        - "56+"

        Args:
            age (str,int): The age value to categorize.

        Returns:
            int: A string representing the age range the input falls into.

        Raises:
            ValueError: If the age is not a positive integer.
        """
        # validate the age input
        Validator.validate_age(age)
        
        # convert the age to a number
        age = int(age)
        
        # categorize the age
        if age < 18:
            return 1
        elif age < 25:
            return 18
        elif age < 35:
            return 25
        elif age < 45:
            return 35
        elif age < 50:
            return 45
        elif age < 56:
            return 50
        else:
            return 56
        
    @staticmethod
    def gender_to_category(gender):
        """
        Categorize the gender input into a numeric value.

        This function takes a gender input as a string and returns a 
        category based on the value:
        - 0 for "M"
        - 1 for "F"

        Args:
            gender (str): The gender identifier, expected to be "M" or "F".

        Returns:
            int: The corresponding gender category.

        Raises:
            ValueError: If the gender input is invalid.
        """
        # convert to uppercase to normalize the input
        gender = gender.upper()

        # validate the gender
        Validator.validate_gender(gender)

        if gender == 'M':
            return 0
        else:
            return 1
        
    @staticmethod
    def genre_to_category(genres):
        """
        Convert genre to a numerical value based on predefined categories.
        
        Args:
            genre (str): The genre name to convert.

        Returns:
            int: Numerical value corresponding to the genre, or 99 for None.
        """
        genre_mapping = {
            "Action": 0,
            "Adventure": 1,
            "Animation": 2,
            "Children's": 3,
            "Comedy": 4,
            "Crime": 5,
            "Documentary": 6,
            "Drama": 7,
            "Fantasy": 8,
            "Film-Noir": 9,
            "Horror": 10,
            "Musical": 11,
            "Mystery": 12,
            "Romance": 13,
            "Sci-Fi": 14,
            "Thriller": 15,
            "War": 16,
            "Western": 17,
            None: 99  # Using 99 for None values
        }
        
        return genre_mapping.get(genres, 99)  # Return 99 for any unrecognized genres
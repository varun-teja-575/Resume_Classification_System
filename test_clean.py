
from preprocessing.clean_text import clean_resume

sample_resume = """
John Doe

Email : john@gmail.com

Phone : 9876543210

Experienced Python Developer with 3 years of experience.

Skills:
Python
SQL
Pandas
NumPy
Machine Learning
"""

cleaned = clean_resume(sample_resume)

print(cleaned)
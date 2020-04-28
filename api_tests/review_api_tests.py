from requests import get

# Все отзывы
print(get('http://artour.pythonanywhere.com/api/reviews/0').json())

# Отзывы по id
print('1:', get('http://artour.pythonanywhere.com/api/review/1').json())
print('100:', get('http://artour.pythonanywhere.com/api/review/100').json())

# Отзывы по оценке
print('1:', get('http://artour.pythonanywhere.com/api/reviews/1').json())
print('9:', get('http://artour.pythonanywhere.com/api/reviews/9').json())
print('5:', get('http://artour.pythonanywhere.com/api/reviews/5').json())

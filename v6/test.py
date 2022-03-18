from requests import get, post, put, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/2').json())
print(post('http://localhost:5000/api/v2/users', json={'surname': 'Скот2',
                                                      'name': 'Ридли2',
                                                      'age': '12',
                                                      'position': '03.03.3000',
                                                     'speciality': '03.03.3000',
                                                      'address': 'Moon',
                                                      'email': 's2@s2.com',
                                                      'password': '123'}).json())
print(delete('http://localhost:5000/api/v2/users/6').json())
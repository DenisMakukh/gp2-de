"""
Module Description:
This module performs XYZ functionality.

Author: Denis Makukh
Date: 28.02.2025
"""


def extend_vacancies_from_response(response, vacancies):
    if response and 'objects' in response:
        for vacancy in response['objects']:
            vacancy_data = {
                'vacancy_id': vacancy.get('id'),
                'payment_from': vacancy.get('payment_from'),
                'payment_to': vacancy.get('payment_to'),
                'currency': vacancy.get('currency'),
                'date_published': vacancy.get('date_published'),
                'address': vacancy.get('address'),
                'profession': vacancy.get('profession'),
                'candidat': vacancy.get('candidat'),
                'type_of_work': vacancy.get('type_of_work', {}).get('title'),
                'languages': [lang for lang in vacancy.get('languages', [])],
                'phone': vacancy.get('phone'),
                'link': vacancy.get('link')
            }
            vacancies.append(vacancy_data)

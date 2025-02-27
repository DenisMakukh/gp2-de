"""
Module Description:
This module performs XYZ functionality.

Author: Denis Makukh
Date: 27.02.2025
"""
import logging

import pandas as pd

log = logging.getLogger(__name__)


def parse_json_list_to_dataframe(json_list):
    log.info("Parsing json list into df")
    data_list = []

    for json_data in json_list:
        data = {
            'id': json_data.get('id'),
            'title': json_data.get('title'),
            'salary_from': json_data['salary'].get('from') if json_data.get('salary') else None,
            'salary_to': json_data['salary'].get('to') if json_data.get('salary') else None,
            'salary_currency': json_data['salary'].get('currency') if json_data.get('salary') else None,
            'salary_pay_type': json_data['salary'].get('pay_type') if json_data.get('salary') else None,
            'description': json_data.get('description'),
            'contact_name': json_data['contact_person'].get('name') if json_data.get('contact_person') else None,
            'contact_email': json_data['contact_person'].get('email') if json_data.get('contact_person') else None,
            'contact_phone': json_data['contact_person']['phones'][0]['number_international'] if json_data.get(
                'contact_person') and json_data['contact_person'].get('has_phone') and
                len(json_data['contact_person']['phones']) > 0 else None,
            'operating_schedule': json_data['operating_schedule'].get('name') if json_data.get(
                'operating_schedule') else None,
            'company_name': json_data['company'].get('name') if json_data.get('company') else None,
            'company_id': json_data['company'].get('id') if json_data.get('company') else None,
            'company_type': json_data['company'].get('type') if json_data.get('company') else None
        }
        data_list.append(data)

    df = pd.DataFrame(data_list)

    return df

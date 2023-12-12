import datetime

import json

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def title_to_slug(text):
    return text.lower().replace(' ', '-')

def slug_to_title(slug):
    return slug.replace('-', ' ').title()

def parse_error_message(error_message):
    # Find the index of the newline character (\n)
    newline_index = error_message.find('\n')

    # Extract the error message until the newline character
    parsed_error_message = error_message[:newline_index]

    return parsed_error_message
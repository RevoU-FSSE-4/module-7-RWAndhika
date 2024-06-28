review_insert_schema = {
    'rating': { 'type': 'integer', 'required': True, 'min': 1, 'max': 5 },
    'description': { 'type': 'string', 'required': True, 'minlength': 4 }
}
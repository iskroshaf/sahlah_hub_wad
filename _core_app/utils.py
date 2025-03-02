import uuid

def generate_unique_id(model, prefix, field_name, length=5):
    while True:
        # Generate a unique integer ID from UUID
        unique_id = str(uuid.uuid4().int)[:length]
        unique_identifier = f"{prefix}{unique_id}"

        # Check if the generated ID already exists in the specified model field
        if not model.objects.filter(**{field_name: unique_identifier}).exists():
            return unique_identifier

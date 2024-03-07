
class RegisteredTenant():
    id = String()
    name = String()
    last_name = String()
    email = String()
    created_date = Long()

class ValidatedTenant():
    id = String()
    validation_date = Long()

class DeactivatedTenant():
    id = String()
    deactivated_date = Long()
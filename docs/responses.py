from backend.models.shared import ErrorResponse


already_register_responses = {
    400: {
        "model": ErrorResponse,
        "detail": "User already exists",
    }
}

incorrect_credentials = {
    401: {
        "model": ErrorResponse,
        "detail": "Incorrect login or password",
    }
}



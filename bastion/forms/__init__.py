def first_error_message(form):
    error_data = form.errors.as_data()
    error_data_list = list(error_data.items())
    error_message = error_data_list[0][1][0].message
    message = "{}".format(error_message)
    return message


import time


# noinspection PyBroadException
def get_file_data(location):
    try:
        try:
            with open(location, 'r') as f:
                data = f.read()
        except Exception:
            file_not_found_page = get_file_data('static/pages/404.html')
            try:
                file_not_found_page = file_not_found_page.format(location=location, time=str(time.time()))
            except Exception:
                pass
            return file_not_found_page
    except Exception:
        ise = get_file_data('static/pages/501.html')
        try:
            ise = ise.format(location=location, time=str(time.time()))
        except Exception:
            pass
        return ise
    return data


# noinspection PyBroadException
def load_site(location):
    def pseudo_decorator(function_to_be_decorated):
        def real_wrapper(*args, **kwargs):
            kwargs['html_data'] = get_file_data(location)
            return function_to_be_decorated(*args, **kwargs)
        return real_wrapper
    return pseudo_decorator

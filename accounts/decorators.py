from django.contrib.auth.decorators import user_passes_test


def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name='Admin').exists()
    )(view_func)


def parking_attendant_required(view_func):
    return user_passes_test(
        lambda u: u.groups.filter(name=' Store Attendant').exists()
    )(view_func)


def section_manager_required(view_func):
    return user_passes_test(
        lambda u: u.groups.filter(name='Sales Attendant').exists()
    )(view_func)

def parking_attendant_required(view_func):
    return user_passes_test(
        lambda u: u.groups.filter(name=' Manager').exists()
    )(view_func)

def section_manager_required(view_func):
    return user_passes_test(
        lambda u: u.groups.filter(name='Store Manager').exists()
    )(view_func)


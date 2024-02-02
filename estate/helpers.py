from .models import Property, Location


def get_common_data():
    states = Location.objects.values_list('state', flat=True).distinct()
    cities = Location.objects.values_list('city', flat=True).distinct()
    categories = [category for category, _ in Property.PROPERTY_CATEGORIES]
    statuses = [status for status, _ in Property.PROPERTY_STATUS]

    return {
        'states': states,
        'cities': cities,
        'categories': categories,
        'statuses': statuses,
    }

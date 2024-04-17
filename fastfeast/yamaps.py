from geopy import Yandex


def generate_yandex_map_basket_html(lat1, lon1, lat2, lon2):
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2

    html = f'''
    <div style="position:relative;overflow:hidden;">
        <iframe src="https://yandex.by/map-widget/v1/?ll={center_lon},{center_lat}&mode=routes&rtext={lat1}%2C{lon1}~{lat2}%2C{lon2}&rtt=pd" width="560" height="400" frameborder="1" style="position:relative;"></iframe>
    </div>
    '''

    return html


def generate_yandex_map_institution_html(lat1, lon1):
    html = f'''
    <div style="position:relative;overflow:hidden;">
    <iframe src="https://yandex.by/map-widget/v1/?ll={lon1}%2C{lat1}&mode=whatshere&utm_medium=mapframe&utm_source=maps&whatshere%5Bpoint%5D={lon1}%2C{lat1}&whatshere%5Bzoom%5D=17&z=17.15" width="560" height="400" frameborder="1" style="position:relative;"></iframe>
    </div>
    '''

    return html


def geocoder(address):
    my_geocoder = Yandex(api_key="dd817afb-e96a-4c3a-8592-8beb732d7227").geocode(str("Минск, Беларусь" + address))
    # print(my_geocoder.latitude)
    # print(my_geocoder.longitude)
    # print(my_geocoder.address)
    return [my_geocoder.latitude, my_geocoder.longitude]



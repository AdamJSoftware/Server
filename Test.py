import requests

def internet_on():
    try:
        requests.get('http://216.58.192.142')
        print('ay')
        return True
    except:
        print('nah')
        return False

internet_on()
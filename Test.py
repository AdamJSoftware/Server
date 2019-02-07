with open('Profiles.txt', 'r') as f:
    print("Please wait for system to configure new computer...")
    results = f.read().split(',')
    print(results)
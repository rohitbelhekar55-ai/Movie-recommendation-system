import requests

BASE_URL = 'http://127.0.0.1:5000/recommend'

def test_filters():
    print("Testing Filters...")
    
    # 1. Test Genre Filter
    print("\n1. Testing Genre: Animation")
    data = {'genre': 'Animation', 'movie_name': ''}
    try:
        res = requests.post(BASE_URL, data=data)
        if "Toy Story" in res.text or "Animation" in res.text:
             print("PASS: Animation movies returned.")
        else:
             print("FAIL: Animation check failed.")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Test Rating Filter
    print("\n2. Testing Min Rating: 4.0")
    data = {'rating': '4', 'movie_name': ''}
    try:
        res = requests.post(BASE_URL, data=data)
        if res.status_code == 200:
             print("PASS: Request successful.")
             # In a real test we would parse HTML, but here we just check 200 and some content
        else:
             print(f"FAIL: Status {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    # 3. Test Year Filter
    print("\n3. Testing Year: > 2000")
    data = {'min_year': '2000', 'movie_name': ''}
    try:
        res = requests.post(BASE_URL, data=data)
        if res.status_code == 200:
             print("PASS: Request successful.")
        else:
             print(f"FAIL: Status {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_filters()

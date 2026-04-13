import requests

def test_recommendation():
    url = 'http://127.0.0.1:5000/recommend'
    data = {'movie_name': 'Toy Story (1995)'}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Status Code: 200 OK")
            if "Movies like" in response.text:
                print("Success: Recommendation results found in response.")
                # print(response.text[:500]) # Print first 500 chars to debug if needed
            else:
                print("Failure: Results text not found.")
                print(response.text)
        else:
            print(f"Failed with status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_recommendation()

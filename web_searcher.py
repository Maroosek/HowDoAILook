import replicate
import requests
from bs4 import BeautifulSoup
import os

def generate_search_query(user_input):
    prompt = (
        f"Użytkownik napisał: '{user_input}'. Zwróć jedną krótką frazę do wyszukania w sklepie internetowym (po polsku, maks 5 słów, bez cudzysłowów, poprawna polszczyzna, wszystkie słowa w jednej linii, bez dzielenia wyrazów, żadnych znaków specjalnych)."
    )
    input = {
        "prompt": prompt,
        "max_new_tokens": 40,
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nJesteś pomocnym asystentem.<|eot_id|><|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    }
    result = replicate.run(
        "meta/meta-llama-3-8b-instruct",
        input=input,
    )
    if isinstance(result, list):
        return " ".join(result).strip()
    return str(result).strip()

def duckduckgo_search(query):
    url = "https://html.duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.post(url, data=params, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for result in soup.find_all('a', attrs={'class': 'result__a'}):
        title = result.get_text()
        link = result.get('href')
        results.append({"title": title, "link": link})
        if len(results) >= 5:
            break
    return results

if __name__ == "__main__":
    user_input = "chcę czarny t-shirt rozmiar M"
    fraza = generate_search_query(user_input)
    print("Fraza do wyszukania:", fraza)
    wyniki = duckduckgo_search(user_input + " sklep online")
    print("Najlepsze linki do sklepów z DuckDuckGo:")
    for i, wynik in enumerate(wyniki, 1):
        print(f"{i}. {wynik['title']}\n   {wynik['link']}\n")
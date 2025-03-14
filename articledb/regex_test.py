import re
import unittest

padrao_link = ''.join(
    (
        r"https?://",                                   #  Protocolo http ou https
        r"(?=[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-]+)",          #  Deve haver pelo menos um ponto entre domínios
        r"(?!.*[\?\#&=%@_\-]$)",                            #  Não pode terminar com certos caracteres na URL
        r"[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]{4,}"    #  4 caracteres ou mais no resto da URL
    )
)

test_case = unittest.TestCase()

# Testes do regex de URL

def teste(url: str) -> bool:
    return bool(re.fullmatch(padrao_link, url))


# URLs válidos

urls_validos = urls = {
    "https://example.com": True,                                                        # 
    "http://sub.domain.co.uk": True,                                                    # 
    "https://example.com/search?q=test&page=1": True,                                   # 
    "https://api.example.com/data?user_id=123&token=abc123": True,                      # 
    "https://example.com/products?category=books&sort=price_desc": True,                # 
    "https://example.com/path/to/file.txt": True,                                       # 
    "https://example.com/path/to/some-page.html#section": True,                         # 
    "https://example.com/resource/123@456": True,                                       # 
    "https://example.com/api/v1/get?data=item1,item2,item3": True,                      # 
    "https://example.com/order?status=shipped&date=2025-03-13T12:00:00Z": True,         # 
    "https://example.com/path/with%20space": True,                                      # 
    "https://example.com/api/v1/users?ids=[1,2,3]": True,                               # 
    "https://example.com/resource/[abc]": True,                                         # 
    "https://example.com/search?name=O'Connor": True,                                   # 
    "https://example.com/query?foo=bar&baz=qux!": True,                                 # 
    "https://example.com/path/to/resource(name)": True,                                 # 
    "https://example.com/path/to/file+1.txt": True,                                     # 
    "https://example.com/get;param=value": True,                                        # 
    "https://example.com/api?action=buy&price=$100": True,                              # 
    "https://example.com/products?id=123&name=TV&brand=Sony&color=red": True,           # 
    "https://example.com/query?data=%5B1,2,3%5D": True,                                 # 
    "https://example.com/info?name=J%20Doe&location=NYC": True,                         # 
    "https://example.com/api?value=%23hash": True,                                      # 
    "https://example.com/path?msg=Hello%2C%20World%21": True,                           # 
    "https://www.example.com/": True,
    "https://www.example.com.": True,
}

formatador = max(len(url) for url in urls_validos)
for url, validade in urls_validos.items():
    print(f"URL: {url:<{formatador}} | Esperado: {validade} | Resultado: {teste(url)}")

print("-" * 110)
# URLs inválidos

urls_invalidos = {
    "htts://www.example.com": False,
    "https:/ /www.example.com": False,
    "ftp://files.server.com": False,
    "https://": False,
    "https": False,
    "https://a.c": False,
    "https://w": False,
    "https://example.com/data?filter=[{\"field\":\"name\",\"value\":\"John\"}]": False,
    "www.example.com": False,
    "example.com": False,
    "https://.com": False,
    "https://..com": False,
    "https://.example": False,
    "https://ex@ample.com": False,
    "htp://example.com": False,
    "httpx://example.com": False,
    "file://example.com": False,
    "sftp://example.com": False,
    "https://example .com": False,
    "https:// example.com": False,
    "https://example.com/ space": False,
    "https://example.com/#has space": False,
    "https://example": False,
    "https://example..com": False,
    "": False,
    "https://example.com/space here": False,
    "https://example.com/<script>": False,
    "https://www.example.com/#": False,
    "https://www.example.com/?": False,
    "https://www.example.com/@": False,
    "https://www.example.com/_": False,
    "https://www.example.com/-": False,
}


formatador = max(len(url) for url in urls_invalidos)
for url, validade in urls_invalidos.items():
    print(f"URL: {url:<{formatador}} | Esperado: {validade} | Resultado: {teste(url)}")

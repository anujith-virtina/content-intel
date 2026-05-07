import json, base64, urllib.request

with open('C:/content-intel/new-42108-content.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Content length:", len(content))

creds = base64.b64encode(b'anujith:Mibz 1h3E jWRi bfJs WAXZ rwrM').decode()
payload = json.dumps({
    'content': content,
    'status': 'draft',
    'featured_media': 42109
}).encode('utf-8')

req = urllib.request.Request(
    'https://virtina.com/wp-json/wp/v2/posts/42108',
    data=payload,
    headers={
        'Authorization': 'Basic ' + creds,
        'Content-Type': 'application/json; charset=utf-8'
    },
    method='PUT'
)
with urllib.request.urlopen(req) as resp:
    body = json.loads(resp.read())
    print("Post status:", body['status'])
    print("featured_media:", body['featured_media'])
    print("Returned content length:", len(body['content']['raw']))
    print("First 250 chars:")
    print(body['content']['raw'][:250])

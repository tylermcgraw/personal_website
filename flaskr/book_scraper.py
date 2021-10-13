import urllib.request

def get_books():
  shelves = ['read', 'to-read', 'currently-reading']
  books = []
  for shelf in shelves:
    page = 1
    count = 0
    while count != 1:
      count = 0
      with urllib.request.urlopen(f"https://www.goodreads.com/review/list/137613953-tyler?page={page}&per_page=30&shelf={shelf}&utf8=%E2%9C%93") as response:
        html = response.read().decode('utf-8')
        index = 0
        while index != -1:
          count += 1
          # Get url
          index = html.find('href="/book/show')
          url = 'https://www.goodreads.com' + html[index + html[index:].find('"') + 1:index + html[index + 7:].find('"') + 7]
          html = html[index + 16:]
          # Get title
          index = html.find('href="/book/show')
          start = index + html[index:].find('>') + 1
          end = index + html[index + 16:].find('<') + 16
          title = html[start:end + 10].strip("\n").strip()
          title = title[:title.find('\n')]
          html = html[end:]
          # Get author
          index = html.find('<a href="/author')
          start = index + html[index:].find('>') + 1
          end = index + html[index + 16:].find('<') + 16
          author = html[start:end]
          if author.find(',') != -1:
            author = author[author.find(",") + 2:] + ' ' + author[:author.find(",")]
          html = html[end:]
          # Set status to current shelf
          status = shelf
          books.append({
            'title': title,
            'author': author,
            'status': status,
            'url': url
          })
        # Remove extra book
        books.pop()
        page += 1
  return books

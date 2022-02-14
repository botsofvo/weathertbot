from telegraph import Telegraph

telegraph = Telegraph(
    "8e2fb6c5da86ea9ab894fc5b59c4472b7db8fda4bc54b369074c6192d322")
# telegraph.create_account(short_name='Weather')


def pagecreator(data):
    response = telegraph.create_page(
        '🌅Your weather forecast:',
        html_content=f'''<p>{data}</p>''')
    return response['url']


# Page_link=telegraph.get_page("YOur-weather-forecast-02-14-2")
# No_of_page=telegraph.get_page_list()
# print (No_of_page)
# print(Page_link['url'])
# print(response)
# print(response['url'])

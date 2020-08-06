import pandas as pd
import pdfkit as pdf
import requests
from time import time
import datetime
from sentiment import *


# date_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")


# api_endpoint = "http://newsapi.org/v2/everything?q=bitcoin&from="+date_str+"&sortBy=publishedAt&apiKey=a21ca444cf7b40ae89c0a84c99585d2e&page="

# def get_output(api_endpoint=api_endpoint, query=''):
def get_output(query=''):
    try:
        query = query.split('?')[1]
    except:
        pass

    date_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    print(date_str)
    api_endpoint = str(
        "http://newsapi.org/v2/everything?q=" + query + "&from=" + date_str + "&sortBy=publishedAt&apiKey=a21ca444cf7b40ae89c0a84c99585d2e&page=")

    print(api_endpoint)

    responses = []
    output = []
    total_results = 0
    scores = []

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        i = 1
        while True:
            response = requests.get(api_endpoint + str(i)).json()
            i += 1
            if response["status"] == 'error':
                break
            total_results = int(response["totalResults"])
            responses.append(response)

    except:
        return None

    # i = 1
    # while True:
    #     response = requests.get(api_endpoint + str(i)).json()
    #     i += 1
    #     if response["status"] == 'error':
    #         break
    #     total_results = int(response["totalResults"])
    #     responses.append(response)

    for response in responses:
        for article in response['articles']:
            articles = []
            title = article['title'][:60]

            score = get_score(title)
            scores.append(score)

            url = article['url']
            publisher = article['source']['name']
            timestamp = article['publishedAt']
            timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').strftime("%Y-%m-%d %I:%M %p")
            articles.append(title)
            articles.append(url)
            articles.append(publisher)
            articles.append(timestamp)
            output.append(articles)

    final_score = get_final_score(scores)
    text_score = get_text_score(final_score)

    pd.set_option('colheader_justify', 'center')
    df = pd.DataFrame(output, columns=("Title", "URL", "Publisher", "Timestamp"))
    df.index = df.index + 1

    time_now = datetime.datetime.now().strftime("%Y-%m-%d")  # -%I-%H-%S-%p

    df.to_html('./htmls/table' + time_now + '.html', classes='myStyle')
    print("html file created")
    with open('./htmls/table' + time_now + '.html', 'r', encoding='utf-8') as table_file:
        table_content = table_file.read()

    html_string = f'''
    <html>
      <head><title>Data Table</title></head>
      <link rel="stylesheet" type="text/css" href="./structure/table.css"/>
      <body>
        <div style='text-align: right; width: 100%; margin-bottom: 15px; font-family: Arial, Serif, monospace'>
          <p style="font-size: 15px;"><b>Date:</b> {date_str} (UTC)</p>
          <p style="font-size: 15px;"><b>Ticker:</b> {query}</p>
        </div>
        <div style='margin-bottom: 30px; float: center'>
            <table width='50%' border="1" class="dataframe myStyleSummary">
                <caption style="text-align:left;
                color: #3f81bf; border-top: 2px solid #3f81bf;
                margin-bottom: 2px; font-size: 18px;
                padding: 3px; font-family: Serif, monospace; font-weight: bold;">SUMMARY</caption>
              <thead>
                <tr>
                  <th style="text-align: left;">Total Articles</th>
                  <th>{total_results}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th style="text-align: left;">Overall sentiment</th>
                  <th>{text_score}</th>
                </tr>
              </tbody>
            </table>
        </div>
        <div style="text-align:left;
                color: #3f81bf; border-top: 2px solid #3f81bf;
                margin-bottom: 2px; font-size: 18px;
                padding: 3px; font-family: Serif, monospace; font-weight: bold;">ARTICLES</div>
        <div style="margin-bottom: 40px;">
        {table_content}
        </div>
      </body>
    </html>
    '''
    with open('./htmls/table' + time_now + '.html', 'w', encoding='utf-8') as table_file:
        table_file.write(html_string)
    print("html file modified")
    options = {
        "--enable-local-file-access": '',
        "quiet": '',
        'encoding': "UTF-8",
        'footer-center': 'Page [page] of [topage]',
        '--footer-html': './htmls/structure/footer.html',
        '--header-html': './htmls/structure/header.html',
        '--footer-line': ''
    }
    print("Hello")
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d")  # -%I-%H-%S-%p
    print(datetime_now)
    pdf_gen_file = './pdfs/Quantflare_' + query + '_' + datetime_now + '.pdf'
    # config = pdf.configuaration(wkhtmltopdf="C:\Windows\System32\cmd.exe")
    # pdf.from_file('./htmls/table' + time_now + '.html', pdf_gen_file, options=options, configuaration=config)
    pdf.from_file('./htmls/table' + time_now + '.html', pdf_gen_file, options=options)

    print(pdf_gen_file)

    return pdf_gen_file


if __name__ == "__main__":
    result_file_name = get_output("?TSLA")

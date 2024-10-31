import redis
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_paginate import Pagination, get_page_args # to be able to have a default pagination

def main():
    """The main function for this script."""
    app.run(host='0.0.0.0', port=443, debug=True)
    CORS(app)

app = Flask(__name__)

host = 'redis'
port = 6379

#########
# CONST #
#########
PER_PAGE = 9 # number of news articles per page

# arrows for the pagination
ARROW_LEFT_BIG = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-left-fill" viewBox="0 0 16 16"> <path d="m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z"/></svg>'
ARROW_RIGHT_BIG = ' <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-right-fill" viewBox="0 0 16 16"><path d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"/></svg>'
ARROW_LEFT_SMALL = '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" fill="currentColor" class="bi bi-caret-left-fill" viewBox="0 0 16 16"> <path d="m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z"/></svg>'
ARROW_RIGHT_SMALL = ' <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" fill="currentColor" class="bi bi-caret-right-fill" viewBox="0 0 16 16"><path d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"/></svg>'

# AUXILIAR FUN
def pagination_gen(data, page, per_page=8):
    total = len(data)
    offset = (page - 1) * per_page
    # data.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
    return data[offset: offset + per_page], total


@app.route("/index")
def index():
    return render_template("index.html")



@app.route("/news")
def get_news():
    r = redis.Redis(host=host, port=port, decode_responses=True)

    nid = request.args.get('id', None)

    if nid != None:
        
        # redis.Query()

        return render_template(
            'single_news_article.html',
            news_articles=news_articles,
            page=page,
            news_articles_total=news_articles_total,
            pagination=pagination,
            small_pagination=small_pagination
        )
    else:
        page, _, _ = get_page_args(page_parameter='page',
                                per_page_parameter='per_page')
        keys = r.keys('*')
        documents = []
        for key in keys:
            if r.type(key) == 'hash':
                doc = r.hgetall(key)
            else:
                doc = r.get(key)
            documents.append((key, doc))

        href = f'/demo/news?page=' + '{0}'
        news_articles, news_articles_total = pagination_gen(page=page, per_page=PER_PAGE, data=documents)
        pagination = Pagination(page=page, per_page=PER_PAGE, total=news_articles_total,
                                    css_framework='bootstrap5', bs_version = 5, prev_label = ARROW_LEFT_BIG, next_label = ARROW_RIGHT_BIG, href=href, display_msg="<p class='text-uppercase fw-light'>Showing <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>")
        small_pagination = Pagination(page=page, per_page=PER_PAGE, total=news_articles_total,
                                    css_framework='bootstrap5', bs_version = 5, prev_label = ARROW_LEFT_SMALL, next_label = ARROW_RIGHT_SMALL, href=href,display_msg="<p class='text-uppercase fw-light'>Showing <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>", link_size='sm')

        return render_template(
            'redis.html',
            news_articles=news_articles,
            page=page,
            news_articles_total=news_articles_total,
            pagination=pagination,
            small_pagination=small_pagination
        )

if __name__ == "__main__":
    main()

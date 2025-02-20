from prometheus_client import make_wsgi_app, Counter
from flask import Response

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'http_status']
)

@api.route('/metrics')
def metrics():
    return Response(make_wsgi_app(), mimetype="text/plain")

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(
        request.method,
        request.path,
        response.status_code
    ).inc()
    return response
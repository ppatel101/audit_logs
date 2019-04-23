from sanic import Sanic
from sanic import response
import csv
import datetime
from sanic_openapi import swagger_blueprint, doc

app = Sanic()

@app.post("/audit_logs/new")
@doc.summary("Creates a audit log")
@doc.consumes(doc.JsonBody({"audit_log": { "action": str , "event_type": str}}), content_type="application/json", location="body")
async def auditLogs(request):

    params = getattr(request, "json")
    row_count = sum(1 for line in open("audit_logs.csv"))

    rows = [
                [
                    row_count,
                    params["audit_log"]["action"],
                    params["audit_log"]["event_type"],
                    datetime.datetime.now()
                ],
            ]

    csv.register_dialect('myDialect',
                        quoting=csv.QUOTE_ALL,
                        skipinitialspace=True
                    )

    with open('audit_logs.csv', 'a') as f:
        writer = csv.writer(f, dialect='myDialect')
        for row in rows:
            writer.writerow(row)

    f.close()
    return response.json(
        {
            "data": {
                        "id": row_count,
                        "action": params["audit_log"]["action"],
                        "event_type": params["audit_log"]["event_type"],
                        "created_at": datetime.datetime.now()
                    }
        },
        status=201
    )

if __name__ == "__main__":
    app.blueprint(swagger_blueprint)
    app.run(host="0.0.0.0", port=8000)
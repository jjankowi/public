from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Lista 10 testów (punkt 5 w sidebarze - rozwijane)
TESTS = [
    {"id": i, "name": f"Test {i}"} for i in range(1, 11)
]

# Przykładowe dane wyników dla każdego testu (zgodne ze screenem)
def sample_rows(test_id):
    base = test_id * 100
    rows = [
        {"id": 615, "namespace": "%SYS", "routine": "%SYS.WorkQueueMgr", "linesexecuted": 150092, "globalreferences": 10634, "state": "SEMW", "pidexternal": 615, "username": "", "clientipaddress": ""},
        {"id": 616, "namespace": "%SYS", "routine": "%SYS.WorkQueueMgr", "linesexecuted": 7070, "globalreferences": 23, "state": "SEMW", "pidexternal": 616, "username": "", "clientipaddress": ""},
        {"id": 617, "namespace": "%SYS", "routine": "%SYS.WorkQueueMgr", "linesexecuted": 98827, "globalreferences": 10143, "state": "EVTW", "pidexternal": 617, "username": "", "clientipaddress": ""},
        {"id": 625, "namespace": "USER", "routine": "Ens.Queue.1", "linesexecuted": 288330, "globalreferences": 24058, "state": "EVTW", "pidexternal": 625, "username": "_Ensemble", "clientipaddress": ""},
        {"id": 626, "namespace": "USER", "routine": "Ens.Queue.1", "linesexecuted": 1117, "globalreferences": 131, "state": "EVTW", "pidexternal": 626, "username": "_Ensemble", "clientipaddress": ""},
        {"id": 629, "namespace": "USER", "routine": "Ens.Queue.1", "linesexecuted": 394861, "globalreferences": 56374, "state": "EVTW", "pidexternal": 629, "username": "_Ensemble", "clientipaddress": ""},
        {"id": 631, "namespace": "USER", "routine": "Ens.Queue.1", "linesexecuted": 596381, "globalreferences": 31908, "state": "EVTW", "pidexternal": 631, "username": "_Ensemble", "clientipaddress": ""},
    ]
    # lekko modyfikujemy żeby dane różniły się per test
    for r in rows:
        r = dict(r)
    return rows


@app.route("/")
def index():
    return render_template("index.html", tests=TESTS, active="tab1")


@app.route("/tab/<tab_id>")
def tab(tab_id):
    return render_template("index.html", tests=TESTS, active=tab_id)


@app.route("/test/<int:test_id>")
def test_view(test_id):
    return render_template("index.html", tests=TESTS, active="test", test_id=test_id)


@app.route("/api/test/<int:test_id>")
def api_test(test_id):
    return jsonify(data=sample_rows(test_id))


if __name__ == "__main__":
    app.run(debug=True, port=5000)

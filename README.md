# ShuttleStack

**ShuttleStack** is a queue system for a public badminton venue specifically in Wet Market, Iligan City, with 3 courts and a flat 50-peso entry fee. Players join the queue as a pair, a group of four, or alone, see how many teams are ahead of them, and the caretaker calls the next team. The staff dashboard has no login yet; anyone who opens /staff can use it. Login comes in a later week. To run it: create a virtual environment, run
`pip install -r requirements.txt`, then `flask --app app run --debug` and
open http://127.0.0.1:5000.
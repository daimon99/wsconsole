A websocket console.

You can use this console to remote control your machine.

# Requires

* python 3.6

# Install

```bash
pyvenv env
. env/bin/activate
pip install -r requirements.txt
```

# Run

```bash
cd src && python server.py
```

# Usage

1. Set your connect pin
    
    Modify `PIN` value in `server.py`

2. Connect using your browser

    Access [http://localhost:5678/ws-console/](http://localhost:5678/ws-console/)
    
    input the PIN you set just now.

3. Type your command to see the result.

4. Specail commands:

    * clear: clear the output
    * conn: reconnect to the server






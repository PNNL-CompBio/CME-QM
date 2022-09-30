##### build environment

```bash
conda create -n cme_api python=3.5
source activate cme_api # Activate the environment
```

##### Install dependencies

```python
pip install -r requirements.txt
```

##### Start MongoDB Server

If you're using MacOS, you could use `brew` to start the server.

```bash
brew services start mongodb
```

##### Start the application

```bash
python app.py
```

Once the application is started, go to [localhost](http://localhost:5000/) on Postman and explore the APIs.

More detail on [](../devDocs/apis.md)
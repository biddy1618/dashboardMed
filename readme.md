# MedProject for PrimeSource

Tiny project for showing the demo-dashboard for the client stakeholders of MedProject

## Getting Started

For the quick review, visit the `Testing.ipynb` file as on any Jupyter Notebook (or any other platform that reads notebook document). The demo site is tested through __Flask__ web-framework locally, and deployment is done on __Flex environment of GCP__ through the very same __Flask__ framework with __Dash__ on front-end.

### Prerequisites, installing, and deploying locally

Create __virtual environment__, activate it

```
python -m virtualenv venv venv
. venv/bin/activate
```

Locate into dashboard folder

```
cd dashboard
```

and install all required libraries listed in _'./dashboard/requirements.txt'_ by running

```
pip install requirements.txt
```

Then simply type in terminal the following to run the server locally

```
python main.py
```

Now you have the server up and running locally at your browser.

## Deployment

To deploy, __GCP__'s `gcloud` tool is used. Basically, if you have installed `gcloud` command-line tool, then you need to set your credentials and project-id, where you will be deploying your application (you can proceed without setting credentials doing it on the fly while deploying). To deploy, just type

```
gcloud app deploy
```

while staying in __dashboard/__ folder. It will read the `app.yaml`, and deploy according to configurations set up there.

That's it, you should have your application up and running on your __GCP__.

It should look like below:

![Site Preview](/siteOutlook.png)

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used (back)
* [Dash](https://dash.plot.ly/) - The dashboard-specific front-end framework (wrapper for Flask)
* [GCP](https://cloud.google.com/) - Deployment cloud

## Authors

* **Dauren Baitursyn** - *Dashboards for KazMed* - [biddy1618](https://github.com/biddy1618)

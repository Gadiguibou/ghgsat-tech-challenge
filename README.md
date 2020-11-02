# ghgsat-tech-challenge
Solution to GHGSat's tech challenge

This projects aims to create a web API using Python 3 with Django and DRF.

## Setup

First, clone this repository using your favorite method.

In order to install all the requirements, run the following command inside of the cloned repo.

```bash
python -m pip install -r requirements.txt
```

## Running the server's API in your shell

To access the server's Python shell API, run the following command inside of the mysite directory.

```bash
python manage.py shell
```

You can access, create, delete and manipulate Targets and Observations easily from here.

### Example Usage

```python
(env) ghgsat-tech-challenge/mainsite [main●] » python manage.py shell
Python 3.8.6 (default, Sep 25 2020, 09:36:53)
[GCC 10.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> # Import relevent modules
>>> from myapi.models import Target, Observation
>>> 
>>> # Create a new Target
>>> t = Target(name="new_target", latitude=45.656565, longitude=-80.999999)
>>> 
>>> # Save an image of the target
>>> t.save_image("/home/username/Downloads/new_target_image.jpg")
>>> 
>>> # Import PIL.Image to open the overlay file
>>> from PIL import Image
>>> 
>>> # Save an image of the target with the given overlay
>>> with Image.open("../plume.png") as overlay:
...     t.save_overlaid(overlay, "/home/gabriel/Downloads/new_target_overlaid.png")
>>> 
>>> # Save the Target
>>> t.save()
>>> 
>>> # Query all available targets
>>> Target.objects.all()
<QuerySet [<Target: test>, <Target: quai_ultramar>, <Target: new_target>]>
>>> 
>>> # Select a target from its primary key
>>> t = Target.objects.get(pk=1)
>>> t
<Target: test>
>>> # Delete a target
>>> Target.objects.get(id=3).delete()
(1, {'api.Target': 1})
>>> Target.objects.all()
<QuerySet [<Target: test>, <Target: quai_ultramar>]>
>>> # I won't go into more details as to how to use this API but it's more than powerful enough for our usage.
>>> quit()
```

## Accessing the admin interface from a browser

Run the following command from the `mainsite` directory.

```bash
python manage.py runserver
```

Open the [admin page](http://localhost:8000/admin/) inside your browser and log in using the following credentials:

Username: `admin`

Password: `password`

## Interacting with the REST API

You can interact with the REST API with a command-line utility like `curl` or `httpie`, through your browser using the UI provided by DRF (by just visiting the endpoint's URL), or through an API development toolchain like Postman.

### Endpoints

 - To `GET` the list of all available targets or observations or `POST` a new model instance use (`http://localhost:8000`)`/myapi/targets` or `/myapi/observations`.
 - To read, write to or delete (`GET`, `PUT`, `PATCH` or `DELETE`) a single model instance use `/myapi/targets/<id>/`
 - To `GET` an image of a target without overlay use `/myapi/targets/<id>/show/`
 - To `GET` an image of a target with the overlay use `/myapi/targets/<id>/result/`
 - To `GET` an image of the observation without the satellite imagery use `/myapi/observations/<id>/show/`
 - To `GET` an image of the observation overlaid over a satellite image of the target use `/myapi/observations/<id>/result/`
 
### Example of `POST`ing a new observation using Postman

`target` specifies the ID of the corresponding Target instance.

![postman-example-usage-screenshot](https://user-images.githubusercontent.com/34945306/97900037-20131f00-1d08-11eb-9f01-96af562a8c3d.png)

Notice you need to change the body type to `form-data` and the key type to `File` in order to add a file to your `POST` request.

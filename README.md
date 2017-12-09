Physical Gradient Descent
=========================

This is code for adapting the gradient descent algorithm to run on earth's
actual geometry. You can read more about this in the attached [blog post].

## Running gradient descent

You'll need Python 3, and can install the dependencies with:

```bash
> virtualenv -p python3 env
> source env/bin/activate
> pip install -r requirements.txt
```

And run gradient descent like so:

```bash
(env)> python gradientdescent.py 47.801686 -123.709083 ~/Downloads/srtm_12_03/srtm_12_03.tif
```

Mount olympus : python gradientdescent.py 47.801686 -123.709083 ~/Documents/physical-gradient-descent/srtm_12_03.tif
Olin College : python gradientdescent.py 42.2934 -71.2639 ~/Documents/physical-gradient-descent/srtm_22_04.tif
Mount Everest : python gradientdescent.py 27.9880 86.9252  ~/Documents/physical-gradient-descent/srtm_54_07.tif

A number of parameter tweaking options are supported:

```bash
usage: gradientdescent.py [-h] [--output OUTPUT] [--alpha ALPHA]
                          [--gamma GAMMA] [--iters ITERS]
                          lat lon tif
```

You can get TIF files from this [tile grabber]!

## Running the visualizer

The visualizer makes AJAX requests, so you will need to serve it from a web
server instead of just opening the HTML file on the filesystem. You can do that
easily with Python if you prefer, which will serve the local directory:

```bash
> python -m http.server
```

Then access http://localhost:8000 and the visualizer will start. You may have to
update the key used inside the HTML by editing the file to your own Google Maps
API key.

[tile grabber]: http://dwtkns.com/srtm/
[blog post]: https://fosterelli.co/executing-gradient-descent-on-the-earth

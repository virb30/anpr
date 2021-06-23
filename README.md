# ANPR - Automatic Number Plate Recognition

In this project we apply a series of image processing techniques to extract the 
number plate of a car image. Considering:
* The image contains just 1 car
* The plate pattern is Mercosul

## Algorithm

The following techniques sequence was applied in order to 
achiev the expected result:
1. Convert to Grayscale;
2. Black Hat Morphologial Transformations - to reveal characters
against light backgrounds;
3. Close operation to fill gaps and little areas - to identify bigger structures;
4. Calculate the magnitude gradient (of axis x) of the Black Hat Transformation result image;
    .  Put the result into [0, 255] scale
5. Smooth the image, apply another close transformation and another binary threshold using
Otsu's method.

# How to Develop

1. Clone this repo
2. Go to project folder
3. Start coding

```shell
# clone this repo
git clone https://github.com/virb30/anpr.git anpr
# cd to project folder
cd anpr
```

# How to Deploy

1. Login to Heroku Account
2. Create a new Heroku Project
3. Commit and push changes to heroku

```shell
# login to heroku account
heroku login
# create heroku project
heroku create [project-name]
# commit & push changes to heroku
git add .
git commit -m "deploy"
git push heroku master
```

# Demo 

https://number-plate-extractor.herokuapp.com/
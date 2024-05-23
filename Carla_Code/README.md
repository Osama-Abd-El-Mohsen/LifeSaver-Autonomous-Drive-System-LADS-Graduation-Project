># Installation

- ### Install Requirments (Tested On Carla 0.9.14 & Python 3.7.0)

  - Make **Virtual Environment**
  - `python -m venv venv `
  - Activate the environment
  - `venv\Scripts\activate`
  - Then Install Requirements
  - `pip install -r requirements.txt`
  - Run Town01 or Town02 Code
  - `python town01.py`

 ### Apply it on any other map 
  - **You will need to change just hospitals spawn points**
  Here with the new map positions
  ``` python
  h1 = carla.Transform(carla.Location(x=325.489990, y=273.743317, z=0.300000))
h2 = carla.Transform(carla.Location(x=176.589493, y=123.749130, z=0.300000))
h3 = carla.Transform(carla.Location(x=307.398132, y=5.570724, z=0.300000))
h4 = carla.Transform(carla.Location(x=10.509980, y=190.429993, z=0.300000))

``` 
- and dont forget to load the map here 
```python
   client.load_world("Town01")
   ```

># Output :

|Town01|Town02|
|----|----|
|https://drive.google.com/file/d/12rFK5r0yPDK6kGE8qaoomyGk-ulQi7XS/preview|https://drive.google.com/file/d/12rFK5r0yPDK6kGE8qaoomyGk-ulQi7XS/preview|
|![Town01](https://i.ibb.co/18pvsQf/Whats-App-Image-2024-05-16-at-12-45-15-6f66bb2f.jpg)|![Town02](https://i.ibb.co/18pvsQf/Whats-App-Image-2024-05-16-at-12-45-15-6f66bb2f.jpg)|

# CAMPI QUI PUGUI!

![Campers](https://github.com/SergiColl5/Camper_spots/blob/main/images/cover_camper.jpeg)

I am a camper enthusiast. I really like a nice road trip. And being able to carry around your home is concept of travelling that I love.

Sometimes though, is not that easy to find the best route, the best places to visit or (the most difficult one) the best places to spend the night. At least that’s what most in the sector say. 
	
I have personal experiences where I was expecting to just magically find a spot with the best views in the middle of the nature, but I end up sleeping in a parking lot next to a supermarket. 

It is true that exists some website that provides you with cool places and spots. But you can spend hours navigating through all of them, and mostly when you are tired after driving for a couple of hours. 

That’s why I wanted to create an application that does this work for me, way faster and way better:

Campi qui pugui!

An application where you can specify your starting locations, choose some preferences like the type of places you want to visit or the type of spots where you want to spend the night.
The application will provide you with a map where you can see the route, the locations and the spots that suits best your preferences and also the link to the places at Park4night. Basically, is planning for you the best route!

![Road](https://github.com/SergiColl5/Camper_spots/blob/main/images/road_picture.jpeg)

To achieve this goal, I had to go through 5 steps:


	


## 1.	Data extraction

First and most important of it all. What data do I need? Where can I extract it from? How can I do that?

What do I need? 
Point of interests. All those cool places that as traveller you wouldn’t like to miss. 
Spots to stay. All locations where you can park you camper and spend the night.
Geography of Spain. Geojson of the autonomous communities of Spain.

Of course, researching is the most tedious part. But luckily, I knew a web site that has all the places where people have stayed for a night before. The problem here is how to get it. 

Where can I get the data from?

Park4night: Website that people use to share the places where they have stayed during the night or spent some time during the day with a campervan or motorhome. They upload the locations, pictures, and comments and later on other people can rate that place or add more information.

Google Maps API: API used to get the points of interest near a specific location based on keywords. Also, it provides you with the directions from where you specify.

INE: Instituto Nacional de Estadística.They have a Geojson map with all the information that required.


How can I get it?

Web scraping: Navigate through all the possible endpoints within the website. Over 60.000 around Europe. Read the html and extract the correct information.

Requests to API: Perform requests with the specific parameters to get either the points of interest or the directions. Read the responses and extract the correct information.

Download Geojson: Just downloading the file and uploading it into MongoDB

For the web scraping part, the code needs to be built to prevent possible errors. Since the website had different layouts depending on the type of spot, a lot of “try and Except” had to be implemented. Also, to keep the information even if the code crashed at some point, creating loops is helpful for saving information each iteration. It might be a little more time consuming, but no one wants to lose the information after 4 hours scraping.






## 2.	Data cleaning

Once all the information is gathered, a proper cleaning must be done. In this case, it consisted of grouping and naming the categories, change the format of the coordinates, change the format of the rating, and get rid of those rows that contained null values in the coordinates field.

Also, I had to format and add fields to improve the filtering that I would perform later.

This added information consisted in finding the region within Spain that the different places were located. To do so, I queried using MongoDB the different coordinates to see what was the polygon that they were intersecting. 



## 3.	Filtering

I let the user choose and filter different parameters.
-	Starting point.
-	Points of interest.
-	Region to visit.
-	Rating.
-	Type of place the spend the night.
-	The distance between night spots.

I save these selections and then I query the SQL database to extract only those locations that matches the parameters. 
In the end the user will be selecting once, but the queries will be done to different tables.

After that, I have all possible candidates, in one side the points of interest, in the other side the possible night spots.

##4.	Calculations

This is the most challenging part. I needed to create the algorithm that returned the perfect night spots depending on three main things: the amounts of points of interest around, the rating of the spot, and the distance between spots.

This is how it works.
First, based on the region selected by the user the whole dataset is filtered. This way we work only with a small portion of it.
Second, we need to count how many points of interest each night spot has. To do so, we need to perform an intersect query taking the area around each spot and keep the count.
Third, based on the count of points of interest and rating, the candidates are ordered.
Fourth, following the order previously found. The function takes the one on top of the list and checks all the night spots that are within a radius specified by the user and mark them as a not potential spots, since the first one should be the best already. 
Fifth, having all spots ready, based on the starting point, the route is calculated to all the different locations. So the user gets an overview of what way it should take.

This was complicated because it changes depending based on filters provided by the user. Every time the queries has different arguments, so I had to adapt the functions to be flexible and capable of finding the right results. 

For example, if I choose to see mountains or beaches in Cantabria, the spots that I receive might not be the same. Could happen as well depending on the minimum rating.

## 5.	Display result

For now, I have created a Folium map where all the points of interest and night spots can be located. Extra information appears if the marker is clicked. 
Also, a list of the spots with basic information and the link to its endpoint within Park4Night, so the user can check comments or more specific information. 

## 6.	Next Steps

To continue this project, I’ll partner with my brother, who is an excellent UX/UI designer and Web Developer to create a proper website so we can help all the camper lovers. 
I would also like to improve the pipeline for the data extraction and make it more robust and efficient. 


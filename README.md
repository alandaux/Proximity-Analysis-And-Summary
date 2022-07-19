# Proximity-Analysis-And-Summary
QGIS models and spatial Python for analyzing proximity between two spatial layers, and for summarizing data by country.

These models require QGIS to run, you can find help on downloading QGIS [here](https://www.qgis.org/en/site/forusers/download.html)

To demonstrate how to use the following models, this repository contains a sample of EJAtlas data, as well as a geopackage with 2 shapefiles: simpleCountryBoundaries and protectedLandSouthAmerica. We will use the first model, [Summarize Data by Country](SummarizeDataByCountry.model3), to calculate the number of EJAtlas cases in each country with an outcome of compensation. We will use the second model, [Proximity Analysis](ProximityAnalysis.model3), to analyze how which protected lands, and how many, are in proximity to EJAtlas cases in South America.

### Adding Models to QGIS

Open a new project in QGIS and then navigate to the processing toolbox. It should be the panel on the right hand side of
your screen. If you don't see the processing toolbox, go to View > Panels > Processing Toolbox.

Hover over the gear icon in the top left of the processing toolbox, and click on Add Model To Toolbox...

![Add Model to Toolbox](/images/AddModelToToolbox.png)

Navigate to where you downloaded the github repository, and click on the model3 files to add them to your processing toolbox.

The models will now appear under the models tab near the bottom of the processing toolbox.

### Adding Data Geopackage and Data with Lat/Long Coordinates to QGIS

Navigate to your Proximity-Analysis-And-Summary folder in the QGIS browser. Drag the geopackage, ProximityAndSummaryGeopackage.gpkg into the layers panel. A new window will pop up asking which vector layers you would like to add. Make sure both layers are highlighted, then click ok.

![AddGeopackage](/images/AddGeopackage.png)

To make things easier, let's now rename our two new layers to remove the geopackage title. You can do this by right clicking on each layer and then clicking rename.

![RenameLayers](/RenameLayers.png)

Now would be a good time to save your project. Go to Project > Save As... and navigate to where you'd like to store the project.

Before we summarize our example data by country, we first need to add it to our QGIS project. *Make sure the data you wish to add to your QGIS project is saved as a CSV file!*

Go to Layer > Add Layer > Add Delimited Text Layer...

![AddCSV](/images/AddCSV.png)

In the next panel, click the ... on the right side of File Name and navigate to your CSV file. In this example, the file is titled EJAtlasCases.csv. Under Geometry Definition, make sure point coordinates are picked, the X field should be Lon, and the Y field should be Lat. Then hit add.

![AddCSV2](/images/AddCSV2.png)

Your map panel should look something like this:

![MapPanel1](/images/MapPanel1.png)

###Summarize Data by Country

Now that we have all the data we need to run our models. Let's start by using the Summarize Data By Country model to calculate the number of EJAtlas cases in each country where compensation is provided.

Navigate to the model in the processing toolbox, and double click.

![SummarizeDataByCountry1](/images/SummarizeDataByCountry1.png)

A panel will pop up with the model's interface. The right side contains instructions on how to use the model, and general descriptions of all the required inputs and outputs.

First, choose the layer that contains country boundaries. In this example, the layer is called simpleCountryBoundaries.
Then, go to the third field and select the layer containing the data you wish to summarize. In this example, the layer is called EJAtlasCases.

![SummarizeDataByCountry2](/images/SummarizeDataByCountry2.png)

In the second field, unclick the blank checkbox, and instead click on any fields with the data you wish to summarize per country. In this case, we want to summarize ConflictEvent:Compensation. Then click OK.

![SummarizeDataByCountry3](/images/SummarizeDataByCountry3.png)

Now you can either have the results output in a temporary later, or choose to save the output as a file. In this case, we can name the file compensationByCountry. You should save this layer wherever you saved your project.

![SummarizeDataByCountry4](/images/SummarizeDataByCountry4.png)

Then hit Run.

A new layer titled compensationByCountry should now appear in the layers panel on the left. Right click on that layer and click Open Attribute Table.

![OpenAttributeTable](/images/OpenAttributeTable.png)

Once it opens. You should see two new fields. The left field is the number of features counted in each country, and the right field is the summary of that data per country. In this example, the left field is the number of EJAtlas cases per country, and the right field is the number of cases per country where compensation occurred.

![compensationByCountryDataTable](/images/compensationByCountryDataTable.png)

### Proximity Analysis

First, choose the data layer in which you would like to analyze its proximity to a second data layer. The first data layer will be the input layer, the second layer will be the join layer. Also identify a field in each layer that can serve as a unique id.

As an example, we will analyze the proximity of EJAtlas cases to protected lands in North and South America. EJAtlas cases will be the input layer, and protected lands in North and South America will be the join layer. The model will output two layers. The first will be EJAtlas cases with a new field: the number of protected lands in proximity. The second will be protected lands with a new field: the number of EJAtlas cases in proximity. We can use these results to see which EJAtlas cases pose the biggest threat to protected lands, and which protected lands are most at risk from EJAtlas cases.

Let's begin. Navigate to the Proximity Analysis model in the Processing Toolbox and double click.

![ProximityAnalysis1](/images/ProximityAnalysis1.png)

The model interface should pop up. The right side contains instructions on how to use the model, and general descriptions of all the required inputs and outputs.

First let's choose our distance, the value which we will use to determine whether features are in proximity to each other. *Distance in this model is in meters.* For this example, we will consider features within 10km of each other as being in proximity, so we will set the distance to 10,000m.

Our input layer is EJAtlasCases. Our unique ID field, or Input ID, will be Conflict Id. *Remember that the Input ID and Join ID must be unique values for each feature!*

Our join layer is protectedLandSouthAmerica, and our Join ID will be fid.

Next we have to choose our projected coordinate system. Because this model measures distance, you need to choose a projected coordinate system that is localized and equidistant. Since we are analyzing protected lands in South America, we will choose the default CRS of South_America_Equidistant_Conic. There are equidistant conic projections for all areas of the world, and you can pick the one you need by clicking on the globe icon next to the Projected Coordinate System field.

![ProximityAnalysis2](/images/ProximityAnalysis2.png)

![ProximityAnalysis3](/images/ProximityAnalysis3.png)

You can choose to save the outputs to a file, or create temporary layers. For this example, we will name the Join Features with Counted Proximity as protectedLandsNearEJCases. We will name the Input Features with Counted Proximity as EJCasesNearProtectedLands.

Then hit Run.

![ProximityAnalysis4](/images/ProximityAnalysis4.png)

Two new layers should appear in the layers panel. The first layer, protectedLandsNearEJCases (join features with counted proximity) now has a new field on the far right of the attribute table ("Conflic I" in this example), which represents the number of EJAtlas cases within 10km of a protected area. Remember that you open the attribute table by right clicking on the layer, and then clicking open attribute table.

![ProximityAnalysisJoinTable](/images/ProximityAnalysisJoinTable.png)

The second layer, EJCasesNearProtectedLands (input features with counted proximity) now has a new field on the far right of the attribute table ("fid_count" in this example), which represents the number of protected lands within 10km of each EJAtlas case.

![ProximityAnalysisInputTable](/images/ProximityAnalysisInputTable.png)

Note that the new fields in your output layers are named after the unique ID chosen to identify the features in the other layer.  

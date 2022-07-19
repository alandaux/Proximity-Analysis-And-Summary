"""
Model exported as python.
Name : Summarize Data by Country
Group : 
With QGIS : 31604
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterBoolean
import processing


class SummarizeDataByCountry(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('CountryBoundaries', 'CountryBoundaries', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('DataFieldToSummarize', 'Data Field(s) To Summarize', type=QgsProcessingParameterField.Any, parentLayerParameterName='DataToSummarize', allowMultiple=True, defaultValue=''))
        self.addParameter(QgsProcessingParameterVectorLayer('DataToSummarize', 'Data To Summarize', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Datasummarizedbycountry', 'dataSummarizedByCountry', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': parameters['CountryBoundaries'],
            'JOIN': parameters['DataToSummarize'],
            'JOIN_FIELDS': parameters['DataFieldToSummarize'],
            'PREDICATE': [0],
            'SUMMARIES': [0,5],
            'OUTPUT': parameters['Datasummarizedbycountry']
        }
        outputs['JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Datasummarizedbycountry'] = outputs['JoinAttributesByLocationSummary']['OUTPUT']
        return results

    def name(self):
        return 'Summarize Data by Country'

    def displayName(self):
        return 'Summarize Data by Country'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def shortHelpString(self):
        return """<html><body><h2>Algorithm description</h2>
<p>You can use this model to summarize data by country. It will count the number of data points per country, and summarize the chosen data field.</p>
<h2>Input parameters</h2>
<h3>CountryBoundaries</h3>
<p></p>
<h3>Data Field(s) To Summarize</h3>
<p>Fields to sum together at the country level. Summaries can be calculated for one or more fields. </p>
<h3>Data To Summarize</h3>
<p>Vector layer containing the data you wish to summarize</p>
<h3>dataSummarizedByCountry</h3>
<p>Outputs a data table with one row per country, with new data fields: count (number of data points summarized for each country) and sum (summed values of chosen data field by country)</p>
<h3>Verbose logging</h3>
<p></p>
<h2>Outputs</h2>
<h3>dataSummarizedByCountry</h3>
<p>Outputs a data table with one row per country, with new data fields: count (number of data points summarized for each country) and sum (summed values of chosen data field by country)</p>
<br><p align="right">Algorithm author: Arielle Landau</p></body></html>"""

    def createInstance(self):
        return SummarizeDataByCountry()

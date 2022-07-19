"""
Model exported as python.
Name : Proximity Analysis
Group : 
With QGIS : 31604
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterCrs
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterBoolean
import processing


class ProximityAnalysis(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterNumber('Distance', 'Distance', type=QgsProcessingParameterNumber.Double, minValue=0, defaultValue=10000))
        self.addParameter(QgsProcessingParameterVectorLayer('Input', 'Input', defaultValue=None))
        self.addParameter(QgsProcessingParameterField('InputID', 'Input ID', type=QgsProcessingParameterField.Any, parentLayerParameterName='Input', allowMultiple=False, defaultValue=''))
        self.addParameter(QgsProcessingParameterField('JoinID', 'Join ID', type=QgsProcessingParameterField.Any, parentLayerParameterName='JoinLayer', allowMultiple=False, defaultValue=''))
        self.addParameter(QgsProcessingParameterVectorLayer('JoinLayer', 'Join Layer', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterCrs('ProjectedCoordinateSystem', 'Projected Coordinate System', defaultValue='ESRI:102032'))
        self.addParameter(QgsProcessingParameterFeatureSink('JoinFeaturesWithCountedProximity', 'Join Features with Counted Proximity', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('InputFeaturesWithCountedProximity', 'Input Features with Counted Proximity', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Reproject layer
        alg_params = {
            'INPUT': parameters['Input'],
            'OPERATION': '',
            'TARGET_CRS': parameters['ProjectedCoordinateSystem'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': parameters['Distance'],
            'END_CAP_STYLE': 0,
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': parameters['JoinLayer'],
            'JOIN': outputs['Buffer']['OUTPUT'],
            'JOIN_FIELDS': parameters['InputID'],
            'PREDICATE': [0],
            'SUMMARIES': [0],
            'OUTPUT': parameters['JoinFeaturesWithCountedProximity']
        }
        outputs['JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['JoinFeaturesWithCountedProximity'] = outputs['JoinAttributesByLocationSummary']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer']['OUTPUT'],
            'JOIN': parameters['JoinLayer'],
            'JOIN_FIELDS': parameters['JoinID'],
            'PREDICATE': [0],
            'SUMMARIES': [0],
            'OUTPUT': parameters['InputFeaturesWithCountedProximity']
        }
        outputs['JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['InputFeaturesWithCountedProximity'] = outputs['JoinAttributesByLocationSummary']['OUTPUT']
        return results

    def name(self):
        return 'Proximity Analysis'

    def displayName(self):
        return 'Proximity Analysis'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def shortHelpString(self):
        return """<html><body><h2>Algorithm description</h2>
<p>You can use this model to calculate how many of one set of features, is within a set proximity or distance of another set of features. </p>
<h2>Input parameters</h2>
<h3>Distance</h3>
<p>Distance, in m, used to measure if the input features are in close proximity to the join features. </p>
<h3>Input</h3>
<p>Layer where geographic features will be expanded to calculate the proximity of the features in the join layer. </p>
<h3>Input ID</h3>
<p>Unique ID for the input layer.</p>
<h3>Join ID</h3>
<p>Unique ID for the join layer. </p>
<h3>Join Layer</h3>
<p>Layer whose features are evaluated to see how many of the input layer's features are in its proximity. </p>
<h3>Projected Coordinate System</h3>
<p>CRS used to reproject input layer. Choose a projected coordinate system for the geographic area of the input layer. The default is a equidistant conic projection for South America.</p>
<h3>Join Features with Counted Proximity</h3>
<p></p>
<h3>Input Features with Counted Proximity</h3>
<p></p>
<h3>Verbose logging</h3>
<p></p>
<h2>Outputs</h2>
<h3>Join Features with Counted Proximity</h3>
<p></p>
<h3>Input Features with Counted Proximity</h3>
<p></p>
<br><p align="right">Algorithm author: Arielle Landau</p></body></html>"""

    def createInstance(self):
        return ProximityAnalysis()

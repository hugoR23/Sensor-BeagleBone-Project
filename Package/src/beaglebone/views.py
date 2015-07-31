'''
@Author: Hugo Robellaz
Configuration of the templates and the route to Display
'''
from pyramid.view import view_config
from pyramid.response import FileResponse
from datetime import datetime, timedelta

from globals import TEMP,HUMI,LUMI,PRES
from layouts import Layouts
import graph, data

class ProjectorViews(Layouts):

    def __init__(self, request):
        self.request = request
        self.data= data.Data()
        self.graph= graph.Graph(self.data)

    @view_config(renderer="templates/index.pt")
    def index_view(self):
        latestData=self.data.getLatestData()
        pageData={"title": "Home"}
        pageData.update(latestData)
        return pageData
	
    @view_config(renderer="templates/detailed.pt", name="temperature")
    def temp_view(self):
        mainData=self.data.getMainData(TEMP['id'], self.getDate())
        pageData=TEMP
        pageData.update(mainData)
        return pageData
		
    @view_config(renderer="templates/detailed.pt", name="pressure")
    def pressure_view(self):
        mainData=self.data.getMainData(PRES['id'], self.getDate())
        pageData=PRES
        pageData.update(mainData)
        return pageData
		
    @view_config(renderer="templates/detailed.pt", name="luminance")
    def luminance_view(self):
        mainData=self.data.getMainData(LUMI['id'], self.getDate())
        pageData=LUMI
        pageData.update(mainData)
        return pageData

    @view_config(renderer="templates/detailed.pt", name="humidity")
    def humidity_view(self):
        mainData=self.data.getMainData(HUMI['id'], self.getDate())
        pageData=HUMI
        pageData.update(mainData)
        return pageData

    @view_config(route_name='mainPlot')
    def mainPlot_view(self):
        response = FileResponse(
            self.graph.produceMain(self.HTML_GET('sensorType'),self.getDate()),
            request=self.request,
            content_type='image/png'
            )
        return response

    @view_config(route_name='smallPlot')
    def smallPlot_view(self):
        response = FileResponse(
            self.graph.produceSmall(self.HTML_GET('sensorType')),
            request=self.request,
            content_type='image/png'
            )
        return response

		
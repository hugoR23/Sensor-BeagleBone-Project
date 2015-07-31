'''
@Author: Hugo Robellaz
Additional functions to help render the HTML pages
'''
from pyramid.renderers import get_renderer
from pyramid.decorator import reify
from datetime import datetime, timedelta


class Layouts(object):

    @reify
    def global_template(self):
        renderer = get_renderer("templates/global_layout.pt")
        return renderer.implementation().macros['layout']

    def HTML_GET(self,item):
        return self.request.GET[item] if(self.request.GET.keys().count(item)) else 0

    #Return a string representing the date or time to display by default in the HTML input
    def getDateToPrint(self,inputName):
        today=datetime.today()
        value=self.HTML_GET(inputName)
        if value!=0:
            return value
        elif inputName=='toDate':
            return today.strftime('%d/%m/%y')
        elif inputName=='fromDate':
            value=today-timedelta(hours=24)
            return value.strftime('%d/%m/%y')
        elif (inputName=='toHour' or inputName=='fromHour'):
            return today.strftime('%H:%M')
        else:
            return 0

    #Returns a tuple of datetime objects representing the time interval received by the GET method for which we want the data displayed
    def getDate(self):
        today=datetime.today()
        custom=self.HTML_GET('custom')
        deltaTime=self.HTML_GET('deltaTime')
        deltaTime=86400 if (deltaTime==0 and custom==0) else int(deltaTime)
        if custom!=0:
            fromTime=datetime.strptime(self.HTML_GET('fromDate')+" "+self.HTML_GET('fromHour'),"%d/%m/%y %H:%M")
            toTime=datetime.strptime(self.HTML_GET('toDate')+" "+self.HTML_GET('toHour'),"%d/%m/%y %H:%M")
        else:
            fromTime=today-timedelta(seconds=deltaTime)
            toTime=today
        return(fromTime,toTime)

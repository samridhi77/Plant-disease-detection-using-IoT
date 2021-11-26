from django.shortcuts import render_to_response
from django.template import RequestContext
import requests
import xively
FEED_ID="feed_id"
API_KEY="api_key"
api=xively.XivelyAPIClient(API_KEY)

feed=api.feeds.get(FEED_ID)

temp_datastream=feed.datastream.get("temperature")
humidity_datastream=feed.datastream.get("humidity")
rgb_datastream=feed.datastream.get("rgb")

def home(request):
    temperature=temp_datastream.current_value
    humidity_datastream=humidity_datastream.current_value
    rgb_datastream=rgb_datastream.current_value
    return render_to_response('index.html','Temp range:15-30,Humidity range:30%-50%, Rgb range:15-30','temperature':temperature,'humidity':humidity,'rgb':rgb,context_instance=RequestContext(request))

import math, datetime
from tempodb import Client, DataPoint
API_KEY = "8d5a615fbac449a3ba56ab2520922ee3"
API_SECRET = "143e9b1785604f7daf2c6d864f861c39"

def import_samples():
	sin = [math.sin(math.radians(d)) for d in range(0,3600)]
	cos = [math.cos(math.radians(d)) for d in range(0,3600)]

	sin_data = []
	cos_data = []
	start_time = datetime.datetime(2013,07,26)
	for i in range(len(sin)):
		current_time =  start_time + datetime.timedelta(minutes=i)
		sin_data.append(DataPoint(current_time, sin[i]))
		cos_data.append(DataPoint(current_time, cos[i]))

	client = Client(API_KEY, API_SECRET)
	client.write_key('type:trig.function:sin.1',sin_data)
	client.write_key('type:trig.function:cos.1', cos_data)


def read_samples():
	client = Client(API_KEY, API_SECRET)
	start_time = datetime.datetime(2013,07,26)
	end_time = start_time + datetime.timedelta(minutes=3600)
	dataset = client.read_key('type:trig.function:sin.1', start_time, end_time, interval="1min")
	print "Average of sin", round(dataset.summary.mean)
	print "Max of sin", dataset.summary.max


	attributes={
				"function": "sin"
				}

	datasets = client.read(start_time, end_time, attributes=attributes)

	for dset in datasets:
		print "Average of %s" % dset.series.attributes['function'], round(dset.summary.mean)

	attrs={'type':'trig'}
	datasets = client.read(start_time, end_time, attributes=attrs)
	for dset in datasets:
		print "Average of %s" % dset.series.attributes['function'], round(dset.summary.mean)
		
if __name__=="__main__":
	read_samples()
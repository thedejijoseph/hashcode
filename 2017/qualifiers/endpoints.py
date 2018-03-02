import os
import sys
import logging

logging.basicConfig(
	level=logging.DEBUG,
	format="%(asctime)s | %(levelname)s | %(message)s"
)

class Cache():
	def __init__(self, id, size):
		self.id = int(id)
		self.size = int(size)
		
		self.content = []
	
	def add(self, video):
		if self.space_left() >= video.size:
			self.content.append(video)
		else:
			print("video size is larger than the available space")
			return
	
	def space_left(self):
		in_place = 0
		for video in self.content:
			in_place += video.size
		
		return self.size - in_place
	
	def __repr__(self):
		return f"Cache {self.id}; Size {self.size}"

class Endpoint():
	def __init__(self, id, video_requests, cache_connections):
		self.id = id
		self.requests = video_requests
		self.caches = cache_connections
		
		self.datacenter = 0
	
	# where:
		# EP is endpoint
		# VR is video requests
		# CC is cache conections
	def __repr__(self):
		return f"EP {self.id}; {len(self.requests)} VR(s); {len(self.caches)} CC(s)"

class Video():
	def __init__(self, id, size):
		self.id = int(id)
		self.size = int(size)
	
	def __repr__(self):
		return f"Video {self.id}; Size {self.size}"

class Request():
	def __init__(self, video, endpoint, freq):
		self.video = video
		self.endpoint = endpoint
		self.freq = freq
	
	def __repr__(self):
		return f"Request for Video {self.video.id}; Frq: {self.freq}"

class CacheConnection():
	def __init__(self, cache_id, latency):
		self.cache_id = cache_id
		self.latency = latency

videos = []
endpoints = []
requests = []
caches = []

print("example, zoo, spread, trending, kittens")
print("are available datasets.")

input_dataset = input("what should we crunch: ").strip()
path = os.path.join('input', input_dataset)

if os.path.exists(path):
	pass
else:
	print(f"{input_dataset} is not an available dataset")
	sys.exit()

logging.info("opening dataset")

dataset = open(path, 'r')
submission = open("output/example", 'w')

logging.info("digesting dataset")

# stage 1
dataset_info = dataset.readline().strip('\n').split(' ')

# stage 2
the_videos = dataset.readline().strip('\n').split(' ')
no_of_videos = int(dataset_info[0])

for video_no in range(no_of_videos):
	id = video_no
	size = the_videos[id]
	
	videos.append(Video(id, size))

# stage 3
no_of_endpoints = int(dataset_info[1])
for endpoint_no in range(no_of_endpoints):
	endpoint_info = dataset.readline().strip('\n').split(' ')
	
	datacenter_latency = int(endpoint_info[0])
	cache_connections = int(endpoint_info[1])
	
	its_caches = []
	
	for cache_no in range(cache_connections):
		cache_info = dataset.readline().strip('\n').strip()
		
		cache_id = cache_info[0]
		latency = cache_info[1]
		
		cache_connection = CacheConnection(cache_id, latency)
		
		its_caches.append(cache_connection)
	
	endpoint_id = endpoint_no
	cache_connections = its_caches
	
	endpoint = Endpoint(endpoint_id, cache_connections)
	endpoint.datacenter = datacenter_latency
	
	endpoints.append(endpoint)

# stage 4
no_of_requests = int(dataset_info[2])
for request_no in range(no_of_requests):
	request = dataset.readline().strip('\n').split(' ')
	
	video_id = int(request[0])
	video = videos[video_id]
	
	endpoint_id = int(request[1])
	endpoint = endpoints[endpoint_id]
	
	freq = int(request[2])
	
	request = Request(video, endpoint, freq)
	
	target_endpoint = endpoints[endpoint_id]
	
	target_endpoint.requests.append(request)
	requests.append(request)

logging.info("digest complete")

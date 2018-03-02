import os
from operator import attrgetter
import threading
import logging

logging.basicConfig(
	level = logging.DEBUG,
	format = "%(asctime)s | %(levelname)s | %(message)s"
)

logging.disable(logging.DEBUG)

file = input("dataset to open: ")
path = os.path.join('input', file)

dataset = open(path, 'r')
logging.info("dataset is open")

class Cache():
	def __init__(self, id, size):
		self.id = id
		self.size = size
		
		self.content = []
	
	def add(self, video):
		self.content.append(video)
	
	def space_left(self):
		total = 0
		for video in self.content:
			total += video.size
		
		return self.size - total
	
	def empty(self):
		if self.space_left() == self.size:
			return True
		else:
			return False

class CacheConnection():
	def __init__(self, cache_id, latency):
		self.id = int(cache_id)
		self.latency = int(latency)

class Endpoint():
	def __init__(self, id, dc_latency, cache_pool):
		self.id = int(id)
		self.latency = int(dc_latency)
		self.cache_pool = sorted(cache_pool, key=attrgetter('latency'))

class Video():
	def __init__(self, id, size):
		self.id = int(id)
		self.size = int(size)
	
	def __repr__(self):
		return f"V {self.id} ; S {self.size}"

class Request():
	def __init__(self, video, endpoint, freq):
		self.video = video
		self.endpoint = endpoint
		self.freq = int(freq)

logging.info("parsing dataset")
dataset_info = dataset.readline().strip('\n').split(' ')

no_of_videos = int(dataset_info[0])
no_of_endpoints = int(dataset_info[1])
no_of_requests = int(dataset_info[2])
no_of_caches = int(dataset_info[3])
cache_size = int(dataset_info[4])

caches = []
for no in range(no_of_caches):
	cache_id  = no
	cache = Cache(cache_id, cache_size)
	
	caches.append(cache)

video_sizes = dataset.readline().strip('\n').split(' ')
videos  = []
for no in range(no_of_videos):
	video_id = no
	video_size = video_sizes[video_id]
	
	video = Video(video_id, video_size)
	videos.append(video)

endpoints = []
def parse_endpoints():
	logging.debug('parsing endpoints')
	for endpt in range(no_of_endpoints):
		endpt_desc = dataset.readline().strip('\n').split(' ')
		
		endpt_id  = int(endpt)
		dc_latency = int(endpt_desc[0])
		no_of_cc = int(endpt_desc[1])
		cache_pool = []
		
		for cc in range(no_of_cc):
			cc_desc = dataset.readline().strip('\n').split(' ')
			
			cache_id = int(cc_desc[0])
			latency = int(cc_desc[1])
			
			CC = CacheConnection(cache_id, latency)
			cache_pool.append(CC)
		
		endpoint  = Endpoint(endpt_id, dc_latency, cache_pool)
		endpoints.append(endpoint)
	logging.debug('\tendpoints parsed')
parsing_endpoints = threading.Thread(target=parse_endpoints, daemon=True)
parsing_endpoints.start()

request_pool = []
def parse_requests():
	logging.debug('parsing requests')
	for req in range(no_of_requests):
		req_desc = dataset.readline().strip('\n').split(' ')
		
		video_id = int(req_desc[0])
		video = videos[video_id]
		
		endpoint_id = int(req_desc[1])
		endpoint = endpoints[endpoint_id]
		
		freq = int(req_desc[2])
		
		request = Request(video, endpoint, freq)
		request_pool.append(request)
	logging.debug('\trequests parsed')
parsing_requests = threading.Thread(target=parse_requests, daemon=True)
parsing_requests.start()

logging.info("\tdone parsing dataset")

dataset.close()
logging.info("closed dataset")

def present(video, cache):
	if not cache.content:
		return False
	
	if cache.content:
		for vid in cache.content:
			if video.id == vid.id:
				return True
			else:
				return  False

def it_fits(video, cache):
	if video.size  > cache.size:
		return False
	if video.size <= cache.space_left():
		return True

def move(video, cache_no=0):
	if cache_no < max_cache:
		select_cache = endpoint.cache_pool[cache_no]
		cache = caches[select_cache.id]
		if present(video, cache) == False:
			if it_fits(video, cache):
				cache.add(video)
				return
			else:
				cache_no += 1
				move(video, cache_no)

logging.info("solving request pool")
def solve():
	logging.debug('solve thread started')
	request_pool = sorted(request_pool, key=attrgetter('freq'), reverse=True)
	for request in request_pool:
		endpoint = request.endpoint
		video = videos[request.video.id]
		
		if endpoint.cache_pool:
			max_cache = len(endpoint.cache_pool)
			move(video)
	logging.debug('solve thread finished')

solve_thread = threading.Thread(target=solve, daemon=True)
solve_thread.start()

logging.info("\tdone")

logging.info("refining solutions")
solution = []
used = []
for cache in caches:
	if not cache.empty():
		used.append(cache)

solution.append(str(len(used)))

for cache in caches:
	if not cache.empty():
		videos = list(set([str(video.id) for video in cache.content]))
		
		result = str(cache.id) + ' ' + ' '.join(videos)
		solution.append(result)
logging.info("\tdone")

path = os.path.join('output', file)
submission = open(path, 'w')
logging.info("submission file is open")
logging.info("writing solutions")

for line in solution:
	submission.write(line + '\n')
logging.info("\tdone")

submission.close()
logging.info("submission file is closed")
logging.info("we're done here")

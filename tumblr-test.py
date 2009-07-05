# -*- coding: utf-8 -*-

# Copyright 2008 Ryan Cox ( ryan.a.cox@gmail.com ) All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import sys
from tumblr import Api, TumblrAuthError, TumblrRequestError, TumblrError

BLOG = 'YOU.tumblr.com'
USER = 'YOUREMAIL'
PASSWORD = 'YOURPASSWORD'

class TumblrTests(unittest.TestCase):

	def testFixNames(self):
		api = Api(BLOG)
		before = {}
		before['test_one'] = 1 
		before['test_two'] = 1 

		after = api._fixnames(before)
		assert not 'test_one' in after
		assert 'test-one' in after

		assert 'test-two' in after
		assert not 'test_two' in after

	def testRequiredArgs(self):
		api = Api(BLOG, USER, PASSWORD)
		self.assertRaises(TumblrError, api.write_regular)
		self.assertRaises(TumblrError, api.write_quote)
		self.assertRaises(TumblrError, api.write_photo)
		self.assertRaises(TumblrError, api.write_photo, source='foo', data='bar')
		self.assertRaises(TumblrError, api.write_conversation)
		self.assertRaises(TumblrError, api.write_link)
		self.assertRaises(TumblrError, api.write_video )

	def testWrite(self):
		api = Api(BLOG, USER, PASSWORD)

		newpost = api.write_regular('title','body')
		post = api.read(newpost['id'])
		assert newpost['id'] == post['id']

		newpost = api.write_link('http://www.google.com')
		post = api.read(newpost['id'])
		assert newpost['id'] == post['id']

		newpost = api.write_quote('it was the best of times...')
		post = api.read(newpost['id'])
		assert newpost['id'] == post['id']

		newpost = api.write_conversation('me: wow\nyou: double wow!')
		post = api.read(newpost['id'])
		assert newpost['id'] == post['id']

		newpost = api.write_video('http://www.youtube.com/watch?v=60og9gwKh1o')
		post = api.read(newpost['id'])
		assert newpost['id'] == post['id']

		newpost = api.write_photo('http://www.google.com/intl/en_ALL/images/logo.gif')
		post = api.read(newpost['id'])
		assert newpost['id'] == post['id']

	def testRead(self):
		api = Api(BLOG)
		freq = {}
		posts = api.read()
		total = 0
		for post in posts:
			total += 1
			type = post['type']
			try:
				freq[type] += 1
			except:
				freq[type] = 1
		assert total > 0
		for type in freq:
			assert self.countType(api,type) == freq[type]

	def countType(self, api, t):
		posts = api.read(type=t)
		i = 0
		for post in posts: 
			i += 1
		return i
		
	def testAuthenticate(self):
		api = Api(BLOG, USER, PASSWORD )
		api.auth_check()

	def testBadAuthenticate(self):
		api = Api(BLOG, USER, 'badpassword' )
		try:
			api.auth_check()
			assert False # should never get here	
		except TumblrAuthError,  e:
			pass

if __name__ == "__main__":
	unittest.main(argv=sys.argv)


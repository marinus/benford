"""
Benford's Law for Splunk by Marinus van Aswegen (mvanaswegen AT gmail.com) v0.1

inspired by Christian S. Perone (christian.perone AT gmail.com) 

Examples

  | benford field=value | table digit value benford
  | benford field=value digit=2 | table digit value benford 


Copyright 2010 Marinus van Aswegen. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY MARINUS VAN ASWEGEN ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL MARINUS VAN ASWEGEN OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Marinus van Aswegen.

"""

import splunk.Intersplunk
import sys
import math

def benford_law():
	""" calculate the benford distribution """
	return [math.log10(1+1/float(i))*100.0 for i in xrange(1,10)]

def calc_digit(dataset, digit=1):
	xdigit = []
	for value in dataset:
		try:
			xdigit.append(str(value)[int(digit)-1])
		except:
			pass

	distr = [xdigit.count(str(i))/float(len(dataset))*100 for i in xrange(1, 10)]

	return distr

try:   

        keywords,options = splunk.Intersplunk.getKeywordsAndOptions()

	if not options.has_key('field'):
		splunk.Intersplunk.generateErrorResults("no field specified")
		exit(0)

        digit = options.get('digit', '1')
	field = options.get('field', None)

	dataset = []
	benford_dist = benford_law()
							
	# get the previous search results
	results,unused1,unused2 = splunk.Intersplunk.getOrganizedResults()

	# build a dataset
	for result in results:
		dataset.append(result[field])

	# get the distribution of the dataset		
	dataset_dist = calc_digit(dataset, digit)	

	# add new fields
	results = []

	for digit in range(1,10):
		temp = {}
		temp['benford'] = benford_dist[digit-1]
		temp[field] = dataset_dist[digit-1]
		temp['digit'] = digit
		results.append(temp)

	# output results
	splunk.Intersplunk.outputResults(results)

except Exception, e:
	results = splunk.Intersplunk.generateErrorResults(str(e))



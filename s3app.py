import sys
import boto.s3.connection

access_key = 'your-s3-access-key'
secret_key = 'you-s3-secret-key'
conn = boto.connect_s3(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        host='yout-gateway-host', port=7480,
        is_secure=False, calling_format=boto.s3.connection.OrdinaryCallingFormat(),
       )
#bucket = conn.create_bucket('my-new-bucket')


#sys.argv
#[1]: bucket or object
#[2]: operation create list delete
#[3]: bucket name/object name

if(len(sys.argv) <3):
	print "error, see the documentation"

elif(len(sys.argv) >= 3 and sys.argv[1] == "bucket"):
	
	operation = sys.argv[2]
	
	#List all bucket
	#Usage: python s3app.py bucket list
	if(operation == "list"):
		bucket = conn.get_all_buckets()
		json = '{"data": ['
		for index in range(0,len(bucket)):
			if(index == len(bucket)-1):
				json += '{"name": "' + bucket[index].name + '", "created":"' + bucket[index].creation_date + '"}]}'
				#print "{'name': '" + bucket[index].name + "', 'created':'" + bucket[index].creation_date + "'}]"
			else:
				json += '{"name": "' + bucket[index].name + '", "created": "' + bucket[index].creation_date + '"},'
				#print "{'name': '" + bucket[index].name + "', 'created':'" + bucket[index].creation_date + "'},",
		print json


	#List a bucket contents
	#Auto create bucket if it's not created
	#Usage: python s3app.py bucket content <bucketname>
	elif (operation == "content"):
		bucketname = sys.argv[3]
		bucket = conn.create_bucket(bucketname)

		counter = 0
		for key in bucket.list():
			counter+=1

		json = '{"data": ['
		index  = 0
		for key in bucket.list():
			zz = key.get_acl()
			gr = zz.acl.grants
			if (len(gr)) > 1:
				pm = gr[0].permission
			else:
				pm = gr[0].permission
			index+= 1
			if(index==counter):
				json += '{"name": "' + key.name + '", "size": "' + str(key.size) + '", "last_modified": "' + key.last_modified + '","acl":"'+pm+'"}]}'
			else:
				json += '{"name": "' + key.name + '", "size": "' + str(key.size) + '", "last_modified": "' + key.last_modified + '","acl":"'+pm+'"},'
		if counter < 1:
			json = '{"data":""}'
		print json

	#Create new bucket
	#Usage: python s3app.py bucket create <bucketname>
	elif (operation == "create"):
		bucketname = sys.argv[3]
		conn.create_bucket(bucketname)
		json = '{ "data": "success creating bucket: ' + bucketname + '"}' 
		print json

	#Delete a bucket
	#Usage: python s3app.py bucket delete <bucketname>
	elif (operation == "delete"):
		bucketname = sys.argv[3]
		conn.delete_bucket(bucketname)
		json = '{ "data": "success deleting bucket: ' + bucketname + '"}' 
		print json

elif(len(sys.argv) >= 3 and sys.argv[1] == "object"):
	
	operation = sys.argv[2]

	#Create a new object
	#The content of the object is optional, available in 4th argument if exists
	#Usage: python s3app.py object create <bucketname> <objectname> <objectcontent>
	if(operation == "create"):
		bucketname = sys.argv[3]
		objectname = sys.argv[4]
		objectcontent = sys.argv[5]

		bucket = conn.create_bucket(bucketname)
		key = bucket.new_key(objectname)
		key.set_contents_from_string(objectcontent)
		key.set_canned_acl('public-read')
		json = '{ "data": "success creating bucket: ' + objectname + '"}' 
		print json

	#Change an object's ACL
	#Public or Private are set on the 3th argument, default is public
	#Usage: python s3app.py object acl <bucketname> <objectname> <permission>
	elif(operation == "acl"):
		bucketname = sys.argv[3]
		objectname = sys.argv[4]
		permission = sys.argv[5]

		bucket = conn.create_bucket(bucketname)
		if(permission == "private"):
			plans_key = bucket.get_key(objectname)
			plans_key.set_acl('private')
			json = '{ "data": "' + objectname + '" permission is set to private}' 
			print json
		else:
			plans_key = bucket.get_key(objectname)
			plans_key.set_acl('public-read')
			json = '{ "data": "' + objectname + '" permission is set to public}' 
			print json

	#Delete an object
	#Usage: python s3app.py object delete <bucketname> <objectname>
	elif(operation == "delete"):
		bucketname = sys.argv[3]
		objectname = sys.argv[4]

		bucket = conn.create_bucket(bucketname)
		bucket.delete_key(objectname)
		json = '{ "data": "success deleting object: ' + objectname + '"}' 
		print json

	#Create a downloadable link
	#Usage: python s3app.py object download <bucketname> <objectname>
	elif(operation == "download"):
		bucketname = sys.argv[3]
		objectname = sys.argv[4]

		bucket = conn.create_bucket(bucketname)
		hello_key = bucket.get_key(objectname)
		hello_url = hello_key.generate_url(3600, query_auth=False, force_http=False)
		json = '{ "data": "' + hello_url + '"}' 
		print json
	#Detail an Objet of Bucket
	#Usage: python s3app.py object detail <bucketname> <objectname>
	elif(operation=="detail"):
		bucketname = sys.argv[3]
		objectname = sys.argv[4]

		bucket = conn.get_bucket(bucketname)
		key = bucket.lookup(objectname)
		x = (key.get_acl()).acl.grants
		if (len (x) > 1):
			pm = x[0].permission
		else:
			pm = x[0].permission
		
		json = '{"data":[{"name": "' + key.name + '", "size": "' + str(key.size) + '", "last_modified": "' + key.last_modified + '","acl":"'+pm+'"}]}'
		print json

else:
	print "Bad request"

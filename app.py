#!flask/bin/python
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

#Bucket Operation

@app.route('/s3/bucket/list', methods=['GET'])
def s3_bucket_list():
	output = subprocess.Popen(["python", "s3app.py", "bucket", "list"], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/s3/bucket/create/<string:bucketname>')
def s3_bucket_create(bucketname):
	output = subprocess.Popen(["python", "s3app.py", "bucket", "create", bucketname], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/s3/bucket/delete/<string:bucketname>')
def s3_bucket_delete(bucketname):
	output = subprocess.Popen(["python", "s3app.py", "bucket", "delete", bucketname], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/s3/bucket/content/<string:bucketname>')
def s3_bucket_content(bucketname):
	output = subprocess.Popen(["python", "s3app.py", "bucket", "content", bucketname], stdout=subprocess.PIPE).communicate()[0]
	return output	


#Object Operation

@app.route('/s3/object/create/<string:bucketname>/<string:objectname>/<string:objectcontent>')
def s3_object_create(bucketname, objectname, objectcontent):
	output = subprocess.Popen(["python", "s3app.py", "object", "create", bucketname, objectname, objectcontent], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/s3/object/acl/<string:bucketname>/<string:objectname>/<string:permission>')
def s3_object_acl(bucketname, objectname, permission):
	output = subprocess.Popen(["python", "s3app.py", "object", "acl", bucketname, objectname, permission], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/s3/object/delete/<string:bucketname>/<string:objectname>')
def s3_object_delete(bucketname, objectname):
	output = subprocess.Popen(["python", "s3app.py", "object", "delete", bucketname, objectname], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/s3/object/download/<string:bucketname>/<string:objectname>')
def s3_object_download(bucketname, objectname):
	output = subprocess.Popen(["python", "s3app.py", "object", "download", bucketname, objectname], stdout=subprocess.PIPE).communicate()[0]
	return output

@app.route('/s3/object/detail/<string:bucketname>/<string:objectname>')
def s3_object_detail(bucketname, objectname):
	output = subprocess.Popen(["python", "s3app.py", "object", "detail", bucketname, objectname], stdout=subprocess.PIPE).communicate()[0]
	return output

if __name__ == '__main__':
    app.run(host='0.0.0.0')

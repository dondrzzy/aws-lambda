import boto3
import cStringIO
import os
from PIL import Image, ImageOps

s3 = boto3.client("s3")
size = int(os.environ['THUMBNAIL_SIZE'])


def s3_thumbnail_generator(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # get the image
    image = get_s3_image(bucket, key)
    # resize the image
    thumbnail = image_to_thumbnail(image)
    # get the new filename
    thumbnail_key = new_filename(key)
    print('thumbnail: ', thumbnail_key)
    # upload the file
    bucket = "donald-s3-thumbnail-generator-final-bucket"
    url = upload_to_s3(bucket, thumbnail_key, thumbnail)

def get_s3_image(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    image_content = response['Body'].read()
    file = cStringIO.StringIO(image_content)
    img = Image.open(file)
    return img

def image_to_thumbnail(img):
    return ImageOps.fit(img, (size, size), Image.ANTIALIAS)

def new_filename(key):
    key_split = key.rsplit('.', 1)
    return key_split[0] + "_thumbnail.png"

def upload_to_s3(bucket, key, image):
    # save the image into a cStringIO object to avoid writing to a disk
    out_thumbnail = cStringIO.StringIO()
    # must specify the file type
    image.save(out_thumbnail, 'PNG')
    out_thumbnail.seek(0)
    x3 = boto3.resource('s3')
    obj = x3.Object(bucket, key)
    r = obj.put(Body=out_thumbnail)

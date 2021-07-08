import unittest
import app.util.aws.s3 as s3
import boto3
import io

FILE_NAME = 'tests/test_content/testFile.txt'
OBJ_NAME = 'test_user/housing/testFile.txt'
BUCKET = 'houseit'
USER_NAME = 'test_user'
PREFIX = 'test_user/housing'
UNUSED_CATEGORY = 'abcd'
IMG1 = 'app/assets/room_mock_images/1.jpg'
IMG2 = 'app/assets/room_mock_images/2.jpg'
IMG3 = 'app/assets/room_mock_images/3.jpg'
IMG4 = 'app/assets/room_mock_images/4.jpg'

class TestS3(unittest.TestCase):

    def test_upload_and_delete_file_wname(self):
        self.assertEqual(s3.upload_file_wname(FILE_NAME, BUCKET), True)
        self.assertEqual(s3.delete_file_wname(FILE_NAME, BUCKET), True)

        self.assertEqual(s3.upload_file_wname(FILE_NAME, BUCKET, OBJ_NAME), True)
        self.assertEqual(s3.delete_file_wname(FILE_NAME, BUCKET), True)

    def test_upload_file_wobject(self):
        with open(FILE_NAME, 'rb') as FILE_OBJ:
            self.assertEqual(s3.upload_file_wobject(FILE_OBJ, BUCKET, OBJ_NAME), True)
            
        with open(FILE_NAME, 'rb') as FILE_OBJ:  
            self.assertEqual(s3.upload_file_wobject(FILE_OBJ, BUCKET), True)


    def test_delete_folder(self):
        # when folder does not exist
        self.assertEqual(s3.delete_folder(PREFIX, BUCKET), True)

        # when folder exists
        s3.upload_file_wname(FILE_NAME, BUCKET, OBJ_NAME)
        self.assertEqual(s3.delete_folder(PREFIX, BUCKET), True)

    def test_get_images(self):
        self.assertEqual(len(s3.get_images(USER_NAME, UNUSED_CATEGORY)), 0)

        # upload 4 jpg/png images
        s3.upload_file_wname(IMG1, BUCKET, USER_NAME + '/housing/1.jpg')
        s3.upload_file_wname(IMG2, BUCKET, USER_NAME + '/housing/2.jpg')
        s3.upload_file_wname(IMG3, BUCKET, USER_NAME + '/housing/3.jpg')
        s3.upload_file_wname(IMG4, BUCKET, USER_NAME + '/housing/4.jpg')
        links = s3.get_images(USER_NAME)
        self.assertEqual(len(links), 4)

    def tearDown(self):
        s3.delete_folder(PREFIX, BUCKET)




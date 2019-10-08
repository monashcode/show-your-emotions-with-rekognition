# Getting Started: Show your emotions with AWS Rekognition
![Diagram](https://github.com/melbourne-cloudtools-meetup/show-your-emotions-with-rekognition/blob/ALL_STEPS/repoImages/Banner.png?raw=true)
### What is this?
This is the <b>Show your emotions with Rekognition</b> repository as part of the event organised by the [Melbourne AWS Programming and Tools Meetup](https://www.meetup.com/Melbourne-AWS-Programming-and-Tools-Meetup/events/261692367/).

 - This repository contains instructions and code to build your first AWS Rekognition application with python and Cloud9 IDE hosted on AWS. 
 - It is split up into 5 Steps, each containing instructions to get your first Rekognition project to work. 
 - Step 5 is the option to go serverless via putting code into a AWS Lambda function which is triggered by S3 events. 
### What is Rekognition?
 - Rekognition is a AWS managed image and video analysis service. 
 - You just provide an image or video to the Rekognition API, and the service can identify objects, people, text, scenes, and activities. It can detect any inappropriate content as well. 
 - Rekognition also provides highly accurate facial analysis and facial recognition. You can detect, analyze, and compare faces for a wide variety of use cases, including user verification, cataloging, people counting, and public safety.
 - Rekognition webpage - https://aws.amazon.com/rekognition/

#### Other AWS services involved in this workshop
 - S3 - https://aws.amazon.com/s3/
 - Cloud9 - https://aws.amazon.com/cloud9/
 - Lambda - https://aws.amazon.com/lambda/   (Workshop option, refer Step 5 below)
## Pre-requisites
 - AWS account (admin role recommended)
 - Cloud9 IDE 
    - Login into aws management console, type "cloud9" into the search bar and enter
    - Switch region to Singapore (any available Cloud9 region will work, but closest region will reduce latency of the IDE)
    - Hit "Create environment" button
    - Choose the name and hit "Next step"
    - Choose "Create a new instance for environment (EC2)" --> t2.micro --> Amazon Linux --> Leave everything else default --> "Next step" --> "Create environment"
    - Now wait for the IDE to be initialized

## Workshop diagram (step 1 to 4)
![Diagram](https://github.com/melbourne-cloudtools-meetup/show-your-emotions-with-rekognition/blob/ALL_STEPS/repoImages/Simple_Steps.png?raw=true)
## Step 1 - Basic preparation
 - Install dependencies. Libraries we need are included in setup.sh. Run it to install.

 - Create an aws S3 bucket to store the image to be used in next steps. This bucket is also used to store processed image and enable a signed url to allow temporary access to the image from a user who doesn't have aws credentials. 

 - Create a rekognition collection to store the facial signature. A facial signature consists of feature vectors sampled by aws rekognition service from input image frame and this metadata can be used for matching faces and emotioanl analysis. AWS rekognition service groups the signatures about objects including faces into collections. 
    ```bash
    # Clone the github repo

    git clone <repo>
    
    # Change directory to the cloned repository
    
    cd show-your-emotions-with-rekognition
    
    # Install dependencies
    # Make sure the console outputs "Dependencies installed successfully." 

    ./setup.sh

    # Create your s3 buckets using command below, pick a globally unique bucket name. 
    # These bucket name will be used in next steps. Name can be a mixture of lowercase letters and numbers.
    # If successful, console will prompt: "make_bucket:<your bucket name>" e.g. aws s3 mb s3://rekognition-workshop-simon
    # Use command  'aws s3 ls' to verify the creation of bucket

    aws s3 mb s3://<your_raw_images_bucket_name>
    aws s3 mb s3://<your_processed_images__bucket_name>

    # Create a rekognition pool 
    # Console will prompt "StatusCode": 200 when successful
    # e.g.  aws rekognition create-collection --collection-id rekognition-workshop-simon

    aws rekognition create-collection --collection-id <your_collection_name> 

    ```

## Step 2 - Upload an image to S3 bucket
 - Ready a photo and save it onto your local machine, make sure there is at least one face in it. AWS Rekognition service can index up to 100 faces at once, here we keep it simple by letting rekognition index the one prominent face. Detail shown in step 3.

 - Upload it to your Cloud9 IDE working directory: same directory where .py files resides

 - In case the Cloud9 'Upload Local Files" doesn't work, follow the steps below:
    - Step 1: Change "IMAGE_PATH" in 'convertImageBase64.py' (e.g. "IMAGE_PATH = "~/workspace/wolverine.jpg") and run it on local machine against the image file
    - Step 2: In Cloud9, open 'assembleImg.py', paste the base64 string into the designated place, and change the new image name, then run it. An image will be created.
    ```
    ~/workspace $ python convertImageBase64.py                                                              
   /9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoK
   CgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAFAAeADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgc...
   qunC6hVTcQjJGPvLXhup6ZLZznerIvrjHFTboVe50kN1dWcJRiQitlcHrXe+Etdj1iBbe6AWdflSQ9Gryew1m5TKzN5sfQhq09C1z7Be+agIQkZXoKTjYE7nqBvIbDVXtpi0Suu0uBww9CKEaOObMUhUDkZNVvEtoniDw4mp6e7efAMvjg4rlNB1VpibSfHnL93AznB9anldx3P/Z

   Please copy the string above into designated place in assembleImg.py manually
   ```
    OR (if the file is online already)
    - Step 1: from your repo directory, curl the image(s) to the directory
    ```
    curl https://hips.hearstapps.com/digitalspyuk.cdnds.net/17/10/1489149452-wolverine-surprise-hugh-jackman-wants-to-be-wolverine-forever-and-here-s-how-he-can-do-it.jpeg > image.jpg
    ```

 - Check if the image is in the working directory.

 - Give the command below to upload the image to the s3 bucket
    ```bash
    # Parameter -i followed by path to the image and -b followed by the bucket name are required 
    # E.g. python3 upload_to_s3.py -i raw_image.jpg -b rekognition-workshop-simon

    python3 upload_to_s3.py -i <image_name> -b <bucket_name>
    ```

## Step 3 - Use the main function to index the image to Rekognition 
 - Modify the variable names in index.py according to the comments

 - It performs tasks below sequentially: 
    - Indexing the face to AWS Rekognition service 
    - Process the metadata received from Rekognition service 
    - Print the resulsts of facial analysis to the console
    - Put a bounding box around the face on the image 
    - Send the image to the s3 processed images bucket 

 - Run it
    ```bash
    python3 index.py
    ```

## Step 4 - Generate a signed url for users without aws credentials to temporarily access the image
- By default, all objects uploaded to S3 are private. In order to allow public access, the object's permissions need to be altered. This can be done by altering the Bucket or Object policies, or by creating a temporary URL that allows access. 

- Attempt to access the object by the direct URL (can be located in the object screen in the S3 console). Observe that the image is not accessible directly.

```
E.g.

This XML file does not appear to have any style information associated with it. The document tree is shown below.
<Error>
 <Code>AccessDenied</Code>
 <Message>Access Denied</Message>
 <RequestId>FCB390BE80C6AADF</RequestId>
 <HostId>
  81Dswc+uohL/I//f/rVErmWzMl8eddu+DewMxYpwv69WvcUQaNo5CxlIVqsHTNBHkBqHweOZDIU=
 </HostId>
</Error>
```

- A user who does not have AWS credentials or permission to access an S3 object can be granted temporary access by using a presigned URL

 - A presigned URL is generated by an AWS user who has access to the object. The generated URL is then given to the unauthorized user. The presigned URL can be entered in a browser or used by a program or HTML webpage. The credentials used by the presigned URL are those of the AWS user who generated the URL

 - A presigned URL remains valid for a limited period of time which is specified when the URL is generated
    ```bash
    # Parameter -i followed by name of processed image and -b followed by the processed images bucket name are required

    python3 url_gen.py -i <image_name> -b <bucket_name>
    ```
 - Copy the url prompted on console and paste it to your browser

## Step 5 (workshop option) - Go serverless: create a lambda function
![Diagram](https://github.com/melbourne-cloudtools-meetup/show-your-emotions-with-rekognition/blob/ALL_STEPS/repoImages/Lambda.png?raw=true)
 - We ran index.py in the previous step but we do not want to do it every time we upload a new photo to the S3 bucket. Instead we will create a lambda function so that S3 will trigger the whole process automatically whenever we upload a an image to S3
 - AWS Lambda lets you run code without provisioning or managing servers. You pay only for the compute time you consume - there is no charge when your code is not running.

    - Lambda features:
        - No server to manage
            - AWS Lambda automatically runs your code without requiring you to provision or manage servers. Just write the code and upload it to Lambda
        - Continous scaling
            - AWS Lambda automatically scales your application by running code in response to each trigger. Your code runs in parallel and processes each trigger individually, scaling precisely with the size of the workload
        - Subsecond metering 
            - With AWS Lambda, you are charged for every 100ms your code executes and the number of times your code is triggered. You don't pay anything when your code isn't running

 - Follow steps below to create a lambda function:

    - Step 1 - Steup IAM role 
        - Go to the IAM dashboard by clicking Service the topleft corner and type in "IAM" and enter
        - Choose "Roles" --> "Create role" --> "AWS service" --> "Lambda" --> "Lambda" --> "Select your use case - lambda" --> "Next: Permission" --> "Create policy" --> Check "AmazonS3FullAccess" and "AmazonRekognitionFullAccess" --> "Next: Tags" --> "Next: Review" --> type a name into "Role name" --> "Create role"

    - Step 2 - Create a lambda function
        - Open aws management console, type "lambda" into the "Find Service" search bar and enter
        - Hit "Create function" then check "Author from scratch"
        - Enter a name for "Function name"
        - Choose Python 3.6 for Runtime
        - Choose "Use an existing role" then choose the IAM role created from last step

    - Step 3 - Add a event trigger to this lambda function following last step
        - Hit "+ Add trigger" button then select "S3"
        - Choose the bucket that has just been created and select "All object ctreate events" for Event type.
        - Check "Enable trigger" and hit "Add" button
        - Hit "Functions" at the topleft corner of the refreshed page

    - Step 4 - Edit the lambda function
        - Choose the lambda function from last step
        - Edit lambda_handler.py with some variable names changed (the file in the repo)
        - Scroll down to "Function code" area and replace the code in editor with the modified code in lambda_handler.py
        - Change "Timeout" to 10 sec in Basic setting section
        - Hit "Save" at topright corner

    - Step 5 - Setup environment for lambda
    
        - IMPORTANT: Ensure the PROCESSED_BUCKET variable is set to the processed images bucket set up in Step 1
          - Ensure the processed bucket name is different to the raw images bucket name
            ```
            E.g. change:
            PROCESSED_BUCKET = "<YOUR_PROCESSED_BUCKET>"
            to whatever your bucket name is:
            PROCESSED_BUCKET = "rekognition-workshop-processed"
            ```

        - Note: the library cv2 used in this lambda function is not native to aws lambda runtime environment. So we need to set it up here. 
        - In Cloud9 termianl, run: 
            ```bash
            # Create a .zip file contains the package we need 

            docker run --rm -v $(pwd):/package tiivik/lambdazipper opencv-python 
            sudo zip -r9 opencv-python.zip lambda_handler.py

            # Update the lambda function we created

            aws lambda update-function-code --function-name <your_lambda_function_name> --zip-file fileb://opencv-python.zip
            ```
        - Change the content under "Handler" section to: "lambda_handler.lambda_handler" <-- without double quotes
        - Change "memory" to 512 mb in Basic setting section
        - Edit lambda_handler.py in Cloud9:
            - change variable names follow the comments
        - Then in Cloud9 termianl, run: 
            ```bash
            # Update the lambda function

            sudo zip -r9 opencv-python.zip lambda_handler.py
            aws lambda update-function-code --function-name <your_lambda_function_name> --zip-file fileb://opencv-python.zip
            ```
    - Step 6 - Trigger the lambda
    
        - Now we are ready to trigger the lambda function
        - Use command below:
            ```bash
            # Upload an image to the bucket
            # The bucket event will trigger the lambda function to run

            python3 upload_to_s3.py -i <image_name> -b <bucket_name>
            ```
    - Step 7 - Open the s3 bucket, there should be a lambda-processed image with the name you decided. Open the image file and see how it looks. 
    
## Step 6 (extra credit!) Mark-up the image with the emotion meta-data
  Open lambda_handler.py in the IDE. Find the following commented out line.
  ```
  # cv2.putText(img, str(emotion), (50, 50), FONT, 1, (0, 255, 0), 2, cv2.LINE_AA)
  ```
  This line should write the main facial emotion onto the image while processing, however, it doesn't work. See if you can fix it!

## FAQ


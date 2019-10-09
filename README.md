# Getting Started: Show your emotions with AWS Rekognition
![Diagram](https://github.com/melbourne-cloudtools-meetup/show-your-emotions-with-rekognition/blob/ALL_STEPS/repoImages/Banner.png?raw=true)
### What is this?
This is the <b>Show your emotions with Rekognition</b> repository for the NAB x MAC x diversIT event.

 - This repository contains instructions and code to build your first AWS Rekognition application with Python and Cloud9 IDE hosted on AWS. 
 - It is split up into 5 Steps, each containing instructions to get your first Rekognition project to work. 
 - Step 5 is the option to go serverless via putting code into a AWS Lambda function which is triggered by S3 events. 
### What is Rekognition?
 - Rekognition is a AWS managed image and video analysis service. 
 - You just provide an image or video to the Rekognition API, and the service can identify objects, people, text, scenes, and activities. It can detect any inappropriate content as well. 
 - Rekognition also provides highly accurate facial analysis and facial recognition. You can detect, analyze, and compare faces for a wide variety of use cases, including user verification, cataloging, people counting, and public safety.
 - Rekognition webpage - https://aws.amazon.com/rekognition/

#### Other AWS services involved in this workshop
 - S3 - https://aws.amazon.com/s3/
    - Amazon Simple Storage Service (S3) lets you store objects and is where you'll be storing the images and other files in this workshop.
 - Cloud9 - https://aws.amazon.com/cloud9/
    - AWS Cloud9 is a cloud-based IDE that lets you write, run and debug your code with just a browser.
    - It includes a code editor, debugger and terminal.
    - It comes prepackaged with essential tools for popular programming languages and AWS so you don't have to install files or configure your machine to start new projects.
 - Lambda - https://aws.amazon.com/lambda/   (Workshop option, refer Step 5 below)
    - AWS Lambda lets you run code without provisioning or managing servers
    - You only pay for the compute time you consume so there is no charge when your code is not running
    - Not having to worry about server administration (patching, scalability, security) has led to the trend of serverless computing 
    
## Pre-requisites
 - AWS account (admin role recommended)
 - Cloud9 IDE 
    - Login into the [AWS Management Console](https://console.aws.amazon.com/console/home), type "cloud9" into the search bar and enter
    - Switch region to Singapore (any available Cloud9 region will work, but closest region will reduce latency of the IDE). You can switch your region at the top right corner once you are in the console.
    - Hit "Create environment" button
    - Choose a name (e.g. myCloud9Env) and hit "Next step"
    - Choose "Create a new instance for environment (EC2)" --> t2.micro --> Amazon Linux --> Leave everything else as default --> "Next step" --> "Create environment"
    - Now wait for the IDE to be initialized

## Workshop diagram (step 1 to 4)
![Diagram](https://github.com/melbourne-cloudtools-meetup/show-your-emotions-with-rekognition/blob/ALL_STEPS/repoImages/Simple_Steps.png?raw=true)
## Step 1 - Basic preparation
Now we're going to run the following commands below in the bash console at the bottom of the Cloud9 IDE.

 - Install our dependencies. The libraries we need are included in setup.sh. Run it to install.

 - Create an AWS S3 bucket to store the image to be used in next steps. This bucket is also used to store processed image and enable a presigned URL to allow temporary access to the image from a user who doesn't have AWS credentials. 

 - Create a Rekognition collection to store the facial signature. A facial signature consists of feature vectors sampled by AWS Rekognition service from input image frame and this metadata can be used for matching faces and emotional analysis. AWS Rekognition service groups the signatures about objects including faces into collections. 
    ```bash
    # Clone the github repo

    git clone https://github.com/monashcode/show-your-emotions-with-rekognition.git
    
    # Change directory to the cloned repository
    
    cd show-your-emotions-with-rekognition
    
    # Install dependencies
    # Make sure the console outputs "Dependencies installed successfully." 

    ./setup.sh

    # Create your 33 buckets using the command below, pick a globally unique bucket name. 
    # These bucket name will be used in next steps. Name can be a mixture of lowercase letters and numbers.
    # If successful, console will prompt: "make_bucket:<your bucket name>" e.g. aws s3 mb s3://rekognition-workshop-simon
    # Use command  'aws s3 ls' to find and verify the creation of bucket
    
    aws s3 mb s3://<your_raw_images_bucket_name>
    aws s3 mb s3://<your_processed_images__bucket_name>

    # Create a rekognition pool 
    # Console will prompt "StatusCode": 200 when successful
    # e.g.  aws rekognition create-collection --collection-id rekognition-workshop-simon

    aws rekognition create-collection --collection-id <your_collection_name> 

    ```

## Step 2 - Upload an image to S3 bucket
 - Ready a photo and save it onto your local machine, make sure there is at least one face in it. AWS Rekognition service can index up to 100 faces at once, here we keep it simple by letting Rekognition index the one prominent face. More details shown in step 3.
   - You can try this with any image you want but there are some sample images in the folder "sampleImages". If you use these, make sure you drag the images out to where your .py files reside (as below)
  
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

 - Give the command below to upload the image to the S3 bucket that holds the raw images
    ```bash
    # Parameter -i followed by path to the image and -b followed by the bucket name are required 
    # E.g. python3 upload_to_s3.py -i raw_image.jpg -b rekognition-workshop-simon

    python3 upload_to_s3.py -i <image_name> -b <your_raw_images_bucket_name>
    ```

## Step 3 - Use the main function to index the image to Rekognition 
 - Modify the variable names in index.py according to the comments

 - Our code will perform the tasks below sequentially: 
    - Index the face to AWS Rekognition service 
    - Process the metadata received from Rekognition service 
    - Print the results of facial analysis to the console
    - Put a bounding box around the face on the image 
    - Send the image to the s3 processed images bucket 

 - Save the file and run it
    ```bash
    python3 index.py
    ```

## Step 4 - Generate a presigned url for users without AWS credentials to temporarily access the image
- By default, all objects uploaded to S3 are private. In order to allow public access, the object's permissions need to be altered. This can be done by altering the Bucket or Object policies, or by creating a temporary URL that allows access (aka presigned URL). 

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
 
 - Run the command below to generate your presigned URL
    ```bash
    # Parameter -i followed by name of the processed image and -b followed by the processed images S3 bucket name are required

    python3 url_gen.py -i <image_name> -b <processed_bucket_name>
    ```
 - Copy the URL prompted on console and paste it to your browser/send it to others

## Step 5 - Go serverless: create a Lambda function
![Diagram](https://github.com/melbourne-cloudtools-meetup/show-your-emotions-with-rekognition/blob/ALL_STEPS/repoImages/Lambda.png?raw=true)
 - We ran index.py in the previous step but we do not want to do this manually every time we upload a new photo to the S3 bucket.
 - Instead we will create a Lambda function so that S3 will trigger the whole process automatically whenever we upload a an image to S3
 - AWS Lambda lets you run code without provisioning or managing servers. You pay only for the compute time you consume - there is no charge when your code is not running.

    - Lambda features:
        - No server to manage
            - AWS Lambda automatically runs your code without requiring you to provision or manage servers. Just write the code and upload it to Lambda
        - Continuous scaling
            - AWS Lambda automatically scales your application by running code in response to each trigger. Your code runs in parallel and processes each trigger individually, scaling precisely with the size of the workload
        - Subsecond metering 
            - With AWS Lambda, you are charged for every 100ms your code executes and the number of times your code is triggered. You don't pay anything when your code isn't running

 - Follow steps below to create a Lambda function:

    - Step 1 - Setup an Identity Access Management (IAM) role 
        - Go to the IAM dashboard by clicking Service the topleft corner and type in "IAM" and enter
        - Choose "Roles" --> "Create role" --> "AWS service" --> "Lambda"  --> "Next: Permission" --> "Attach permissions policies" --> Check "AmazonS3FullAccess" and "AmazonRekognitionFullAccess" --> "Next: Tags" --> "Next: Review" --> type a name into "Role name" (e.g. MyRekognitionRole) --> "Create role"

    - Step 2 - Create a Lambda function
        - Open AWS Management console, type "lambda" into the "Find Service" search bar and enter
        - Make sure you are in the same region as 
        - Hit "Create function" then check "Author from scratch"
        - Enter a name for "Function name" (e.g. RekognitionS3Function)
        - Choose Python 3.6 for Runtime
        - Under "Choose or create an execution role", choose "Use an existing role" then choose the IAM role created from last step

    - Step 3 - Add a event trigger to this Lambda function following last step
        - Hit "+ Add trigger" button then select "S3"
        - Select your S3 bucket that holds the raw images and select "All object create events" for the Event type.
        - Check "Enable trigger" and hit "Add" button
        - Hit "Functions" at the topleft corner of the refreshed page

    - Step 4 - Edit the Lambda function
        - Click on the Lambda function
        - Change "Timeout" to 10 sec in the Basic settings section below
        - Hit "Save" at the top right corner

    - Step 5 - Setup environment for Lambda
        - Over in the Cloud9 IDE, edit lambda_handler.py and fill in the variable names
        - IMPORTANT: Ensure the PROCESSED_BUCKET variable is set to the processed images bucket set up in Step 1
          - Ensure the processed bucket name is different to the raw images bucket name
            ```
            E.g. change:
            PROCESSED_BUCKET = "<YOUR_PROCESSED_BUCKET>"
            to whatever your bucket name is:
            PROCESSED_BUCKET = "rekognition-workshop-processed"
            ```

        - Note: the library cv2 used in this Lambda function is not native to AWS Lambda runtime environment. So we need to set it up here. 
        - In Cloud9 terminal, run: 
            ```bash
            # Create a .zip file contains the package we need 

            docker run --rm -v $(pwd):/package tiivik/lambdazipper opencv-python 
            sudo zip -r9 opencv-python.zip lambda_handler.py

            # Update the Lambda function we created

            aws lambda update-function-code --function-name <YOUR_LAMBDA_FUNCTION_NAME> --zip-file fileb://opencv-python.zip
            ```
        - Back in your Lambda window, Change the content under "Handler" section to: "lambda_handler.lambda_handler" <-- without double quotes
        - Change "memory" to 512 mb in Basic setting section
        - Edit lambda_handler.py in Cloud9:
            - change variable names follow the comments
        - Then in Cloud9 terminal, run: 
            ```bash
            # Update the Lambda function

            sudo zip -r9 opencv-python.zip lambda_handler.py
            aws lambda update-function-code --function-name <YOUR_LAMBDA_FUNCTION_NAME> --zip-file fileb://opencv-python.zip
            ```
    - Step 6 - Trigger the Lambda
    
        - Now we are ready to trigger the Lambda function
        - Use command below:
            ```bash
            # Upload an image to the bucket
            # The bucket event will trigger the lambda function to run

            python3 upload_to_s3.py -i <image_name> -b <bucket_name>
            ```
    - Step 7 - Open the S3 bucket, there should be a lambda-processed image with the name you decided. Open the image file and see how it looks. 
    - End result: When you now upload an image to your S3 bucket, Lambda automatically triggers and runs the specified code (from lambda_handler.py) to take the image metadata and place the processed image in your processed images S3 bucket.
       - Have a look at your processed images bucket to see an image starting with "lambda-processed-" + your raw images name
    
## Step 6 (extra credit!) Mark-up the image with the emotion meta-data
  Open lambda_handler.py in the IDE. Find the following commented out line.
  ```
  # cv2.putText(img, str(emotion), (50, 50), FONT, 1, (0, 255, 0), 2, cv2.LINE_AA)
  ```
  This line should write the main facial emotion onto the image while processing, however, it doesn't work. See if you can fix it!

## FAQ
 - Q: Nothing is changing when I make a change in the Cloud9 IDE?
    - A: Auto save isn't actually enabled by default so make sure to manually save after writing up the commands.
 -

# Face Recognition Subway Project

As the Philadelphia metro system, SEPTA gradually returns to pre-pandemic ridership levels [1], the demand for efficient travel is greater than ever. Have you ever found yourself rushing to catch a train, only to fumble for your credit card buried at the bottom of your backpack or purse? With the introduction of facial recognition technology, passengers will soon be able to effortlessly "swipe" in using just their faces, streamlining the boarding process.
[1] https://6abc.com/septa-regional-rail-train-expansion-philadelphia-commuters/14454932/

# How to run the code
- First, lone this project and download the necessary Python library using _pip install_.
- Then, create a Google Firebase account and set up Realtime Database and Storage in a project. Create a file named serviceAccountKey.json using the secret key obtained from the Google Project Services tab in Settings. Put some images of faces that are in a 200x200 .png form in the Images folder. There are already 3 currently in that folder.
- Next, run EncodeGenerator.py and AddDataToDatabase.py files to upload and encrypt images and customer data to Firebase. Also have premade data for the 3 customers.
- Finally, run main.py and see how the system behaves.

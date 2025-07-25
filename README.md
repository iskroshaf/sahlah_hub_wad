# sahlan_hub

Sahlan Hub is an e-commerce platform built using Django. It provides a seamless shopping experience for customers while offering a robust dashboard for sellers and administrators. This project includes essential e-commerce functionalities such as product management, order processing, and secure authentication.

## Setup Instructions

Follow the steps below to set up the project on your local machine:

### 1. Clone the Project  
Run the following command:  
`git clone https://github.com/iskroshaf/sahlan-hub-dev.git`  

Navigate into the project directory:  
`cd sahlan_hub`  

### 2. Create a Virtual Environment  
Create a virtual environment named `myenv`:  
`python -m venv myenv`  

### 3. Activate the Virtual Environment  
For Windows:  
`myenv\Scripts\activate`  

For Mac/Linux:  
`source myenv/bin/activate`  

### 4. Install Dependencies  
Run the following command to install all required packages:  
`python -m pip install -r requirements.txt`  

### 5. Create Media Directories  
Run the following commands to set up the necessary media folders:  

For Windows (Command Prompt):  
```sh
mkdir media
mkdir media\image_avatars
mkdir media\file_business_licenses

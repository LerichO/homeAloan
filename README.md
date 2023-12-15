# homeAloan from HackUTD X: Golden Hour
![image](https://github.com/LerichO/homeAloan/assets/86967773/62b400df-08c7-4d88-9208-990aa0fb575f)

The current generation of rising young adults face growing challenges in understanding and preparing for the housing market; this app seeks to mitigate that issue. HomeAloan is a website that seeks to evaluate the expenses and income of end users and provide meaningful insight into their eligibility for home loans.

Web app developed by Laya Srinivas, Suvel Muttreja, Joie Lin, Lerich Osay during the HackUTD X: Golden Hour Hackathon from November 4-5, 2023

structure of flask app:

<pre>
homeAloan
├── .gitignore - shows which files (like .pyc) for git to ignore.
├── app.py - This is the main file for our app.
├── loan_approval.py - This is where user input will be processed to determine if they are loan eligble.
├── suggestion_gpt.py - This is where our chatbot, powered by GPT, will be implemented.
├── readme.md - That's this file!
├── requirements.txt - Used for deployment to say what packages are needed.
├── runtime.txt - Ignore. Used for deployment.
├── static - This is where we house assets like images and stylesheets.
│   ├── css - Put stylesheets here.
│   │   └── css files
│   └── images - Put images here.
│       └── jpg and png files
└── templates - Put templates (views) in this folder.
    └── html documents
</pre>

To finish implementing in the future:
- Chatbot integration
- Implement page of graphs and other data vizualizations
- Improved UI of results page
- (Possibly) implementing React.js

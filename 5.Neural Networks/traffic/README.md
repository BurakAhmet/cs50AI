
An AI to identify which traffic sign appears in a photograph using neural networks.

### Video Demo

  https://github.com/BurakAhmet/cs50AI/assets/89780902/15cae668-1e40-4f89-ba8a-60c550220608


### My Conclusions

  At first, I wanted to achieve the highest accuracy with the dataset, so I used many layers. But it took too long to train, and the results weren't great. So, I tried removing layers one by one and adjusting settings. Surprisingly, this improved accuracy each time. So I noticed that more layers does not mean better accuracy and drop out affects the accuracy very much.



### Usage
  Download requirements: pip3 install -r requirements.txt
  
  Start application: python traffic.py gtsrb
  * Download the data set:
    - [Data set](https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip)
    - [Small data set](https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb-small.zip)


          

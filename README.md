Submitted By  - Pankaj Chhabra

I used Python 2.7.9 and used sys, datetime and time libraries.

I have tried to implement all the features without using exotic libraries available for data analysis. 

Also for the test cases ip and resources had extra line in the end but hours didn't so I formatted my code accordingly. There's a chance you might get a conflight because of this adjustment but the results would be same.

For finding 10 frequent ips I used hashmap to store their number of occurrence and find the 10 most frequent

For finding 10 most heavy resources I have used the same approach 

For finding the busiest 60 minutes window I have first aggregated the frequency of logs at timestamp present in the log and then used that for lookup during window sliding as it would be o(1) running time and skip if instance of timestamp not present in aggregate hashmap. (the code is little untidy because of last minute time constraints)

For feature 4 I have used the error codes and the timestamp to find when the user is blocked and write his blocked request to blocked.txt.



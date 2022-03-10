# FMIS Query Runs

There are two parts to this: parsing user data and turning it into a Query object; and actually running that query. 

**Notes**

Class-based Query model:
- Scott handles parsing into query class
- Json config files
- I handle running the query class

My tasks:
- Testing
  - Could use CI and test on the full Git repo
  - Need a way to validate incoming JSON data (this is more Scott's realm)
  - Mostly, we need to test that example query runs work as expected. 
- Actual Query Runs
  - Folder Setup
  - Browser Setup
  - Query Run + Download
  - Browser Teardown
- Binning it into daily runs (list of queries)
- Need to secure the Username and Password
- Setup:
    - Need to understand all the bash files – they are very repetitive.

Could even do it at a web level – google form into a JSON. Add new Query. 

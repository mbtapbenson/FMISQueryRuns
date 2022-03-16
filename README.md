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
  - Folder Setup (DONE)
  - Browser Setup (DONE)
  - Query Run + Download (DONE)
  - Browser Teardown (DONE)
  - Query post-processing – this is rm_head.py
  - **Question**: are the flags for "dev/prod/both" and "ohio/local/both" still active? should we deprecate these?
    - Answer: yes. 
- Binning it into daily runs (list of queries)
- Need to secure the Username and Password (ENV variables seem like the best way to do this)
- Setup:
    - Need to understand all the bash files – they are very repetitive. (DONE)

Could even do it at a web level – google form into a JSON. Add new Query. 

Crontab scheduling: 
- We need to have a "run_from_file.py" running daily with the daily_runs file as an argument. 
- This interval-level binning is handled from crontab. 

Class Architecture:
- Query
    - Subquery (Direct queries, parameterized queries, etc.)
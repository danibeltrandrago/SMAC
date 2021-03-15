# Smart Cities Project

## Workflow:

- Python files
  - [x] `air_pollution.py`: Pull the data from the pollution link site 
  - [x] `traffict.py`: Read from Barcelona transit site where to pull all the transit data in a .json file
- MongoDB
  - [x] `docker.compose.yml`: Docker file containing Grafana and MongoDB
  - [ ] Connect and upload all the data generated by the files
  - [ ] Give a specific format
- Grafana
  - [ ] Docker file
  - [ ] Connect and read values
  - [ ] Make/Get a dashboard
  - [ ] Show data


## Webapges to inspect:
- [Pollution link site](https://aqicn.org/map/barcelona/)
- [Barcelona transit data](https://com-shi-va.barcelona.cat/ca/transit)


## MongoDB dataset structure
The database will have two main sets: Air pollution and traffic density. The first one is made 
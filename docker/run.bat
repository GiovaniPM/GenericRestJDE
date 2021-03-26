SET ORACLE_SERVER=172.17.0.3

docker run -d --env ORACLE_SERVER --name="gapi" -p 8080:8080 gapimg
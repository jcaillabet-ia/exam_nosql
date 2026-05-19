docker exec -it my_mongo bash
mongoimport -d sample -c books --authenticationDatabase admin --username datascientest --password dst123 --file /data/db/books.json

python3 main.py
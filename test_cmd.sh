curl -XPOST -H "Content-type: application/json" http://127.0.0.1:9527/ -d '{"myname": "电子科技大学@2023"}'
curl -XPOST -H "Content-type: application/json" http://127.0.0.1:9528/ -d '{"tasks": ["task 1", "task 2", "task 3"]}'
curl -XPOST -H "Content-type: application/json" http://127.0.0.1:9529/ -d '{"age": 123}'

curl http://127.0.0.1:9528/myname
curl http://127.0.0.1:9527/tasks
curl http://127.0.0.1:9527/notexistkey

curl -XDELETE http://127.0.0.1:9529/myname
curl http://127.0.0.1:9527/myname
curl -XDELETE http://127.0.0.1:9529/myname
## To deploy from DockerHub:

```
docker run -p 9475:9475 patrickkwang/robokop-nlp
```

## To run from source:

```
git clone https://github.com/ncats-gamma/robokop-nlp
cd robokop-nlp
echo PYTHONPATH=$PYTHONPATH:.
./parser/api/server.py
```
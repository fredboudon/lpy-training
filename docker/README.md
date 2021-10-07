```sh
docker build --rm -f "docker/Dockerfile" -t vmango-lab-demo:lastest .
```

```sh
docker run -it --rm -p 8080:8080 -v $PWD/notebooks:/notebooks vmango-lab-demo:lastest jupyter lab --port=8080 --notebook-dir=/notebooks
```

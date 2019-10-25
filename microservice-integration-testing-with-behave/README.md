# Testing a microservice with Docker and `behave`

### Building

You can use the canned `Makefile` to build the image:

```bash
$ make build
```


### Testing

You can run the integration tests with `docker-compose`. The `Makefile` defines
the testing target also:

```bash
$ make test-integration
```

To interactively step through stages in the container, you can run the integration
tests in "shell" mode, which will spin up the service and the testing container
within the same docker network:

```bash
$ make test-integration-shell
```


### Running locally

To run locally, spin up your docker container:

```bash
$ docker run -p 8000:9000 --rm -it my-cool-timezone-app:local
```

And then POST a JSON to the service:

```bash
$ curl -d '{"timezone": "UTC"}' -H "Content-Type: application/json" -X POST localhost:8000/get-time
{"body":"2019-10-25 14:25:29 PM","status":"OK"}

$ curl -d '{"timezone": "US/Eastern"}' -H "Content-Type: application/json" -X POST localhost:8000/get-time
{"body":"2019-10-25 10:27:37 AM","status":"OK"}

$ curl -d '{"timezone": "US/Central", "format": "%m/%d/%Y %H:%M"}' -H "Content-Type: application/json" -X POST localhost:8000/get-time
{"body":"10/25/2019 09:28","status":"OK"}
```

You can also hit the GET endpoints:

```bash
$ curl -X GET localhost:8000/ping
{"body":"pong","status":"Serving"}

$ echo $(curl -X GET localhost:8000/help)
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   157  100   157    0     0  22428      0 --:--:-- --:--:-- --:--:-- 22428
{"body":"Accepted args:
	timezone: (required)
	format: (optional)
Example: {\"timezone\": \"UTC\", \"format\": \"%Y-%m-%d %H:%M:%S %p\"}","status":"OK"}
```

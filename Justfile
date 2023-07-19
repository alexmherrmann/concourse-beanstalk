


ecrRepo:="ghcr.io/alexmherrmann/concourse-beanstalk"

build:
  docker build -t {{ecrRepo}}:$(git describe --tags) .

push:
  docker push {{ecrRepo}}:$(git describe --tags)
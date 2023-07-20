


ecrRepo:="ghcr.io/alexmherrmann/concourse-beanstalk"

newtag:
  git tag $(./increment.py $(git describe --tags))
build:
  docker build -t {{ecrRepo}}:$(git describe --tags) .

push:
  docker push {{ecrRepo}}:$(git describe --tags)
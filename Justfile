


ecrRepo:="ghcr.io/alexmherrmann/concourse-beanstalk"

d:
  @just -l

newtag:
  git tag $(./increment.py $(git describe --tags))
  git push
  git push --tags
build:
  docker build -t {{ecrRepo}}:$(git describe --tags) .

push:
  docker push {{ecrRepo}}:$(git describe --tags)
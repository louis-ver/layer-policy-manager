# Assumptions
1. When you say 'all our types of layers', I assumed that this was simply all layers. I understood 'types' to be Runtimes, and therefore simply fetch all (latest) layers when adding a new permission.
# Usage Notes
If you want to use `layer-policy-manager` via Docker, you have to mount your `~/.aws/credentials` file to the Docker filesystem. The run command would look something like this:

```
docker run \
    -it \
    --rm \
    -v /Users/<user>/.aws/credentials:/root/.aws/credentials \
    layer-policy-manager [OPTIONS]
```
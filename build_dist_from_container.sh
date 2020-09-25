#!/bin/bash
docker run --rm -v $(pwd)/dist:/workspaces/pyko/dist codebasic/pyko:dev /bin/bash -c "VERSION=$VERSION ./build_dist.sh"
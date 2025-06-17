#!/bin/sh
set -e


SCALE_FACTOR=${SCALE_FACTOR:-1}
echo "Will generate and upload about ${SCALE_FACTOR}GB worth of data to the S3 bucket ${BUCKET?BUCKET is not an environment variable} under the prefix ${PREFIX?PREFIX is not an environment variable}"

tmp_dir=$(mktemp --directory)
trap exiting exit
function exiting() { rm -rf "${tmp_dir}"; exit; }

pushd "$tmp_dir"

docker run -it  --rm \
  -v "$(pwd)":/data \
  ghcr.io/scalytics/tpch-docker:main \
  -s "${SCALE_FACTOR}"

aws s3 sync ./ s3://${BUCKET}/${PREFIX}

popd

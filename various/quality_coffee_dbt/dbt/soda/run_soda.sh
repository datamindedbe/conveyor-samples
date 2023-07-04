# Handle paths relative to the script location
if [[ ${BASH_SOURCE} = */* ]]; then
    cd -- "${BASH_SOURCE%/*}/" || exit
fi

soda test-connection -d quality_coffee -c configuration.yml
soda scan -d quality_coffee -c configuration.yml checks.yml

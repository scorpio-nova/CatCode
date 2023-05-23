#!/bin/bash

# get the directory of the script
SCRIPT_FOLDER=$(cd "$(dirname "$0")";pwd)
# Set DIRECTORY_FOLDER as the path ../../ to DIRECTORY_FOLDER
DIRECTORY_FOLDER="${SCRIPT_FOLDER}/../../"
echo "DIRECTORY_FOLDER: ${DIRECTORY_FOLDER}"

echo "Creating JavaTransformer.jar"
mvn clean compile assembly:single
java -jar "${SCRIPT_FOLDER}/target/jar/JavaTransformer.jar" > "${DIRECTORY_FOLDER}/target/default.log"

echo "Saved JAR into target/jar/"

java -jar "${SCRIPT_FOLDER}/target/jar/JavaTransformer.jar" "${DIRECTORY_FOLDER}/data/categorical_data/morphism_input/mathqa_java/" "${DIRECTORY_FOLDER}/data/categorical_data/morphism_output/mathqa_java" || exit 1
java -jar "${SCRIPT_FOLDER}/target/jar/JavaTransformer.jar" "${DIRECTORY_FOLDER}/data/categorical_data/morphism_input/mbxp_java/" "${DIRECTORY_FOLDER}/data/categorical_data/morphism_output/mbxp_java" || exit 1
java -jar "${SCRIPT_FOLDER}/target/jar/JavaTransformer.jar" "${DIRECTORY_FOLDER}/data/categorical_data/morphism_input/humaneval_java/" "${DIRECTORY_FOLDER}/data/categorical_data/morphism_output/humaneval_java" || exit 1

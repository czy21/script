def build(){
    sh 'chmod +x ${PROJECT_ROOT}/gradlew && ${PROJECT_ROOT}/gradlew --init-script ${GRADLE_INIT_FILE} --build-file ${PROJECT_ROOT}/build.gradle ${PROJECT_MODULE}:clean ${PROJECT_MODULE}:build -x test'
}

return this;
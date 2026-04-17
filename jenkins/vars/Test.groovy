


def call(Map inputs) {
        pipeline {
        agent any
        stages {
            stage('Init') {
                steps {
                    script {
                        sh "echo ${inputs.a}"
                    }
                }
            }
        }
    }
}
#!/usr/bin/env groovy

def call(Map map) {
    pipeline {
       agent any
       stages{
         stage('build'){
            steps{
                script{
                }
                sh 'echo hello docker'
            }
         }
       }
    }
}


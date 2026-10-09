pipeline {
    agent any

    stages {
        stage('1. Checkout') {
            steps {
                checkout scm
                sh 'ls -la'
            }
        }
        stage('2. Docker Check') {
            steps {
                sh 'docker --version'
                sh 'echo "Hello from Jenkins!"'
            }
        }
    }
}
pipeline {
    agent any

    stages {
        stage('1. Checkout') {
            steps {
                checkout scm
                sh 'ls -la'
            }
        }


        stage('2. Security: SAST (Semgrep)') {
            steps {
                echo ' Запуск Semgrep: статический анализ кода...'
                sh '''
                    pip3 install --quiet --break-system-packages semgrep
                    semgrep scan --config=p/security-audit --error . || true
                '''
            }
        }

        stage('3. Docker Check') {
            steps {
                sh 'docker --version'
                sh 'echo "Hello from Jenkins!"'
            }
        }
    }
}
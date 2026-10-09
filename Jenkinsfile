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
                echo '🔍 Запуск Semgrep: статический анализ кода...'
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE}:/src" \
                        returntocorp/semgrep:latest \
                        semgrep scan --config=p/security-audit --error /src || true
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
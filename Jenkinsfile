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
                        -w /src \
                        returntocorp/semgrep:latest \
                        sh -c "rm -rf /tmp/scan && mkdir -p /tmp/scan && cp *.py /tmp/scan/ 2>/dev/null; cp requirements.txt /tmp/scan/ 2>/dev/null; cd /tmp/scan && semgrep scan --config=p/security-audit --error . || true"
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
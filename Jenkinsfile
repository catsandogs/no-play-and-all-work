pipeline {
    agent any

    environment {
        image = "calculator-api"
        container = "calculator-prod"
        tag = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('1. checkout') {
            steps {
                echo 'загрузка кода из репозитория'
                checkout scm
                sh 'ls -la'
            }
        }

        stage('2. semgrep') {
            steps {
                echo 'статический анализ кода'
                sh '''
                    pip3 install --quiet --break-system-packages semgrep
                    semgrep scan --config=p/security-audit --error . || true
                '''
            }
        }

        stage('3. trivy fs') {
            steps {
                echo 'сканирование зависимостей'
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE}:/src" \
                        -w /src \
                        aquasec/trivy:latest \
                        fs --severity HIGH,CRITICAL . || true
                '''
            }
        }

        stage('4. docker build') {
            steps {
                echo "сборка образа версии ${tag}"
                sh "docker build -t ${image}:${tag} -t ${image}:latest ."
                sh "docker images ${image}"
            }
        }

        stage('5. trivy image') {
            steps {
                echo 'сканирование собранного образа'
                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest \
                        image --severity HIGH,CRITICAL calculator-api:latest || true
                '''
            }
        }

        stage('6. deploy') {
            steps {
                echo 'перезапуск контейнера'
                sh '''
                    docker stop ${container} || true
                    docker rm ${container} || true
                    docker run -d --name ${container} -p 8000:8000 ${image}:latest
                    sleep 5
                    curl -sf http://172.17.0.1:8000/health || (docker logs ${container} && exit 1)
                '''
            }
        }
    }
}
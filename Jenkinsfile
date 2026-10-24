pipeline {
    agent any

    environment {
        IMAGE_NAME = "calculator-api"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "calculator-prod"
    }

    stages {
        stage('1. Checkout') {
            steps {
                echo "Загрузка кода из репозитория..."
                checkout scm
            }
        }

        stage('2. Security: SAST (Semgrep)') {
            steps {
                echo 'Запуск Semgrep: статический анализ кода...'
                sh '''
                    pip3 install --quiet --break-system-packages semgrep
                    semgrep scan --config=p/security-audit --error . || true
                '''
            }
        }

        stage('3. Security: SCA (Trivy FS)') {
            steps {
                echo 'Сканирование зависимостей (requirements.txt)...'
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE}:/src" \
                        -w /src \
                        aquasec/trivy:latest \
                        fs --severity HIGH,CRITICAL . || true
                '''
            }
        }

        stage('4. Docker Build') {
            steps {
                echo "Сборка Docker-образа версии ${IMAGE_TAG}..."
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                sh "docker images ${IMAGE_NAME}"
            }
        }

        stage('5. Security: Container Scan (Trivy Image)') {
            steps {
                echo 'Сканирование собранного Docker-образа...'
                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest \
                        image --severity HIGH,CRITICAL ${IMAGE_NAME}:latest || true
                '''
            }
        }

        stage('6. Deploy (Rotation)') {
            steps {
                echo 'Обновление приложения (перезапуск контейнера)...'
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}:latest

                    echo "Ожидание запуска приложения..."
                    for i in $(seq 1 15); do
                        if curl -s http://localhost:8000/health > /dev/null; then
                            echo "Приложение успешно запустилось!"
                            exit 0
                        fi
                        echo "Попытка $i из 15... ждем 1 секунду"
                        sleep 1
                    done

                    echo "Healthcheck failed: приложение не ответило за 15 секунд"
                    docker logs ${CONTAINER_NAME}
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "Пайплайн #${env.BUILD_NUMBER} успешно завершён."
        }
        failure {
            echo "Сборка #${env.BUILD_NUMBER} провалилась. Смотрите логи."
        }
    }
}
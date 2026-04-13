pipeline {
    agent any

    // 1. AJOUT : On déclare l'outil Maven pour que Jenkins sache exécuter la commande 'mvn'
    // ⚠️ IMPORTANT : Remplace 'Maven_3' par le nom exact que tu as donné à ton Maven dans Jenkins (Administrer Jenkins > Tools)
    tools {
        maven 'Maven3'
        jdk 'JDK21'
    }

    stages {
        stage('Checkout') {
            steps {
                // Récupère le code depuis le SCM configuré dans Jenkins
                checkout scm
            }
        }

        stage('Build') {
            steps {
                // 2. AJOUT : On se déplace dans le bon dossier avant de lancer les commandes
                dir('ICDE848') {
                    script {
                        if (isUnix()) {
                            sh 'mvn clean compile -B'
                        } else {
                            bat 'mvn clean compile -B'
                        }
                    }
                }
            }
        }

        stage('Unit Tests') {
            steps {
                // On n'oublie pas le dir() ici aussi
                dir('ICDE848') {
                    script {
                        if (isUnix()) {
                            sh 'mvn test -B'
                        } else {
                            bat 'mvn test -B'
                        }
                    }
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: '**/target/surefire-reports/*.xml'
                }
            }
        }

        stage('Jacoco') {
            steps {
                // Analyse de la couverture de code avec Jacoco
                dir('ICDE848') {
                    script {
                        if (isUnix()) {
                            sh 'mvn verify -B -DskipTests'
                        } else {
                            bat 'mvn verify -B -DskipTests'
                        }
                    }
                }
            }
            post {
                always {
                    // Publie le rapport de couverture Jacoco
                    jacoco(
                        execPattern: '**/target/jacoco.exec',
                        classPattern: '**/target/classes',
                        sourcePattern: '**/src/main/java'
                    )
                }
            }
        }

        stage('SpotBugs') {
            steps {
                // Analyse des bugs avec SpotBugs
                dir('ICDE848') {
                    script {
                        if (isUnix()) {
                            sh 'mvn spotbugs:check -B'
                        } else {
                            bat 'mvn spotbugs:check -B'
                        }
                    }
                }
            }
            post {
                always {
                    // Rend le rapport disponible dans les artefacts au lieu d'utiliser le plugin Warnings NG qui n'est pas installé
                    archiveArtifacts allowEmptyArchive: true, artifacts: '**/spotbugsXml.xml'
                }
            }
        }

        stage('Checkstyle') {
            steps {
                // Et le dir() ici également
                dir('ICDE848') {
                    script {
                        if (isUnix()) {
                            sh 'mvn checkstyle:checkstyle -B -Dcheckstyle.config.location=checkstyle.xml'
                        } else {
                            bat 'mvn checkstyle:checkstyle -B -Dcheckstyle.config.location=checkstyle.xml'
                        }
                    }
                }
            }
            post {
                always {
                    archiveArtifacts allowEmptyArchive: true, artifacts: '**/target/checkstyle-result.xml'
                }
            }
        }
    }

    post {
        failure {
            script {
                echo "Le build a échoué. Envoi de l'email d'alerte..."
                if (isUnix()) {
                    sh "python3 ICDE848/send_email.py failure \"${env.BUILD_URL}\" \"${env.JOB_NAME}\""
                } else {
                    bat "python ICDE848/send_email.py failure \"${env.BUILD_URL}\" \"${env.JOB_NAME}\""
                }
            }
        }
        fixed {
            script {
                echo "Le build est de nouveau stable après une erreur. Envoi de l'email..."
                if (isUnix()) {
                    sh "python3 ICDE848/send_email.py fixed \"${env.BUILD_URL}\" \"${env.JOB_NAME}\""
                } else {
                    bat "python ICDE848/send_email.py fixed \"${env.BUILD_URL}\" \"${env.JOB_NAME}\""
                }
            }
        }
    }
}
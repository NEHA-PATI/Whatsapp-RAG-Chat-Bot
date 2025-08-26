git add .
git commit -m "push_and_deploy"
git push

printf '\n\n*** DEPLOYING IN PROD SERVER ***\n\n'
ssh kite "cd /home/django/suniba-ai/django_project && ./pull_and_deploy.sh"
